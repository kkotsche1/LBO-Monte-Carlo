# main.py

import openpyxl
from deal_metrics import extract_expanded_deal_metrics
from case_data import build_cases
from cell_mappings import cell_mappings  # Assuming this contains your mappings

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

print(expanded_metrics)
print(all_cases)