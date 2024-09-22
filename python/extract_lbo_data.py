import re
import openpyxl
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from cell_mappings import cell_mappings
import numpy as np

# Define the path to your Excel file
EXCEL_FILE_PATH = '../cleaned_lbo_template.xlsx'  # Update with your actual file path

# Load the workbook
wb = openpyxl.load_workbook(EXCEL_FILE_PATH, data_only=True)

# Access the 'LBO' and 'Cases' sheets
lbo_sheet = wb['LBO']
cases_sheet = wb['Cases']


@dataclass
class CaseData:
    name: str
    # Key P&L Drivers
    revenue: Dict[int, float] = field(default_factory=dict)
    ebitda: Dict[int, float] = field(default_factory=dict)
    ebitda_normalizations: Dict[int, float] = field(default_factory=dict)
    depreciation: Dict[int, float] = field(default_factory=dict)
    amortization: Dict[int, float] = field(default_factory=dict)
    ebit: Dict[int, float] = field(default_factory=dict)
    # CapEx
    maintenance_capex: Dict[int, float] = field(default_factory=dict)
    expansion_capex: Dict[int, float] = field(default_factory=dict)
    # Balance Sheet Items
    inventory: Dict[int, float] = field(default_factory=dict)
    accounts_receivable: Dict[int, float] = field(default_factory=dict)
    accounts_payable: Dict[int, float] = field(default_factory=dict)
    other_wc_assets: Dict[int, float] = field(default_factory=dict)
    other_wc_liabilities: Dict[int, float] = field(default_factory=dict)
    provisions: Dict[int, float] = field(default_factory=dict)
    # Key Stats
    revenue_growth: Dict[int, float] = field(default_factory=dict)
    ebitda_margin: Dict[int, float] = field(default_factory=dict)
    depreciation_percent: Dict[int, float] = field(default_factory=dict)
    amortization_percent: Dict[int, float] = field(default_factory=dict)
    ebit_margin: Dict[int, float] = field(default_factory=dict)
    m_capex_percent: Dict[int, float] = field(default_factory=dict)
    e_capex_percent: Dict[int, float] = field(default_factory=dict)
    inventory_percent: Dict[int, float] = field(default_factory=dict)
    accounts_receivable_percent: Dict[int, float] = field(default_factory=dict)
    accounts_payable_percent: Dict[int, float] = field(default_factory=dict)
    other_wc_assets_percent: Dict[int, float] = field(default_factory=dict)
    other_wc_liabilities_percent: Dict[int, float] = field(default_factory=dict)
    provisions_growth: Dict[int, float] = field(default_factory=dict)
    # Add more fields as necessary


def extract_years_from_sheet(sheet, year_cells: List[str]) -> List[int]:
    """
    Extracts years from specified cells in a sheet.
    Assumes that each cell contains a date string in the format 'Mon-YYE' or similar.
    """
    import re
    from datetime import datetime

    year_pattern = re.compile(r'^[A-Za-z]{3}[-/\.]?(\d{2,4})[A-Za-z]*$')  # Matches 'Dec-23E', 'Jun/24', etc.
    years = set()

    for cell in year_cells:
        cell_value = sheet[cell].value
        if isinstance(cell_value, str):
            cell_value = cell_value.strip()
            match = year_pattern.match(cell_value)
            if match:
                year_str = match.group(1)
                if len(year_str) == 2:
                    year_suffix = int(year_str)
                    # Adjust century if necessary
                    full_year = 2000 + year_suffix if year_suffix < 100 else year_suffix
                elif len(year_str) == 4:
                    full_year = int(year_str)
                else:
                    continue  # Unexpected format
                years.add(full_year)

    return sorted(list(years))


def get_cell_value(sheet, cell: str) -> Optional[float]:
    """
    Retrieves and converts the value from a specific cell to float.
    Returns None if the cell is empty or contains non-numeric data.
    """
    value = sheet[cell].value  # data_only=True ensures this is the evaluated value if a formula is present
    if isinstance(value, (int, float)):
        return float(value)
    elif isinstance(value, str):
        try:
            # Remove any non-numeric characters, e.g., percentage signs
            value_clean = re.sub(r'[^\d\.\-]', '', value)
            return float(value_clean)
        except ValueError:
            return None
    else:
        return None



def extract_case_data(case_name: str, mappings: Dict[str, Dict[int, str]], sheet) -> CaseData:
    """
    Extracts data for a given case based on the cell mappings.
    """
    case_data = CaseData(name=case_name)

    for variable, year_cells in mappings.items():
        for year, cell in year_cells.items():
            value = get_cell_value(sheet, cell)
            if variable == 'Revenue':
                case_data.revenue[year] = value
            elif variable == 'EBITDA':
                case_data.ebitda[year] = value
            elif variable == 'EBITDA normalizations':
                case_data.ebitda_normalizations[year] = value
            elif variable == 'Depreciation':
                case_data.depreciation[year] = value
            elif variable == 'Amortization':
                case_data.amortization[year] = value
            elif variable == 'EBIT':
                case_data.ebit = {**case_data.ebit, year: value}
            elif variable == 'Maintenance Capex':
                case_data.maintenance_capex[year] = value
            elif variable == 'Expansion Capex':
                case_data.expansion_capex[year] = value
            # Continue mapping other variables to their respective fields
            # Add additional elif clauses for other variables
            elif variable == 'Inventory':
                case_data.inventory[year] = value
            elif variable == 'Accounts Receivable':
                case_data.accounts_receivable[year] = value
            elif variable == 'Accounts Payable':
                case_data.accounts_payable[year] = value
            elif variable == 'Other W/C Assets':
                case_data.other_wc_assets[year] = value
            elif variable == 'Other W/C Liabilities':
                case_data.other_wc_liabilities[year] = value
            elif variable == 'Provisions':
                case_data.provisions[year] = value
            elif variable == 'Revenue growth':
                case_data.revenue_growth[year] = value
            elif variable == 'EBITDA margin':
                case_data.ebitda_margin[year] = value
            elif variable == 'Depreciation as % of rev.':
                case_data.depreciation_percent[year] = value
            elif variable == 'Amortization as % of rev.':
                case_data.amortization_percent[year] = value
            elif variable == 'EBIT margin':
                case_data.ebit_margin[year] = value
            elif variable == 'M-Capex as % of rev.':
                case_data.m_capex_percent[year] = value
            elif variable == 'E-Capex as % of rev.':
                case_data.e_capex_percent[year] = value
            elif variable == 'Inventory as % of rev.':
                case_data.inventory_percent[year] = value
            elif variable == 'Accounts Receivable as % of rev.':
                case_data.accounts_receivable_percent[year] = value
            elif variable == 'Accounts Payable as % of rev.':
                case_data.accounts_payable_percent[year] = value
            elif variable == 'Other W/C Assets as % of rev.':
                case_data.other_wc_assets_percent[year] = value
            elif variable == 'Other W/C Liabilities as % of rev.':
                case_data.other_wc_liabilities_percent[year] = value
            elif variable == 'Provisions growth':
                case_data.provisions_growth[year] = value
            # Add more mappings as needed

    return case_data


def build_cases(cell_mappings: Dict[str, Dict[str, Dict[int, str]]], cases_sheet) -> Dict[str, CaseData]:
    """
    Builds a dictionary of CaseData objects for each case based on the cell mappings.
    """
    cases = {}
    for case_name, mappings in cell_mappings.items():
        case_data = extract_case_data(case_name, mappings, cases_sheet)
        cases[case_name] = case_data
    return cases

# Build all cases
all_cases = build_cases(cell_mappings, cases_sheet)

# Example: Access Revenue growth for the 'Sensitivity Case' in 2025
sensitivity_case_name = 'Sensitivity Case'
if sensitivity_case_name in all_cases:
    sensitivity_case = all_cases[sensitivity_case_name]
    revenue_growth_2025 = sensitivity_case.revenue_growth.get(2025)
    print(f"Revenue Growth for {sensitivity_case_name} in 2025: {revenue_growth_2025}%")
else:
    print(f"Case '{sensitivity_case_name}' not found.")

# Example: Iterate through all cases and print Revenue for each year
for case_name, case_data in all_cases.items():
    print(f"\nCase: {case_name}")
    for year, revenue in case_data.revenue.items():
        print(f"  {year}: {revenue} EURm")
