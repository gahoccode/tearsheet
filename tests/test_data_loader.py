"""
tests/test_data_loader.py
Unit tests for data_loader.py (fetch_historical_data, get_close_prices)
"""

import unittest
import pandas as pd
from data_loader import fetch_historical_data, get_close_prices, DataLoaderError

class TestDataLoader(unittest.TestCase):
    def test_fetch_valid_symbols(self):
        symbols = ['REE', 'FMC']
        df = fetch_historical_data(symbols, '2024-01-01', '2024-01-10')
        self.assertIsInstance(df, pd.DataFrame)
        self.assertIn('REE_close', df.columns)
        self.assertIn('FMC_close', df.columns)
        self.assertIn('time', df.columns)

    def test_fetch_invalid_symbol(self):
        symbols = ['INVALIDTICKER']
        with self.assertRaises(DataLoaderError):
            fetch_historical_data(symbols, '2024-01-01', '2024-01-10')

    def test_get_close_prices(self):
        symbols = ['REE', 'FMC']
        df = fetch_historical_data(symbols, '2024-01-01', '2024-01-10')
        close_df = get_close_prices(df, symbols)
        self.assertListEqual(list(close_df.columns), ['time', 'REE_close', 'FMC_close'])
        self.assertEqual(len(close_df), len(df))

    def test_get_close_prices_missing_column(self):
        # Simulate missing column
        df = pd.DataFrame({'time': ['2024-01-01'], 'REE_close': [100]})
        symbols = ['REE', 'FMC']
        with self.assertRaises(DataLoaderError):
            get_close_prices(df, symbols)

if __name__ == '__main__':
    unittest.main()
