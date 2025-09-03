"""
Base configuration settings for tearsheet application.
"""

import os
from pathlib import Path

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent


class BaseConfig:
    """Base configuration class with common settings."""

    # Flask settings
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-key-change-in-production")

    # Application settings
    APP_NAME = "tearsheet"
    APP_VERSION = "0.1.0"

    # Data settings
    DEFAULT_START_DATE = "2024-01-01"
    DEFAULT_END_DATE = "2024-12-31"
    DEFAULT_CAPITAL = 10000000  # 10M VND

    # vnstock settings
    DEFAULT_INTERVAL = "1D"
    DEFAULT_SOURCE = "VCI"
    SUPPORTED_SYMBOLS = [
        "REE",
        "FMC",
        "DHC",
        "VNM",
        "VIC",
        "ACB",
        "TCB",
        "CTG",
        "BID",
        "VCB",
    ]

    # File paths
    STATIC_DIR = PROJECT_ROOT / "static"
    REPORTS_DIR = STATIC_DIR / "reports"
    TEMPLATES_DIR = PROJECT_ROOT / "templates"

    # Export settings
    EXCEL_EXPORT_FORMAT = "xlsx"
    HTML_REPORT_NAME = "quantstats-results.html"

    # Performance settings
    MAX_PORTFOLIO_SIZE = 10
    MAX_DATE_RANGE_DAYS = 365 * 3  # 3 years max

    # Matplotlib settings
    MATPLOTLIB_BACKEND = "Agg"
    MATPLOTLIB_FONT = "DejaVu Sans"

    @classmethod
    def init_app(cls, app):
        """Initialize application with this configuration."""
        # Ensure required directories exist
        cls.REPORTS_DIR.mkdir(parents=True, exist_ok=True)

        # Set matplotlib backend
        import matplotlib

        matplotlib.use(cls.MATPLOTLIB_BACKEND)
        matplotlib.rcParams["font.family"] = cls.MATPLOTLIB_FONT
