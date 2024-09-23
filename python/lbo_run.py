# lbo_run.py

import pandas as pd
from numpy_financial import irr
from python.debt_repayment_schedule import calculate_debt_balances_and_interest

def run_lbo_model_with_repayment_schedule(expanded_metrics, case_data, repayment_schedule, years, tax_rate=0.25, exit_horizons=[3, 4, 5, 6]):
    """
    Runs the LBO model with a predefined debt repayment schedule and calculates results for multiple exit years.

    Parameters:
        expanded_metrics (dict): Deal-specific metrics like debt, interest rates, and entry/exit multiples.
        case_data (CaseData): Operating data (e.g., revenue, EBITDA) for the selected case.
        repayment_schedule (dict): Predefined repayment amounts by year for each debt tranche.
        years (list): List of years to calculate.
        tax_rate (float): Corporate tax rate (default is 25%).
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
        'RCF': 0  # Revolver starts with a 0 balance (consistent key name as 'RCF')
    }
    interest_rates = {
        'Senior A': expanded_metrics['Senior A Interest'],
        'Senior B': expanded_metrics['Senior B Interest'],
        'Subordinate': expanded_metrics['Subordinate Interest'],
        'Mezzanine': expanded_metrics['Mezzanine Cash Interest'],
        'RCF': expanded_metrics['RCF Interest']  # Consistent key for 'RCF'
    }

    # Calculate opening balances, closing balances, and interest payments for each debt tranche
    debt_info = calculate_debt_balances_and_interest(
        expanded_metrics, repayment_schedule, interest_rates, starting_balances, years
    )

    # Initialize financials for the LBO run
    cash_balance = 0.0
    equity_investment = expanded_metrics['ZQWL Equity'] + expanded_metrics['Co-Invest'] + expanded_metrics['MPP']

    # Create a dictionary to store results for multiple exit years
    exit_results = {}

    for year in years:

        # Revenue, EBITDA margin, and normalization (use CaseData)
        revenue = case_data.revenue[year]
        ebitda_margin = case_data.ebitda_margin[year]
        reported_ebitda = revenue * ebitda_margin
        normalized_ebitda = reported_ebitda - case_data.ebitda_normalizations[year]

        # Correct EBITDA and EBIT calculation using depreciation and amortization from CaseData
        ebitda = normalized_ebitda
        depreciation = revenue * case_data.depreciation_percent[year]
        amortization = revenue * case_data.amortization_percent[year]
        ebit = ebitda - depreciation - amortization

        # Total interest expense including PIK interest
        pik_interest = expanded_metrics.get('PIK Interest', 0)
        total_interest_expense = sum(debt_info[debt_type][year]['Interest Payment'] for debt_type in debt_info) + pik_interest

        # Earnings before tax (EBT)
        ebt = ebit - total_interest_expense
        taxes = max(0, ebt * tax_rate)
        net_income = ebt - taxes

        # Changes in working capital
        if year > min(case_data.revenue.keys()):  # Only calculate if there's a previous year
            previous_year = year - 1
            change_in_nwc = (
                (case_data.inventory[year] - case_data.inventory[previous_year]) +
                (case_data.accounts_receivable[year] - case_data.accounts_receivable[previous_year]) -
                (case_data.accounts_payable[year] - case_data.accounts_payable[previous_year])
            )
        else:
            change_in_nwc = 0  # No change in NWC for the first year



        # Change in provisions (if applicable)
        change_in_provisions = case_data.provisions[year] - case_data.provisions[previous_year] if year > min(years) else 0

        # Capital expenditures (CapEx)
        capex = revenue * case_data.m_capex_percent[year] + revenue * case_data.e_capex_percent[year]

        # Free Cash Flow (before debt service)
        fcf = net_income - change_in_nwc - change_in_provisions - capex

        # Apply mandatory debt repayments
        for debt_type in ['Senior A', 'Senior B', 'Subordinate', 'Mezzanine']:
            repayment = repayment_schedule[debt_type][year]
            debt_info[debt_type][year]['Closing Balance'] -= repayment

        # Revolver repayment/utilization logic
        revolver_utilization = repayment_schedule['RCF Utilization'][year]
        revolver_repayment = repayment_schedule['RCF Repayment'][year]
        debt_info['RCF'][year]['Closing Balance'] += revolver_utilization - revolver_repayment

    # Now perform calculations for multiple exit horizons
    initial_year = min(years)
    for exit_horizon in exit_horizons:
        exit_year = initial_year + exit_horizon

        # Ensure the exit year is valid within the model's timeline
        if exit_year in case_data.ebitda:
            exit_ebitda = normalized_ebitda  # Use normalized EBITDA for exit calculation
            exit_enterprise_value = exit_ebitda * expanded_metrics.get('Exit Multiple', expanded_metrics['Entry Multiple'])

            # Calculate net debt at exit
            net_debt_at_exit = sum(debt_info[debt_type][exit_year]['Closing Balance'] for debt_type in debt_info)
            equity_value_at_exit = exit_enterprise_value - net_debt_at_exit

            # IRR & MoM Calculations
            cash_flows = [-equity_investment] + [0] * exit_horizon + [equity_value_at_exit]
            investor_irr = irr(cash_flows)
            investor_mom = equity_value_at_exit / equity_investment

            # Store the results for this exit horizon
            exit_results[exit_horizon] = {
                'Exit Year': exit_year,
                'IRR': investor_irr,
                'MoM': investor_mom,
                'Equity Value at Exit': equity_value_at_exit,
                'Net Debt at Exit': net_debt_at_exit,
                'Cash Flows': cash_flows
            }

    return exit_results