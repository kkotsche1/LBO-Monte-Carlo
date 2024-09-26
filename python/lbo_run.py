# lbo_run.py

import pandas as pd
from numpy_financial import irr
from python.debt_repayment_schedule import calculate_debt_balances_and_interest


def run_lbo_model_with_repayment_schedule(expanded_metrics, case_data, repayment_schedule, years, tax_rate=0.217,
                                          exit_horizons=[3, 4, 5, 6]):
    """
    Runs the LBO model with a predefined debt repayment schedule and calculates results for multiple exit years.

    Parameters:
        expanded_metrics (dict): Deal-specific metrics like debt, interest rates, and entry/exit multiples.
        case_data (CaseData): Operating data (e.g., revenue, EBITDA) for the selected case.
        repayment_schedule (dict): Predefined repayment amounts by year for each debt tranche.
        years (list): List of years to calculate.
        tax_rate (float): Corporate tax rate (default is 21.7%).
        exit_horizons (list): List of exit year horizons relative to year 0 (e.g., [3, 4, 5, 6]).

    Returns:
        dict: A dictionary containing IRR, MoM, and other metrics for each exit year horizon.
    """

    # Extract initial debt balances and interest rates from expanded_metrics
    starting_balances = {
        'Senior A': expanded_metrics['Senior A Amount'],
        'Senior B': expanded_metrics['Senior B Amount'],
        'Subordinate': expanded_metrics['Subordinate Amount'],
        'Mezzanine': expanded_metrics['Mezzanine Cash Amount'],
        'RCF': 0  # Revolver starts with a 0 balance
    }

    interest_rates = {
        'Senior A': expanded_metrics['Senior A Interest'],
        'Senior B': expanded_metrics['Senior B Interest'],
        'Subordinate': expanded_metrics['Subordinate Interest'],
        'Mezzanine': expanded_metrics['Mezzanine Cash Interest'],
        'RCF': expanded_metrics['RCF Interest']  # Interest on revolver
    }

    # Maximum revolver amount you can draw
    max_revolver_draw = expanded_metrics['RCF Amount']

    # Calculate opening balances, closing balances, and interest payments for each debt tranche
    debt_info = calculate_debt_balances_and_interest(
        expanded_metrics, repayment_schedule, interest_rates, starting_balances, years
    )

    # Initialize financials for the LBO run
    cash_balance = 0.0
    equity_investment = expanded_metrics['ZQWL Equity'] + expanded_metrics['Co-Invest'] + expanded_metrics['MPP']

    # Revolver balance starts at zero
    revolver_balance = 0

    # Create a dictionary to store results for multiple exit years
    exit_results = {}

    for year in years:

        # Revenue, EBITDA margin, and normalization (use CaseData)
        revenue = case_data.revenue[year]
        ebitda_margin = case_data.ebitda_margin[year]
        reported_ebitda = revenue * ebitda_margin
        normalized_ebitda = reported_ebitda - case_data.ebitda_normalizations[year]

        # Calculate EBITDA and EBIT
        ebitda = normalized_ebitda
        depreciation = revenue * case_data.depreciation_percent[year]
        amortization = revenue * case_data.amortization_percent[year]
        ebit = ebitda - depreciation - amortization

        # Total interest expense, including any PIK interest
        pik_interest = expanded_metrics.get('PIK Interest', 0)
        total_interest_expense = sum(
            debt_info[debt_type][year]['Interest Payment'] for debt_type in debt_info) + pik_interest

        # Earnings before tax (EBT)
        ebt = ebit - total_interest_expense
        taxes = max(0, ebt * tax_rate)
        net_income = ebt - taxes

        # Calculate changes in working capital
        if year > min(case_data.revenue.keys()):  # Only calculate if there's a previous year
            previous_year = year - 1

            # Calculate Other W/C Assets and Liabilities as a percentage of revenue
            other_wc_assets_current = case_data.other_wc_assets_percent[year] * revenue
            other_wc_assets_previous = case_data.other_wc_assets_percent[previous_year] * case_data.revenue[
                previous_year]

            other_wc_liabilities_current = -case_data.other_wc_liabilities_percent[year] * revenue
            other_wc_liabilities_previous = -case_data.other_wc_liabilities_percent[previous_year] * case_data.revenue[
                previous_year]

            # Calculate Trade Working Capital and changes
            trade_working_capital_current = case_data.inventory[year] + case_data.accounts_receivable[year] + \
                                            case_data.accounts_payable[year]
            trade_working_capital_previous = case_data.inventory[previous_year] + case_data.accounts_receivable[
                previous_year] + case_data.accounts_payable[previous_year]

            # Net Working Capital is Trade Working Capital + Other W/C Assets + Other W/C Liabilities
            net_working_capital_current = trade_working_capital_current + other_wc_assets_current + other_wc_liabilities_current
            net_working_capital_previous = trade_working_capital_previous + other_wc_assets_previous + other_wc_liabilities_previous

            # Change in Net Working Capital
            change_in_nwc = net_working_capital_current - net_working_capital_previous

            # Calculate Change in Provisions
            change_in_provisions = case_data.provisions[year] - case_data.provisions[previous_year]

        else:
            change_in_nwc = 0  # No change in NWC for the first year
            change_in_provisions = 0  # No change in provisions for the first year

        # Capital expenditures (CapEx) based on revenue percentages
        capex = revenue * case_data.m_capex_percent[year] + revenue * case_data.e_capex_percent[year]

        # Calculate CFADS (Cash Flow Available for Debt Service)
        cfads = reported_ebitda - change_in_nwc - change_in_provisions - capex - taxes

        # Calculate cash interest paid (sum of interest on all debt tranches)
        cash_interest_paid = -sum(debt_info[debt_type][year]['Interest Payment'] for debt_type in debt_info)

        # Calculate mandatory debt repayment (sum of repayments across all debt tranches)
        mandatory_debt_repayment = sum(
            repayment_schedule[debt_type][year] for debt_type in ['Senior A', 'Senior B', 'Subordinate', 'Mezzanine'])

        # Calculate Free Cash Flow post-debt service (FCF post-debt service)
        fcf_post_debt_service = cfads + cash_interest_paid + mandatory_debt_repayment
        print(f"Year {year}: Free Cash Flow Post-Debt Service: {fcf_post_debt_service}")

        # Revolver logic: Draw if FCF post-debt service is negative, repay if positive
        if fcf_post_debt_service < 0:
            # Draw from revolver to cover the shortfall, but ensure it doesn't exceed max_revolver_draw
            revolver_draw = min(-fcf_post_debt_service,
                                max_revolver_draw - revolver_balance)  # Limited by max revolver amount
            revolver_balance += revolver_draw
            fcf_post_debt_service = 0  # After covering the shortfall, FCF becomes 0
            print(f"Year {year}: Revolver Draw: {revolver_draw}")
        elif fcf_post_debt_service > 0 and revolver_balance > 0:
            # Repay revolver if there is a positive FCF and an outstanding revolver balance
            revolver_repayment = min(fcf_post_debt_service, revolver_balance)
            revolver_balance -= revolver_repayment
            fcf_post_debt_service -= revolver_repayment
            print(f"Year {year}: Revolver Repayment: {revolver_repayment}")

        # Calculate revolver interest based on average balance
        average_revolver_balance = (starting_balances['RCF'] + revolver_balance) / 2
        revolver_interest = average_revolver_balance * interest_rates['RCF']

        # Store revolver balance and interest for debugging
        print(f"Year {year}: Revolver Balance: {revolver_balance}")
        print(f"Year {year}: Revolver Interest Payment: {revolver_interest}")

        # Apply mandatory debt repayments
        for debt_type in ['Senior A', 'Senior B', 'Subordinate', 'Mezzanine']:
            repayment = repayment_schedule[debt_type][year]
            debt_info[debt_type][year]['Closing Balance'] -= repayment

        # Update the revolver repayment/utilization in the debt_info
        debt_info['RCF'][year] = {
            'Opening Balance': revolver_balance,
            'Closing Balance': revolver_balance,
            'Interest Payment': revolver_interest
        }

    return exit_results

