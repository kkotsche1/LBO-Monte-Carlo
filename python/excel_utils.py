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

