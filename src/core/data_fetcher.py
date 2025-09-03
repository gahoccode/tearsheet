"""
Enhanced data fetching capabilities for tearsheet application.

This module provides comprehensive data fetching from vnstock,
including historical price data and financial ratios.
"""

from typing import List, Dict, Optional
import pandas as pd
import logging
from vnstock import Quote

from ..utils.exceptions import DataFetchError
from ..utils.constants import (
    VNSTOCK_SOURCES,
    VNSTOCK_INTERVALS,
    ERROR_MESSAGES,
)

logger = logging.getLogger(__name__)


class DataFetcher:
    """
    Enhanced data fetcher supporting both price data and financial ratios.
    """

    def __init__(self, source: str = "VCI", default_interval: str = "1D"):
        """
        Initialize data fetcher with default source and interval.

        Args:
            source: Data source for vnstock (VCI, TCBS, SSI)
            default_interval: Default time interval for data
        """
        if source not in VNSTOCK_SOURCES:
            raise DataFetchError(
                f"Unsupported source: {source}. Use one of {VNSTOCK_SOURCES}"
            )

        if default_interval not in VNSTOCK_INTERVALS:
            raise DataFetchError(
                f"Unsupported interval: {default_interval}. Use one of {VNSTOCK_INTERVALS}"
            )

        self.source = source
        self.default_interval = default_interval
        logger.info(
            f"DataFetcher initialized with source={source}, interval={default_interval}"
        )

    def fetch_historical_data(
        self,
        symbols: List[str],
        start_date: str,
        end_date: str,
        interval: Optional[str] = None,
    ) -> pd.DataFrame:
        """
        Fetch and merge historical price data for multiple symbols.

        Args:
            symbols: List of stock tickers
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            interval: Data interval (defaults to instance default)

        Returns:
            Combined DataFrame with columns prefixed by symbol

        Raises:
            DataFetchError: If no data could be fetched for any symbol
        """
        interval = interval or self.default_interval

        if not symbols:
            raise DataFetchError("No symbols provided")

        logger.info(f"Fetching historical data for {len(symbols)} symbols: {symbols}")
        logger.info(f"Period: {start_date} to {end_date}, interval: {interval}")

        all_historical_data: Dict[str, pd.DataFrame] = {}

        for symbol in symbols:
            try:
                quote = Quote(symbol=symbol)
                data = quote.history(
                    start=start_date, end=end_date, interval=interval, to_df=True
                )

                if not data.empty:
                    all_historical_data[symbol] = data
                    logger.debug(f"Fetched {len(data)} records for {symbol}")
                else:
                    logger.warning(f"No data available for symbol {symbol}")

            except Exception as e:
                logger.error(f"Error fetching data for {symbol}: {e}")
                continue

        if not all_historical_data:
            raise DataFetchError(ERROR_MESSAGES["NO_DATA_AVAILABLE"])

        # Merge all data on 'time', prefix columns with symbol
        combined_data = self._merge_symbol_data(all_historical_data)

        logger.info(f"Successfully fetched data for {len(all_historical_data)} symbols")
        return combined_data

    def get_close_prices(
        self, combined_data: pd.DataFrame, symbols: List[str]
    ) -> pd.DataFrame:
        """
        Extract close prices for each symbol from combined DataFrame.

        Args:
            combined_data: Output of fetch_historical_data
            symbols: List of stock tickers

        Returns:
            DataFrame with 'time' and one column per symbol's close price

        Raises:
            DataFetchError: If required columns are missing
        """
        close_cols = ["time"] + [f"{symbol}_close" for symbol in symbols]
        missing_cols = [col for col in close_cols if col not in combined_data.columns]

        if missing_cols:
            raise DataFetchError(f"Missing columns in combined data: {missing_cols}")

        result = combined_data[close_cols].copy()
        logger.debug(f"Extracted close prices for {len(symbols)} symbols")

        return result

    def _merge_symbol_data(self, symbol_data: Dict[str, pd.DataFrame]) -> pd.DataFrame:
        """
        Merge data from multiple symbols with column prefixing.

        Args:
            symbol_data: Dictionary mapping symbol to its DataFrame

        Returns:
            Combined DataFrame with prefixed columns
        """
        combined_data = pd.DataFrame()

        for symbol, data in symbol_data.items():
            temp_df = data.copy()

            # Prefix all columns except 'time'
            for col in temp_df.columns:
                if col != "time":
                    temp_df.rename(columns={col: f"{symbol}_{col}"}, inplace=True)

            if combined_data.empty:
                combined_data = temp_df
            else:
                combined_data = pd.merge(combined_data, temp_df, on="time", how="outer")

        # Sort by time and reset index
        combined_data = combined_data.sort_values("time").reset_index(drop=True)

        return combined_data


# Legacy compatibility functions for backward compatibility
def fetch_historical_data(
    symbols: List[str], start_date: str, end_date: str, interval: str = "1D"
) -> pd.DataFrame:
    """Legacy function for backward compatibility with existing code."""
    fetcher = DataFetcher()
    return fetcher.fetch_historical_data(symbols, start_date, end_date, interval)


def get_close_prices(combined_data: pd.DataFrame, symbols: List[str]) -> pd.DataFrame:
    """Legacy function for backward compatibility with existing code."""
    fetcher = DataFetcher()
    return fetcher.get_close_prices(combined_data, symbols)


# Legacy exception for backward compatibility
class DataLoaderError(DataFetchError):
    """Legacy exception for backward compatibility."""

    pass
