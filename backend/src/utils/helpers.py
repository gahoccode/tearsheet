"""
Common helper functions and utilities.
"""

import pandas as pd
import logging
from typing import Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


def setup_logging(level: str = "INFO", log_file: Optional[str] = None) -> None:
    """
    Set up application logging.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR)
        log_file: Optional log file path
    """
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(log_file) if log_file else logging.NullHandler(),
        ],
    )

    logger.info(f"Logging configured at {level} level")


def format_currency(amount: float, currency: str = "VND") -> str:
    """
    Format currency amount for display.

    Args:
        amount: Numeric amount
        currency: Currency symbol

    Returns:
        Formatted currency string
    """
    if currency == "VND":
        return f"{amount:,.0f} {currency}"
    else:
        return f"{amount:,.2f} {currency}"


def format_percentage(value: float, decimal_places: int = 2) -> str:
    """
    Format percentage for display.

    Args:
        value: Decimal value (e.g., 0.05 for 5%)
        decimal_places: Number of decimal places

    Returns:
        Formatted percentage string
    """
    return f"{value * 100:.{decimal_places}f}%"


def calculate_date_range_days(start_date: str, end_date: str) -> int:
    """
    Calculate number of days between two dates.

    Args:
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD)

    Returns:
        Number of days
    """
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    return (end - start).days


def get_business_days(start_date: str, end_date: str) -> int:
    """
    Calculate number of business days between two dates.

    Args:
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD)

    Returns:
        Number of business days
    """
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    return pd.bdate_range(start, end).size


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """
    Safely divide two numbers, returning default if denominator is zero.

    Args:
        numerator: Numerator value
        denominator: Denominator value
        default: Default value if division by zero

    Returns:
        Division result or default value
    """
    try:
        if denominator == 0:
            return default
        return numerator / denominator
    except (TypeError, ZeroDivisionError):
        return default


def flatten_dict(
    data: Dict[str, Any], separator: str = "_", parent_key: str = ""
) -> Dict[str, Any]:
    """
    Flatten nested dictionary structure.

    Args:
        data: Nested dictionary
        separator: Separator for flattened keys
        parent_key: Parent key prefix

    Returns:
        Flattened dictionary
    """
    items = []

    for key, value in data.items():
        new_key = f"{parent_key}{separator}{key}" if parent_key else key

        if isinstance(value, dict):
            items.extend(flatten_dict(value, separator, new_key).items())
        else:
            items.append((new_key, value))

    return dict(items)


def create_summary_stats(data: pd.Series) -> Dict[str, float]:
    """
    Create summary statistics for a data series.

    Args:
        data: Pandas Series with numeric data

    Returns:
        Dictionary with summary statistics
    """
    if data.empty:
        return {}

    return {
        "count": len(data),
        "mean": data.mean(),
        "std": data.std(),
        "min": data.min(),
        "max": data.max(),
        "median": data.median(),
        "q25": data.quantile(0.25),
        "q75": data.quantile(0.75),
        "skewness": data.skew(),
        "kurtosis": data.kurtosis(),
    }


def validate_dataframe_columns(df: pd.DataFrame, required_columns: list) -> bool:
    """
    Validate that DataFrame contains required columns.

    Args:
        df: DataFrame to validate
        required_columns: List of required column names

    Returns:
        True if all columns present, False otherwise
    """
    missing_columns = set(required_columns) - set(df.columns)

    if missing_columns:
        logger.warning(f"Missing columns: {missing_columns}")
        return False

    return True


def clean_symbol(symbol: str) -> str:
    """
    Clean and standardize stock symbol.

    Args:
        symbol: Raw stock symbol

    Returns:
        Cleaned symbol
    """
    if not symbol:
        return ""

    # Remove whitespace and convert to uppercase
    cleaned = symbol.strip().upper()

    # Remove any non-alphabetic characters
    import re

    cleaned = re.sub(r"[^A-Z]", "", cleaned)

    return cleaned


def get_current_timestamp() -> str:
    """
    Get current timestamp in ISO format.

    Returns:
        ISO formatted timestamp string
    """
    return datetime.now().isoformat()


def convert_to_json_serializable(obj: Any) -> Any:
    """
    Convert object to JSON serializable format.

    Args:
        obj: Object to convert

    Returns:
        JSON serializable object
    """
    if isinstance(obj, pd.Timestamp):
        return obj.isoformat()
    elif isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, pd.Series):
        return obj.to_dict()
    elif isinstance(obj, pd.DataFrame):
        return obj.to_dict("records")
    elif hasattr(obj, "to_dict"):
        return obj.to_dict()
    else:
        return obj


def chunk_list(lst: list, chunk_size: int) -> list:
    """
    Split list into chunks of specified size.

    Args:
        lst: List to chunk
        chunk_size: Size of each chunk

    Returns:
        List of chunks
    """
    return [lst[i : i + chunk_size] for i in range(0, len(lst), chunk_size)]


def merge_dicts(*dicts: Dict) -> Dict:
    """
    Merge multiple dictionaries, with later ones taking precedence.

    Args:
        *dicts: Variable number of dictionaries

    Returns:
        Merged dictionary
    """
    result = {}
    for d in dicts:
        if d:
            result.update(d)
    return result
