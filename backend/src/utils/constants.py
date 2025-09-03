"""
Application constants for tearsheet.
"""

# Portfolio constraints
MIN_PORTFOLIO_SIZE = 1
MAX_PORTFOLIO_SIZE = 10
MIN_WEIGHT = 0.0
MAX_WEIGHT = 1.0
WEIGHT_TOLERANCE = 0.0001

# Date format constants
DATE_FORMAT = "%Y-%m-%d"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
MAX_DATE_RANGE_DAYS = 3650  # Maximum 10 years

# Vietnam stock market constants
VN_MARKET_HOURS = {
    "morning_open": "09:00",
    "morning_close": "11:30",
    "afternoon_open": "13:00",
    "afternoon_close": "15:00",
}

# Financial ratio categories (inspired by ref/process.py patterns)
FINANCIAL_RATIO_CATEGORIES = [
    "liquidity",
    "profitability",
    "efficiency",
    "leverage",
    "valuation",
    "growth",
]

# vnstock data source options
VNSTOCK_SOURCES = ["VCI", "TCBS", "SSI"]
VNSTOCK_INTERVALS = ["1m", "5m", "15m", "30m", "1H", "1D", "1W", "1M"]

# Supported file formats
EXPORT_FORMATS = ["xlsx", "csv", "html", "pdf"]

# Error messages
ERROR_MESSAGES = {
    "INVALID_SYMBOL": "Invalid stock symbol provided",
    "INVALID_WEIGHT": "Portfolio weights must be between 0 and 1",
    "WEIGHTS_NOT_SUM_ONE": "Portfolio weights must sum to 1.0",
    "INVALID_DATE_FORMAT": "Date must be in YYYY-MM-DD format",
    "INVALID_DATE_RANGE": "Start date must be before end date",
    "DATA_FETCH_ERROR": "Failed to fetch stock data",
    "PORTFOLIO_TOO_LARGE": f"Portfolio cannot exceed {MAX_PORTFOLIO_SIZE} stocks",
    "NO_DATA_AVAILABLE": "No data available for the specified period",
}

# Success messages
SUCCESS_MESSAGES = {
    "DATA_FETCHED": "Stock data fetched successfully",
    "ANALYSIS_COMPLETE": "Portfolio analysis completed",
    "REPORT_GENERATED": "Tearsheet report generated successfully",
    "EXPORT_COMPLETE": "Data exported successfully",
}
