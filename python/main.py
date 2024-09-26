import openpyxl
from deal_metrics import extract_expanded_deal_metrics
from case_data import build_cases, CaseData
from cell_mappings import cell_mappings  # Assuming this contains your mappings
from python.debt_repayment_schedule import extract_debt_repayment_schedules
from python.lbo_run import run_lbo_model_with_repayment_schedule

# Define the path to your Excel file
EXCEL_FILE_PATH = '../cleaned_lbo_template.xlsx'

# Load the workbook
wb = openpyxl.load_workbook(EXCEL_FILE_PATH, data_only=True)

# Access the 'LBO' and 'Cases' sheets
lbo_sheet = wb['LBO']
cases_sheet = wb['Cases']

# Extract deal metrics
expanded_metrics = extract_expanded_deal_metrics(lbo_sheet)

# Build and extract all case data
all_cases = build_cases(cell_mappings, cases_sheet)

# Extract debt repayment schedule from the LBO sheet
repayment_schedule = extract_debt_repayment_schedules(lbo_sheet)

# Assuming you have the expanded_metrics and all_cases dictionaries
selected_case = all_cases['Management Case']

# Define the list of years we want to model for the LBO
years = [2024, 2025, 2026, 2027, 2028, 2029, 2030]

# Define the exit horizons (3, 4, 5, and 6 years after investment)
exit_horizons = [3, 4, 5, 6]

# Run the LBO model with the repayment schedule and multiple exit horizons
results = run_lbo_model_with_repayment_schedule(expanded_metrics, selected_case, repayment_schedule, years, exit_horizons=exit_horizons)

# Print the results for each exit horizon
# for horizon, metrics in results.items():
#     print(f"\nExit after {horizon} years (Exit Year: {metrics['Exit Year']}):")
#     print(f"  Investor IRR: {metrics['IRR']:.2%}")
#     print(f"  Investor MoM: {metrics['MoM']:.2f}x")
#     print(f"  Net Debt at Exit: {metrics['Net Debt at Exit']:.2f}")
#     print(f"  Equity Value at Exit: {metrics['Equity Value at Exit']:.2f}")

def extract_stochastic_variables(expanded_metrics, all_cases):
    # Initialize the data structure
    stochastic_variables = {}

    # Define the cases as min, mode, and max
    cases = {
        'min': all_cases['Sensitivity Case'],   # Pessimistic case
        'mode': all_cases['Primary Case'],      # Base case
        'max': all_cases['Management Case']     # Optimistic case
    }

    # Years to consider
    years = [year for year in all_cases['Primary Case'].revenue.keys()]

    # Variables that vary over years
    time_series_variables = [
        'revenue_growth',
        'ebitda_margin',
        'inventory',
        'accounts_receivable',
        'accounts_payable',
        'other_wc_assets',
        'other_wc_liabilities',
        'maintenance_capex',
        'expansion_capex',
        'depreciation',
        'amortization',
        'provisions'
    ]

    # Extract time-series variables
    for var in time_series_variables:
        stochastic_variables[var] = {}
        for year in years:
            # Initialize a dict for this year
            stochastic_variables[var][year] = {}
            for case_name, case_data in cases.items():
                # Get the value
                value = getattr(case_data, var).get(year)
                # Store in the dict
                stochastic_variables[var][year][case_name] = value

    # Variables that are scalars
    scalar_variables = [
        'Exit Multiple',  # From expanded_metrics
        # Interest Rates
        'Senior A Interest',
        'Senior B Interest',
        'Subordinate Interest',
        'Mezzanine Cash Interest',
        'RCF Interest'
    ]

    # Extract Exit Multiple
    # Assuming 'Exit Multiple' is consistent across periods
    exit_multiples = []
    for period, metrics in expanded_metrics.get('Exit Metrics by Period', {}).items():
        exit_multiple = metrics.get('Exit Multiple')
        if exit_multiple is not None:
            exit_multiples.append(exit_multiple)
    if exit_multiples:
        stochastic_variables['Exit Multiple'] = {
            'min': min(exit_multiples),
            'mode': sum(exit_multiples) / len(exit_multiples),
            'max': max(exit_multiples)
        }
    else:
        stochastic_variables['Exit Multiple'] = {
            'min': None,
            'mode': None,
            'max': None
        }

    # Extract Interest Rates
    for var in scalar_variables:
        if var != 'Exit Multiple':
            value = expanded_metrics.get(var)
            stochastic_variables[var] = {
                'min': value,
                'mode': value,
                'max': value
            }

    # Extract Exit Timing
    exit_periods = expanded_metrics.get('Exit Metrics by Period', {}).keys()
    exit_years = []
    for period in exit_periods:
        # Extract the number of years from 'Entry + 3yrs'
        if 'Entry + ' in period and 'yrs' in period:
            num_years = int(period.replace('Entry + ', '').replace('yrs', ''))
            exit_years.append(num_years)
    if exit_years:
        stochastic_variables['Exit Timing'] = {
            'min': min(exit_years),
            'mode': sum(exit_years) / len(exit_years),
            'max': max(exit_years)
        }
    else:
        stochastic_variables['Exit Timing'] = {
            'min': None,
            'mode': None,
            'max': None
        }

    return stochastic_variables

# Call the function to extract stochastic variables
stochastic_variables = extract_stochastic_variables(expanded_metrics, all_cases)

