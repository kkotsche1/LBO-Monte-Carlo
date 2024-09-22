# excel_utils.py

import re
from typing import Optional, Dict
from openpyxl import worksheet

def get_cell_value(sheet: worksheet, cell: str) -> Optional[float]:
    """
    Retrieves and converts the value from a specific cell to float.
    Returns None if the cell is empty or contains non-numeric data.
    """
    value = sheet[cell].value
    if isinstance(value, (int, float)):
        return float(value)
    elif isinstance(value, str):
        try:
            value_clean = re.sub(r'[^\d\.\-]', '', value)  # Remove non-numeric characters
            return float(value_clean)
        except ValueError:
            return None
    return None

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
