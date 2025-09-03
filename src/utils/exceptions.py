"""
Custom exception classes for tearsheet application.
"""


class TearsheetError(Exception):
    """Base exception class for tearsheet application."""

    def __init__(self, message: str, error_code: str = None):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)


class DataFetchError(TearsheetError):
    """Exception raised when data fetching fails."""

    pass


class ValidationError(TearsheetError):
    """Exception raised when input validation fails."""

    pass


class PortfolioError(TearsheetError):
    """Exception raised when portfolio validation fails."""

    pass


class ConfigurationError(TearsheetError):
    """Exception raised when configuration is invalid."""

    pass


class ExportError(TearsheetError):
    """Exception raised when file export fails."""

    pass


class AnalysisError(TearsheetError):
    """Exception raised when portfolio analysis fails."""

    pass


# Legacy compatibility with existing data_loader.py
class DataLoaderError(DataFetchError):
    """Legacy exception for backward compatibility."""

    pass
