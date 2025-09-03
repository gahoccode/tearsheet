"""
data_loader.py
Module for loading and merging historical stock price data using vnstock.
Follows modular, testable, and robust design per project standards.
"""

from typing import List, Dict
import pandas as pd
from vnstock import Quote
import logging


class DataLoaderError(Exception):
    """Custom exception for data loader errors."""

    pass


def fetch_historical_data(
    symbols: List[str], start_date: str, end_date: str, interval: str = "1D"
) -> pd.DataFrame:
    """
    Fetch and merge historical price data for multiple symbols using vnstock.

    Args:
        symbols (List[str]): List of stock tickers.
        start_date (str): Start date (YYYY-MM-DD).
        end_date (str): End date (YYYY-MM-DD).
        interval (str): Data interval (default '1D').

    Returns:
        pd.DataFrame: Combined DataFrame with columns prefixed by symbol.

    Raises:
        DataLoaderError: If no data could be fetched for any symbol.

    Example:
        >>> fetch_historical_data(['REE', 'FMC'], '2024-01-01', '2024-03-19')
    """
    all_historical_data: Dict[str, pd.DataFrame] = {}
    for symbol in symbols:
        try:
            quote = Quote(symbol=symbol)
            data = quote.history(
                start=start_date, end=end_date, interval=interval, to_df=True
            )
            if not data.empty:
                all_historical_data[symbol] = data
            else:
                logging.warning(f"No data for symbol {symbol}")
        except Exception as e:
            logging.error(f"Error fetching data for {symbol}: {e}")
    if not all_historical_data:
        raise DataLoaderError("No historical data fetched for any symbol.")
    # Merge all data on 'time', prefix columns with symbol
    combined_data = pd.DataFrame()
    for symbol, data in all_historical_data.items():
        temp_df = data.copy()
        for col in temp_df.columns:
            if col != "time":
                temp_df.rename(columns={col: f"{symbol}_{col}"}, inplace=True)
        if combined_data.empty:
            combined_data = temp_df
        else:
            combined_data = pd.merge(combined_data, temp_df, on="time", how="outer")
    combined_data = combined_data.sort_values("time").reset_index(drop=True)
    return combined_data


def get_close_prices(combined_data: pd.DataFrame, symbols: List[str]) -> pd.DataFrame:
    """
    Extract close prices for each symbol from combined DataFrame.

    Args:
        combined_data (pd.DataFrame): Output of fetch_historical_data.
        symbols (List[str]): List of stock tickers.

    Returns:
        pd.DataFrame: DataFrame with 'time' and one column per symbol's close price.

    Example:
        >>> get_close_prices(combined_data, ['REE', 'FMC'])
    """
    close_cols = ["time"] + [f"{symbol}_close" for symbol in symbols]
    missing_cols = [col for col in close_cols if col not in combined_data.columns]
    if missing_cols:
        raise DataLoaderError(f"Missing columns in combined data: {missing_cols}")
    return combined_data[close_cols].copy()
