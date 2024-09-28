# debt_repayment_schedule.py

from excel_utils import get_cell_value
from openpyxl import worksheet

def extract_debt_repayment_schedules(sheet):
    """
    Extracts repayment schedules for Senior A, Senior B, Subordinate, Mezzanine, and Revolver debt from the LBO model.

    Parameters:
        sheet (worksheet): The Excel sheet to extract data from.

    Returns:
        dict: A dictionary containing the repayment schedules for each debt type.
    """
    repayment_schedules = {}
    years = [2023, 2024, 2025, 2026, 2027, 2028, 2029, 2030]
    year_columns = ['I', 'J', 'K', 'L', 'M', 'N', 'O', 'P']  # Columns corresponding to 2023E - 2030E

    # Extract Senior A repayment schedule
    senior_a_repayments = {}
    for year, col in zip(years, year_columns):
        senior_a_repayments[year] = get_cell_value(sheet, f'{col}100')
    repayment_schedules['Senior A'] = senior_a_repayments

    # Extract Senior B repayment schedule
    senior_b_repayments = {}
    for year, col in zip(years, year_columns):
        senior_b_repayments[year] = get_cell_value(sheet, f'{col}108')
    repayment_schedules['Senior B'] = senior_b_repayments

    # Extract Subordinate repayment schedule
    subordinate_repayments = {}
    for year, col in zip(years, year_columns):
        subordinate_repayments[year] = get_cell_value(sheet, f'{col}116')
    repayment_schedules['Subordinate'] = subordinate_repayments

    # Extract Mezzanine repayment schedule
    mezzanine_repayments = {}
    for year, col in zip(years, year_columns):
        mezzanine_repayments[year] = get_cell_value(sheet, f'{col}125')
    repayment_schedules['Mezzanine'] = mezzanine_repayments

    # Extract Revolver utilization and repayment schedules
    revolver_utilization = {}
    revolver_repayments = {}
    for year, col in zip(years, year_columns):
        revolver_utilization[year] = get_cell_value(sheet, f'{col}135')
        revolver_repayments[year] = get_cell_value(sheet, f'{col}136')
    repayment_schedules['RCF Utilization'] = revolver_utilization
    repayment_schedules['RCF Repayment'] = revolver_repayments

    return repayment_schedules


def calculate_debt_balances_and_interest(deal_metrics, repayment_schedule, interest_rates, starting_balances, years):
    debt_info = {
        'Senior A': {},
        'Senior B': {},
        'Subordinate': {},
        'Mezzanine': {},
        'RCF': {}
    }
    balances = starting_balances.copy()

    for year in years:
        total_mandatory_repayment = 0  # To track total mandatory debt repayment per year

        for debt_type in ['Senior A', 'Senior B', 'Subordinate', 'Mezzanine']:
            opening_balance = balances[debt_type]

            # Repayment values are already negative, so just add them directly
            repayment = repayment_schedule[debt_type][year]
            total_mandatory_repayment += repayment  # Add to total mandatory repayment

            closing_balance = opening_balance + repayment  # Repayments reduce the balance (since they are negative)

            # Calculate interest based on opening balance for Senior B, and average balance for other debt types
            if debt_type == 'Senior B':
                interest_payment = opening_balance * interest_rates[debt_type]
            else:
                average_balance = (opening_balance + closing_balance) / 2
                interest_payment = average_balance * interest_rates[debt_type]

            # Store values for this year
            debt_info[debt_type][year] = {
                'Opening Balance': opening_balance,
                'Repayment': repayment,
                'Closing Balance': closing_balance,
                'Average Balance': average_balance if debt_type != 'Senior B' else opening_balance,  # For consistency
                'Interest Rate': interest_rates[debt_type],
                'Interest Payment': interest_payment
            }

            # Update opening balance for next year
            balances[debt_type] = closing_balance

        # Handle RCF separately
        debt_type = 'RCF'
        opening_balance = balances[debt_type]
        rcf_utilization = repayment_schedule['RCF Utilization'][year]
        rcf_repayment = repayment_schedule['RCF Repayment'][year]  # No negation needed
        closing_balance = opening_balance + rcf_utilization + rcf_repayment  # Both utilization and repayment are accounted for

        average_balance = (opening_balance + closing_balance) / 2
        interest_rate = interest_rates[debt_type]
        interest_payment = average_balance * interest_rate

        # Calculate undrawn balance and apply commitment fee
        max_revolver_draw = deal_metrics["RCF Amount"]
        undrawn_balance = max_revolver_draw - closing_balance  # Difference between max revolver and drawn balance
        commitment_fee = undrawn_balance * deal_metrics['RCF Undrawn Interest']  # Commitment fee on undrawn portion
        total_interest_payment = interest_payment + commitment_fee

        debt_info[debt_type][year] = {
            'Opening Balance': opening_balance,
            'RCF Utilization': rcf_utilization,
            'RCF Repayment': rcf_repayment,
            'Closing Balance': closing_balance,
            'Average Balance': average_balance,
            'Interest Rate, drawn': interest_rate,
            'Interest Rate, undrawn': commitment_fee,
            'Commitment Fee': commitment_fee,
            'Drawn Interest Fee': interest_payment,
            'Interest Payment': total_interest_payment
        }

        # Update opening balance for next year
        balances[debt_type] = closing_balance

    return debt_info
