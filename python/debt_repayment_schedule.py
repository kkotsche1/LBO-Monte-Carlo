from excel_utils import get_cell_value


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
    """
    Calculates debt balances and interest payments for each debt type based on the repayment schedule.

    Handles Senior A, Senior B, Subordinate, Mezzanine, and RCF (Revolver).

    Parameters:
        deal_metrics (dict): Contains initial debt amounts and interest rates.
        repayment_schedule (dict): Repayment schedule for each debt type.
        interest_rates (dict): Interest rates for each debt type.
        starting_balances (dict): Starting balances for each debt type.
        years (list): List of years for which to calculate balances.

    Returns:
        dict: Contains opening balances, closing balances, and interest payments for each year and debt type.
    """
    # Initialize debt_info for all debt types, including RCF
    debt_info = {
        'Senior A': {},
        'Senior B': {},
        'Subordinate': {},
        'Mezzanine': {},
        'RCF': {}
    }

    # Handle fixed repayment schedule for Senior A, Senior B, Subordinate, Mezzanine
    for debt_type in ['Senior A', 'Senior B', 'Subordinate', 'Mezzanine']:
        opening_balance = starting_balances[debt_type]
        for year in years:
            repayment = repayment_schedule[debt_type][year]
            closing_balance = opening_balance - repayment

            # Calculate interest payment based on the opening balance and interest rate
            interest_payment = opening_balance * interest_rates[debt_type]

            # Store the values for the year
            debt_info[debt_type][year] = {
                'Opening Balance': opening_balance,
                'Closing Balance': closing_balance,
                'Interest Payment': interest_payment
            }

            # Update opening balance for next year
            opening_balance = closing_balance

    # Handle RCF separately: utilization and repayment
    rcf_opening_balance = starting_balances['RCF']
    for year in years:
        # Revolver utilization and repayment
        rcf_utilization = repayment_schedule['RCF Utilization'][year]
        rcf_repayment = repayment_schedule['RCF Repayment'][year]
        rcf_closing_balance = rcf_opening_balance + rcf_utilization - rcf_repayment

        # Interest payment based on the opening balance
        rcf_interest_payment = rcf_opening_balance * interest_rates['RCF']

        # Store the values for the year in the debt_info dictionary for RCF
        debt_info['RCF'][year] = {
            'Opening Balance': rcf_opening_balance,
            'Closing Balance': rcf_closing_balance,
            'Interest Payment': rcf_interest_payment
        }

        # Update RCF opening balance for next year
        rcf_opening_balance = rcf_closing_balance

    return debt_info