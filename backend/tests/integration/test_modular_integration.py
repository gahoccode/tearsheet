"""
Integration tests for the modular architecture.
"""

import unittest
import pandas as pd
from unittest.mock import patch, MagicMock

from src.core.data_fetcher import DataFetcher
from src.core.portfolio_analyzer import PortfolioAnalyzer
from src.services.validation_service import ValidationService
from src.models.portfolio import Portfolio, Stock


class TestModularIntegration(unittest.TestCase):
    """Integration tests for the modular tearsheet system."""

    def setUp(self):
        """Set up test fixtures."""
        self.validator = ValidationService()
        self.data_fetcher = DataFetcher()
        self.analyzer = PortfolioAnalyzer()

        # Sample portfolio data
        self.symbols = ["REE", "FMC", "DHC"]
        self.weights = ["0.5", "0.3", "0.2"]
        self.capital = "10000000"
        self.start_date = "2024-01-01"
        self.end_date = "2024-06-30"

    def test_end_to_end_portfolio_validation_and_creation(self):
        """Test complete portfolio validation and model creation."""
        # Validate form data
        validated_data = self.validator.validate_portfolio_form(
            self.symbols, self.weights, self.capital, self.start_date, self.end_date
        )

        # Create portfolio model
        portfolio = Portfolio.from_form_data(
            symbols=validated_data["symbols"],
            weights=[str(w) for w in validated_data["weights"]],
            capital=str(validated_data["capital"]),
            start_date=validated_data["start_date"],
            end_date=validated_data["end_date"],
        )

        # Verify portfolio
        self.assertEqual(len(portfolio.stocks), 3)
        self.assertAlmostEqual(sum(portfolio.weights), 1.0, places=10)
        self.assertEqual(portfolio.capital, 10000000)

        # Test portfolio dictionary conversion
        portfolio_dict = portfolio.to_dict()
        self.assertIn("stocks", portfolio_dict)
        self.assertIn("summary", portfolio_dict)

    @patch("vnstock.Quote")
    def test_data_fetching_and_analysis_integration(self, mock_quote):
        """Test integration between data fetching and portfolio analysis."""
        # Mock vnstock response
        mock_data = pd.DataFrame(
            {
                "time": pd.date_range("2024-01-01", periods=10, freq="D"),
                "close": [50 + i for i in range(10)],
                "open": [49 + i for i in range(10)],
                "high": [51 + i for i in range(10)],
                "low": [48 + i for i in range(10)],
                "volume": [1000 for _ in range(10)],
            }
        )

        mock_quote_instance = MagicMock()
        mock_quote_instance.history.return_value = mock_data
        mock_quote.return_value = mock_quote_instance

        # Fetch historical data
        combined_data = self.data_fetcher.fetch_historical_data(
            self.symbols, self.start_date, self.end_date
        )

        # Extract close prices
        close_prices = self.data_fetcher.get_close_prices(combined_data, self.symbols)

        # Analyze portfolio
        float_weights = [float(w) for w in self.weights]
        portfolio_returns = self.analyzer.calculate_portfolio_returns(
            close_prices, self.symbols, float_weights
        )

        # Verify integration
        self.assertIsInstance(portfolio_returns, pd.Series)
        self.assertGreater(len(portfolio_returns), 0)

        # Calculate metrics
        metrics = self.analyzer.calculate_performance_metrics(portfolio_returns)
        self.assertIn("total_return", metrics)
        self.assertIn("volatility", metrics)

    def test_portfolio_model_validation_integration(self):
        """Test portfolio model validation with various edge cases."""
        # Test valid portfolio creation
        stocks = [
            Stock(symbol="REE", weight=0.5),
            Stock(symbol="FMC", weight=0.3),
            Stock(symbol="DHC", weight=0.2),
        ]

        portfolio = Portfolio(
            stocks=stocks,
            capital=10000000,
            start_date="2024-01-01",
            end_date="2024-06-30",
        )

        self.assertEqual(portfolio.size, 3)
        self.assertEqual(portfolio.symbols, ["REE", "FMC", "DHC"])

        # Test allocation calculation
        allocation = portfolio.get_stock_allocation()
        expected_allocation = {"REE": 5000000, "FMC": 3000000, "DHC": 2000000}
        self.assertEqual(allocation, expected_allocation)

    def test_validation_error_handling(self):
        """Test error handling across validation layers."""
        # Test invalid weights
        with self.assertRaises(Exception):  # ValidationError or PortfolioError
            invalid_weights = ["0.5", "0.6", "0.2"]  # Sum > 1
            self.validator.validate_portfolio_form(
                self.symbols,
                invalid_weights,
                self.capital,
                self.start_date,
                self.end_date,
            )

        # Test invalid dates
        with self.assertRaises(Exception):  # ValidationError
            self.validator.validate_portfolio_form(
                self.symbols,
                self.weights,
                self.capital,
                "2024-12-31",
                "2024-01-01",  # Start after end
            )

        # Test invalid capital
        with self.assertRaises(Exception):  # ValidationError
            self.validator.validate_portfolio_form(
                self.symbols,
                self.weights,
                "-1000",  # Negative
                self.start_date,
                self.end_date,
            )

    def test_modular_component_isolation(self):
        """Test that modular components can work independently."""
        # Validation service works independently
        validated_symbols = self.validator.validate_symbols(["REE", "fmc", " DHC "])
        self.assertEqual(validated_symbols, ["REE", "FMC", "DHC"])

        # Portfolio analyzer validation works independently
        analyzer_result = self.analyzer.validate_portfolio(
            ["REE", "FMC", "DHC"], [0.5, 0.3, 0.2], 10000000
        )
        self.assertEqual(analyzer_result["size"], 3)

        # Data fetcher can be initialized independently
        fetcher = DataFetcher(source="VCI", default_interval="1D")
        self.assertEqual(fetcher.source, "VCI")
        self.assertEqual(fetcher.default_interval, "1D")


if __name__ == "__main__":
    unittest.main()
