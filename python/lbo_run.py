# lbo_run.py

import pandas as pd
from numpy_financial import irr
from python.debt_repayment_schedule import calculate_debt_balances_and_interest


def run_lbo_model_with_repayment_schedule(expanded_metrics, case_data, repayment_schedule, years, tax_rate=0.25,
                                          exit_horizons=[3, 4, 5, 6]):
    # Extract initial debt balances and interest rates from expanded_metrics
    starting_balances = {
        'Senior A': expanded_metrics['Senior A Amount'],
        'Senior B': expanded_metrics['Senior B Amount'],
        'Subordinate': expanded_metrics['Subordinate Amount'],
        'Mezzanine': expanded_metrics['Mezzanine Cash Amount'],
        'RCF': 0
    }
    interest_rates = {
        'Senior A': expanded_metrics['Senior A Interest'],
        'Senior B': expanded_metrics['Senior B Interest'],
        'Subordinate': expanded_metrics['Subordinate Interest'],
        'Mezzanine': expanded_metrics['Mezzanine Cash Interest'],
        'RCF': expanded_metrics['RCF Interest']
    }

    # Calculate debt balances and interest payments
    debt_info = calculate_debt_balances_and_interest(
        expanded_metrics, repayment_schedule, interest_rates, starting_balances, years
    )

    # Initialize financials
    cash_balance = 0.0
    equity_investment = expanded_metrics['ZQWL Equity'] + expanded_metrics['Co-Invest'] + expanded_metrics['MPP']

    exit_results = {}

    for year in years:
        revenue = case_data.revenue[year]
        ebitda_margin = case_data.ebitda_margin[year]
        reported_ebitda = revenue * ebitda_margin
        normalized_ebitda = reported_ebitda - case_data.ebitda_normalizations[year]

        # Correct EBITDA and EBIT calculation
        ebitda = normalized_ebitda
        depreciation = revenue * case_data.depreciation_percent[year]
        amortization = revenue * case_data.amortization_percent[year]
        ebit = ebitda - depreciation - amortization

        # Interest expenses
        total_interest_expense = sum(debt_info[debt_type][year]['Interest Payment'] for debt_type in debt_info)

        ebt = ebit - total_interest_expense
        taxes = max(0, ebt * tax_rate)
        net_income = ebt - taxes

        # Working capital changes
        if year > min(case_data.revenue.keys()):
            previous_year = year - 1
            change_in_nwc = (
                    (case_data.inventory[year] - case_data.inventory[previous_year]) +
                    (case_data.accounts_receivable[year] - case_data.accounts_receivable[previous_year]) -
                    (case_data.accounts_payable[year] - case_data.accounts_payable[previous_year])
            )
        else:
            change_in_nwc = 0

        # Change in provisions
        change_in_provisions = case_data.provisions[year] - case_data.provisions[previous_year] if year > min(
            years) else 0

        # Capital expenditures
        capex = revenue * case_data.m_capex_percent[year] + revenue * case_data.e_capex_percent[year]

        # Free Cash Flow
        fcf = net_income - change_in_nwc - change_in_provisions - capex

        # Debt repayments
        for debt_type in ['Senior A', 'Senior B', 'Subordinate', 'Mezzanine']:
            repayment = repayment_schedule[debt_type][year]
            debt_info[debt_type][year]['Closing Balance'] -= repayment

    return exit_results