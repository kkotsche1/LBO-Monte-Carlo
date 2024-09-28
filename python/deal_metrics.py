from excel_utils import get_cell_value
from typing import Optional, Dict
from openpyxl import worksheet


def extract_exit_metrics_by_columns(sheet: worksheet, period_column_map: Dict[str, str]) -> Dict[str, Dict[str, float]]:
    """
    Extract exit metrics dynamically for each period based on the column location in the Excel sheet.
    period_column_map: A dictionary mapping periods (e.g., "Entry + 3yrs") to column letters (e.g., "G").
    """
    exit_metrics = {}

    for period, column in period_column_map.items():
        period_data = {}

        # Example cell extraction for the period
        period_data['Exit Multiple'] = get_cell_value(sheet, f'{column}31')
        period_data['Enterprise Value Exit'] = get_cell_value(sheet, f'{column}32')
        period_data['Net Debt Exit'] = get_cell_value(sheet, f'{column}33')
        period_data['Equity Value Exit'] = get_cell_value(sheet, f'{column}35')
        period_data['MoM'] = get_cell_value(sheet, f'{column}43')
        period_data['IRR'] = get_cell_value(sheet, f'{column}44')

        exit_metrics[period] = period_data

    return exit_metrics

def extract_expanded_deal_metrics(sheet) -> dict:
    """
    Extracts various deal metrics including debt, equity, transaction costs, valuation, and exit metrics.
    """
    deal_metrics = {}
    ZQWL = "ZQWL"  # Replace all occurrences of "GHPE" with "ZQWL".

    # Debt Information
    deal_metrics['Senior A Amount'] = get_cell_value(sheet, 'U15')
    deal_metrics['Senior A Interest'] = get_cell_value(sheet, 'X15')
    deal_metrics['Senior B Amount'] = get_cell_value(sheet, 'U16')
    deal_metrics['Senior B Interest'] = get_cell_value(sheet, 'X16')

    # Subordinate/Mezzanine Debt
    deal_metrics["Subordinate Amount"] = get_cell_value(sheet, 'U19')
    deal_metrics['Subordinate Interest'] = get_cell_value(sheet, 'X19')
    deal_metrics['Mezzanine Cash Amount'] = get_cell_value(sheet, 'U20')
    deal_metrics['Mezzanine Cash Interest'] = get_cell_value(sheet, 'X20')

    # Revolving Credit Facility (RCF)
    deal_metrics['RCF Amount'] = get_cell_value(sheet, 'U24')
    deal_metrics['RCF Interest'] = get_cell_value(sheet, 'X24')
    deal_metrics['RCF Undrawn Interest'] = get_cell_value(sheet, 'X25')

    # Equity Contributions
    deal_metrics[f'{ZQWL} Equity'] = get_cell_value(sheet, 'D25')
    deal_metrics['Co-Invest'] = get_cell_value(sheet, 'D24')
    deal_metrics['MPP'] = get_cell_value(sheet, 'D23')

    # Transaction Costs
    deal_metrics['Net Debt at Closing'] = get_cell_value(sheet, 'J20')
    deal_metrics['Restricted Cash & Overfunding'] = get_cell_value(sheet, 'J22')

    # Valuation Metrics
    deal_metrics['Entry Multiple'] = get_cell_value(sheet, 'P16')
    deal_metrics['Enterprise Value Entry'] = get_cell_value(sheet, 'P17')

    # Include exit metrics by period
    period_column_map = {"Entry + 3yrs": "U", "Entry + 4yrs": "V", "Entry + 5yrs": "W", "Entry + 6yrs": "X"}
    deal_metrics['Exit Metrics by Period'] = extract_exit_metrics_by_columns(sheet, period_column_map)

    return deal_metrics
