# lbo_run.py

import pyxirr
from python.debt_repayment_schedule import calculate_debt_balances_and_interest

def run_lbo_model_with_repayment_schedule(expanded_metrics, case_data, repayment_schedule, years, tax_rate=0.217,
                                          exit_horizons=[2026, 2027, 2028, 2029]):
    year_results = {}

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

    equity_investment = expanded_metrics['ZQWL Equity'] + expanded_metrics['Co-Invest'] + expanded_metrics['MPP']
    revolver_balance = 0
    cash_balance = 0.0  # Initialize cash balance for the first year

    exit_results = {}
    exit_horizon_to_key = {2026: 'Entry + 3yrs', 2027: 'Entry + 4yrs', 2028: 'Entry + 5yrs', 2029: 'Entry + 6yrs'}

    per_year_data = {}

    for year in years:

        revenue = case_data.revenue[year]
        ebitda_margin = case_data.ebitda_margin[year]
        reported_ebitda = revenue * ebitda_margin
        normalized_ebitda = reported_ebitda - case_data.ebitda_normalizations[year]

        ebitda = normalized_ebitda
        depreciation = revenue * case_data.depreciation_percent[year]
        amortization = revenue * case_data.amortization_percent[year]
        ebit = ebitda - depreciation - amortization

        pik_interest = expanded_metrics.get('PIK Interest', 0)
        total_interest_expense = -sum(
            debt_info[debt_type][year]['Interest Payment'] for debt_type in debt_info) + pik_interest

        ebt = ebit + total_interest_expense
        taxes = max(0, ebt * tax_rate)
        net_income = ebt - taxes

        if year > min(case_data.revenue.keys()):
            previous_year = year - 1

            other_wc_assets_current = case_data.other_wc_assets_percent[year] * revenue
            other_wc_assets_previous = case_data.other_wc_assets_percent[previous_year] * case_data.revenue[previous_year]

            other_wc_liabilities_current = -case_data.other_wc_liabilities_percent[year] * revenue
            other_wc_liabilities_previous = -case_data.other_wc_liabilities_percent[previous_year] * case_data.revenue[previous_year]

            trade_working_capital_current = case_data.inventory[year] + case_data.accounts_receivable[year] + \
                                            case_data.accounts_payable[year]
            trade_working_capital_previous = case_data.inventory[previous_year] + case_data.accounts_receivable[previous_year] + \
                                             case_data.accounts_payable[previous_year]

            net_working_capital_current = trade_working_capital_current + other_wc_assets_current + other_wc_liabilities_current
            net_working_capital_previous = trade_working_capital_previous + other_wc_assets_previous + other_wc_liabilities_previous

            change_in_nwc = net_working_capital_current - net_working_capital_previous
            change_in_provisions = case_data.provisions[year] - case_data.provisions[previous_year]

        else:
            change_in_nwc = 0
            change_in_provisions = 0

        capex = revenue * case_data.m_capex_percent[year] + revenue * case_data.e_capex_percent[year]
        cfads = reported_ebitda - change_in_nwc - change_in_provisions - capex - taxes
        cash_interest_paid = -sum(debt_info[debt_type][year]['Interest Payment'] for debt_type in debt_info)
        mandatory_debt_repayment = sum(
            repayment_schedule[debt_type][year] for debt_type in ['Senior A', 'Senior B', 'Subordinate', 'Mezzanine'])

        # Calculate Free Cash Flow post-debt service (FCF post-debt service)
        fcf_post_debt_service = cfads + cash_interest_paid + mandatory_debt_repayment

        # Store the unadjusted FCF post-debt service for debugging purposes
        original_fcf_post_debt_service = fcf_post_debt_service

        # Calculate Closing Balance pre-revolver as Free Cash Flow (pre-revolver)
        closing_balance_pre_revolver = original_fcf_post_debt_service

        # Revolver logic: Draw if FCF post-debt service is negative, repay if positive
        if fcf_post_debt_service < 0:
            # Draw exactly enough to cover the shortfall (bring cash balance to 0)
            revolver_draw = -fcf_post_debt_service  # Draw the amount needed to bring cash to zero
            revolver_balance += revolver_draw
            cash_balance = 0  # After drawing from revolver, cash balance should be exactly 0
            fcf_post_debt_service = 0  # Reset FCF post revolver draw (since it's fully covered)

        else:
            if fcf_post_debt_service > 0 and revolver_balance > 0:
                # Repay revolver if there is a positive FCF and an outstanding revolver balance
                revolver_repayment = min(fcf_post_debt_service, revolver_balance)
                revolver_balance -= revolver_repayment
                fcf_post_debt_service -= revolver_repayment
                cash_balance -= revolver_repayment  # Adjust cash balance with revolver repayment

            if fcf_post_debt_service > 0:
                # Excess cash after revolver repayment, accumulate in cash balance
                cash_balance += fcf_post_debt_service
                fcf_post_debt_service = 0  # Reset after adding to cash balance


        average_revolver_balance = (starting_balances['RCF'] + revolver_balance) / 2
        revolver_interest = average_revolver_balance * interest_rates['RCF']

        for debt_type in ['Senior A', 'Senior B', 'Subordinate', 'Mezzanine']:
            repayment = repayment_schedule[debt_type][year]
            debt_info[debt_type][year]['Closing Balance'] -= repayment

        debt_info['RCF'][year] = {
            'Opening Balance': revolver_balance,
            'Closing Balance': revolver_balance,
            'Interest Payment': revolver_interest
        }

        per_year_data[year] = {
            'ebitda': ebitda,
            'cash_balance': cash_balance,
            'debt_closing_balances': {debt_type: debt_info[debt_type][year]['Closing Balance'] for debt_type in debt_info},
        }

        if year in exit_horizons:
            exit_key = exit_horizon_to_key[year]
            exit_multiple = expanded_metrics['Exit Metrics by Period'][exit_key]['Exit Multiple']
            ebitda_exit = per_year_data[year]['ebitda']
            enterprise_value_exit = exit_multiple * ebitda_exit
            total_debt = sum(per_year_data[year]['debt_closing_balances'][debt_type] for debt_type in
                             per_year_data[year]['debt_closing_balances'] if debt_type != 'RCF')
            cash_exit = per_year_data[year]['cash_balance']
            net_debt_exit = total_debt - cash_exit

            equity_value_exit = enterprise_value_exit - net_debt_exit
            mom = equity_value_exit / equity_investment
            cf_equity = [-equity_investment] + [0] * (years.index(year)-1) + [equity_value_exit]
            irr_equity = pyxirr.irr(cf_equity)
            irr_equity_percent = irr_equity * 100

            exit_results[year] = {
                'Exit Year': year,
                'Equity Value at Exit': equity_value_exit,
                'Equity Investment': equity_investment,
                'MoM': mom,
                'IRR': irr_equity_percent,
                'Enterprise Value at Exit': enterprise_value_exit,
                'Net Debt at Exit': net_debt_exit,
            }

    return exit_results
