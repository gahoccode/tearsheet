"""
Advanced vnstock service for comprehensive Vietnam stock market data.

This service provides both historical price data and financial ratios,
inspired by the patterns shown in ref/process.py for enhanced analysis capabilities.
"""

from typing import List, Dict, Optional
import pandas as pd
import logging
from vnstock import Vnstock
from vnstock.core.utils.transform import flatten_hierarchical_index

from ..utils.exceptions import DataFetchError
from ..utils.constants import (
    VNSTOCK_SOURCES,
)

logger = logging.getLogger(__name__)


class VnstockService:
    """
    Advanced vnstock service supporting price data and financial ratios.

    This service combines the basic price data fetching with advanced
    financial ratio analysis capabilities.
    """

    def __init__(self, source: str = "VCI", lang: str = "vi"):
        """
        Initialize vnstock service with advanced capabilities.

        Args:
            source: Data source (VCI, TCBS, SSI)
            lang: Language for ratio data ('vi' or 'en')
        """
        if source not in VNSTOCK_SOURCES:
            raise DataFetchError(f"Unsupported source: {source}")

        self.source = source
        self.lang = lang
        logger.info(f"VnstockService initialized with source={source}, lang={lang}")

    def get_stock_instance(self, symbol: str) -> any:
        """
        Get vnstock Stock instance for a symbol.

        Args:
            symbol: Stock symbol

        Returns:
            Vnstock Stock instance
        """
        try:
            stock = Vnstock().stock(symbol=symbol, source=self.source)
            logger.debug(
                f"Created stock instance for {symbol} with source {self.source}"
            )
            return stock
        except Exception as e:
            raise DataFetchError(
                f"Failed to create stock instance for {symbol}: {str(e)}"
            )

    def fetch_financial_ratios(
        self, symbol: str, period: str = "year", dropna: bool = True
    ) -> pd.DataFrame:
        """
        Fetch comprehensive financial ratios for a stock symbol.

        Inspired by ref/process.py pattern for advanced financial analysis.

        Args:
            symbol: Stock symbol
            period: Time period ('year', 'quarter')
            dropna: Whether to drop NA values

        Returns:
            DataFrame with financial ratios (flattened from MultiIndex)

        Raises:
            DataFetchError: If ratio fetching fails
        """
        try:
            logger.info(f"Fetching financial ratios for {symbol}")

            # Get stock instance
            stock = self.get_stock_instance(symbol)

            # Fetch ratios using the pattern from ref/process.py
            ratios = stock.finance.ratio(period=period, lang=self.lang, dropna=dropna)

            if ratios.empty:
                logger.warning(f"No financial ratio data for {symbol}")
                return pd.DataFrame()

            # Flatten hierarchical index (inspired by ref/process.py)
            flattened_ratios = self._flatten_ratio_data(ratios, symbol)

            logger.info(
                f"Successfully fetched {len(flattened_ratios.columns)} ratio metrics for {symbol}"
            )
            return flattened_ratios

        except Exception as e:
            logger.error(f"Error fetching financial ratios for {symbol}: {e}")
            raise DataFetchError(
                f"Failed to fetch financial ratios for {symbol}: {str(e)}"
            )

    def fetch_multiple_ratios(
        self, symbols: List[str], period: str = "year", dropna: bool = True
    ) -> Dict[str, pd.DataFrame]:
        """
        Fetch financial ratios for multiple symbols.

        Args:
            symbols: List of stock symbols
            period: Time period ('year', 'quarter')
            dropna: Whether to drop NA values

        Returns:
            Dictionary mapping symbol to its ratio DataFrame
        """
        logger.info(f"Fetching financial ratios for {len(symbols)} symbols")

        ratio_data = {}

        for symbol in symbols:
            try:
                ratios = self.fetch_financial_ratios(symbol, period, dropna)
                if not ratios.empty:
                    ratio_data[symbol] = ratios
                else:
                    logger.warning(f"No ratio data for {symbol}")
            except Exception as e:
                logger.error(f"Failed to fetch ratios for {symbol}: {e}")
                continue

        logger.info(
            f"Successfully fetched ratios for {len(ratio_data)} out of {len(symbols)} symbols"
        )
        return ratio_data

    def get_fundamental_summary(
        self, symbols: List[str], metrics: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        Get fundamental analysis summary for multiple symbols.

        Args:
            symbols: List of stock symbols
            metrics: Specific metrics to include (if None, uses common ratios)

        Returns:
            DataFrame with fundamental metrics comparison
        """
        if metrics is None:
            # Common fundamental metrics
            metrics = [
                "pe_ratio",
                "pb_ratio",
                "roe",
                "roa",
                "debt_to_equity",
                "current_ratio",
                "quick_ratio",
                "gross_margin",
                "net_margin",
            ]

        logger.info(f"Creating fundamental summary for {len(symbols)} symbols")

        summary_data = []

        for symbol in symbols:
            try:
                ratios = self.fetch_financial_ratios(symbol)
                if ratios.empty:
                    continue

                # Extract latest values for each metric
                symbol_metrics = {"symbol": symbol}

                for metric in metrics:
                    # Try to find the metric in various possible column names
                    matching_cols = [
                        col for col in ratios.columns if metric.lower() in col.lower()
                    ]

                    if matching_cols:
                        # Use the most recent value
                        latest_value = (
                            ratios[matching_cols[0]].dropna().iloc[-1]
                            if not ratios[matching_cols[0]].dropna().empty
                            else None
                        )
                        symbol_metrics[metric] = latest_value
                    else:
                        symbol_metrics[metric] = None

                summary_data.append(symbol_metrics)

            except Exception as e:
                logger.warning(f"Could not get fundamental data for {symbol}: {e}")
                continue

        if not summary_data:
            logger.warning("No fundamental data available for any symbol")
            return pd.DataFrame()

        summary_df = pd.DataFrame(summary_data)
        logger.info(f"Fundamental summary created with {len(summary_df)} stocks")

        return summary_df

    def _flatten_ratio_data(self, ratios: pd.DataFrame, symbol: str) -> pd.DataFrame:
        """
        Flatten hierarchical ratio data using vnstock transform utilities.

        Applies the pattern from ref/process.py for data transformation.

        Args:
            ratios: Raw ratio data with possible MultiIndex
            symbol: Stock symbol for logging

        Returns:
            Flattened DataFrame
        """
        try:
            # Check if DataFrame has MultiIndex columns
            if isinstance(ratios.columns, pd.MultiIndex):
                logger.debug(f"Flattening MultiIndex columns for {symbol}")

                # Apply flatten_hierarchical_index from vnstock utilities
                # (pattern inspired by ref/process.py)
                flattened_df = flatten_hierarchical_index(
                    ratios, separator="_", handle_duplicates=True, drop_levels=0
                )

                logger.debug(
                    f"Flattened {len(ratios.columns)} to {len(flattened_df.columns)} columns"
                )
                return flattened_df
            else:
                # Already flat
                logger.debug(f"Data for {symbol} already has flat columns")
                return ratios

        except Exception as e:
            logger.warning(f"Could not flatten ratio data for {symbol}: {e}")
            return ratios

    def export_ratios_to_excel(
        self, ratio_data: Dict[str, pd.DataFrame], filename: str
    ) -> str:
        """
        Export financial ratios to Excel file.

        Inspired by the export pattern in ref/process.py.

        Args:
            ratio_data: Dictionary mapping symbol to ratio DataFrame
            filename: Output filename (without extension)

        Returns:
            Full path to exported file
        """
        try:
            from pathlib import Path

            output_path = Path(f"{filename}.xlsx")

            logger.info(f"Exporting ratio data to {output_path}")

            with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
                # Export each symbol's data to separate sheet
                for symbol, data in ratio_data.items():
                    if not data.empty:
                        data.to_excel(writer, sheet_name=symbol, index=True)
                        logger.debug(f"Exported {len(data)} rows for {symbol}")

                # Create summary sheet if multiple symbols
                if len(ratio_data) > 1:
                    summary = self.get_fundamental_summary(list(ratio_data.keys()))
                    if not summary.empty:
                        summary.to_excel(writer, sheet_name="Summary", index=False)
                        logger.debug("Created summary sheet")

            logger.info(f"Successfully exported ratio data to {output_path}")
            return str(output_path)

        except Exception as e:
            raise DataFetchError(f"Failed to export ratio data: {str(e)}")

    def get_stock_overview(self, symbol: str) -> Dict[str, any]:
        """
        Get comprehensive stock overview including basic info and key ratios.

        Args:
            symbol: Stock symbol

        Returns:
            Dictionary with stock overview data
        """
        try:
            logger.info(f"Getting stock overview for {symbol}")

            # Get financial ratios
            ratios = self.fetch_financial_ratios(symbol)

            # Extract key metrics
            overview = {
                "symbol": symbol,
                "source": self.source,
                "has_ratio_data": not ratios.empty,
                "ratio_periods": len(ratios) if not ratios.empty else 0,
                "available_metrics": list(ratios.columns) if not ratios.empty else [],
                "data_timestamp": pd.Timestamp.now(),
            }

            logger.info(f"Stock overview created for {symbol}")
            return overview

        except Exception as e:
            logger.error(f"Error creating stock overview for {symbol}: {e}")
            raise DataFetchError(
                f"Failed to create stock overview for {symbol}: {str(e)}"
            )
