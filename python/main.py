import openpyxl
from deal_metrics import extract_expanded_deal_metrics
from case_data import build_cases, CaseData
from cell_mappings import cell_mappings  # Assuming this contains your mappings
from python.debt_repayment_schedule import extract_debt_repayment_schedules
from python.lbo_run import run_lbo_model_with_repayment_schedule
from monte_carlo_simulation import MonteCarloSimulator

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

# Define the list of years we want to model for the LBO
years = [2024, 2025, 2026, 2027, 2028, 2029, 2030]

# Define the exit horizons (3, 4, 5, and 6 years after investment)
exit_horizons = [2026, 2027, 2028, 2029]

del all_cases['Bottom-Up Case']

print("cases data: ", all_cases)
print("deal metrics: ", expanded_metrics)
print("repayment schedule: ", repayment_schedule)

case = all_cases["Management Case"]

lbo_results = run_lbo_model_with_repayment_schedule(expanded_metrics=expanded_metrics, case_data=case, repayment_schedule=repayment_schedule, years=[2024,2025,2026,2027,2028,2029], tax_rate=0.217)

for key in lbo_results.keys():
    print(lbo_results[key])
    print()

# # Step 4: Initialize the Monte Carlo simulator with all necessary data
# monte_carlo_simulator = MonteCarloSimulator(
#     cases=all_cases,
#     deal_metrics=expanded_metrics,
#     repayment_schedule=repayment_schedule,
#     years=years,
#     iterations=100000,
#     exit_horizons=exit_horizons
# )
#
# # Step 5: Run the simulation
# results_df = monte_carlo_simulator.run_simulation()
#
# # Step 6: Analyze the results
# monte_carlo_simulator.analyze_results(results_df)