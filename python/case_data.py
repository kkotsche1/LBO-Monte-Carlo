from dataclasses import dataclass, field
from typing import Dict


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


def extract_case_data(case_name: str, mappings: Dict[str, Dict[int, str]], sheet) -> CaseData:
    """
    Extracts data for a given case based on the cell mappings.
    """
    from excel_utils import get_cell_value
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
                case_data.ebit[year] = value
            elif variable == 'Maintenance Capex':
                case_data.maintenance_capex[year] = value
            elif variable == 'Expansion Capex':
                case_data.expansion_capex[year] = value
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
                case_data.depreciation_percent[year] = value  # Add this
            elif variable == 'Amortization as % of rev.':
                case_data.amortization_percent[year] = value  # Add this
            elif variable == 'EBIT margin':
                case_data.ebit_margin[year] = value
            elif variable == 'M-Capex as % of rev.':
                case_data.m_capex_percent[year] = value  # Add this
            elif variable == 'E-Capex as % of rev.':
                case_data.e_capex_percent[year] = value  # Add this
            elif variable == 'Inventory as % of rev.':
                case_data.inventory_percent[year] = value  # Add this
            elif variable == 'Accounts Receivable as % of rev.':
                case_data.accounts_receivable_percent[year] = value  # Add this
            elif variable == 'Accounts Payable as % of rev.':
                case_data.accounts_payable_percent[year] = value  # Add this
            elif variable == 'Other W/C Assets as % of rev.':
                case_data.other_wc_assets_percent[year] = value  # Add this
            elif variable == 'Other W/C Liabilities as % of rev.':
                case_data.other_wc_liabilities_percent[year] = value  # Add this
            elif variable == 'Provisions growth':
                case_data.provisions_growth[year] = value
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
