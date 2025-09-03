"""
Unit tests for portfolio analyzer.
"""

import unittest
import pandas as pd
import numpy as np

from src.core.portfolio_analyzer import PortfolioAnalyzer
from src.utils.exceptions import PortfolioError, AnalysisError


class TestPortfolioAnalyzer(unittest.TestCase):
    """Test cases for PortfolioAnalyzer class."""

    def setUp(self):
        """Set up test fixtures."""
        self.analyzer = PortfolioAnalyzer()

        # Sample data
        self.symbols = ["REE", "FMC", "DHC"]
        self.weights = [0.5, 0.3, 0.2]
        self.capital = 10000000

        # Create sample price data
        dates = pd.date_range("2024-01-01", periods=10, freq="D")
        self.price_data = pd.DataFrame(
            {
                "REE_close": np.random.rand(10) * 100 + 50,
                "FMC_close": np.random.rand(10) * 80 + 40,
                "DHC_close": np.random.rand(10) * 60 + 30,
            },
            index=dates,
        )

    def test_validate_portfolio_success(self):
        """Test successful portfolio validation."""
        result = self.analyzer.validate_portfolio(
            self.symbols, self.weights, self.capital
        )

        self.assertEqual(result["symbols"], self.symbols)
        self.assertAlmostEqual(sum(result["weights"]), 1.0, places=10)
        self.assertEqual(result["capital"], self.capital)
        self.assertEqual(result["size"], len(self.symbols))

    def test_validate_portfolio_empty_symbols(self):
        """Test validation with empty symbols."""
        with self.assertRaises(PortfolioError):
            self.analyzer.validate_portfolio([], self.weights, self.capital)

    def test_validate_portfolio_mismatched_lengths(self):
        """Test validation with mismatched symbol/weight lengths."""
        with self.assertRaises(PortfolioError):
            self.analyzer.validate_portfolio(self.symbols, [0.5, 0.5], self.capital)

    def test_validate_portfolio_invalid_weights(self):
        """Test validation with invalid weights."""
        with self.assertRaises(PortfolioError):
            self.analyzer.validate_portfolio(
                self.symbols,
                [0.5, 0.3, 0.3],
                self.capital,  # Sum > 1
            )

    def test_validate_portfolio_negative_capital(self):
        """Test validation with negative capital."""
        with self.assertRaises(PortfolioError):
            self.analyzer.validate_portfolio(self.symbols, self.weights, -1000)

    def test_calculate_portfolio_returns(self):
        """Test portfolio returns calculation."""
        returns = self.analyzer.calculate_portfolio_returns(
            self.price_data, self.symbols, self.weights
        )

        self.assertIsInstance(returns, pd.Series)
        self.assertEqual(
            len(returns), len(self.price_data) - 1
        )  # First row dropped for returns
        self.assertEqual(returns.name, "portfolio_returns")

    def test_calculate_portfolio_returns_missing_columns(self):
        """Test returns calculation with missing price columns."""
        incomplete_data = self.price_data.drop(columns=["REE_close"])

        with self.assertRaises(AnalysisError):
            self.analyzer.calculate_portfolio_returns(
                incomplete_data, self.symbols, self.weights
            )

    def test_calculate_performance_metrics(self):
        """Test performance metrics calculation."""
        returns = self.analyzer.calculate_portfolio_returns(
            self.price_data, self.symbols, self.weights
        )

        metrics = self.analyzer.calculate_performance_metrics(returns)

        expected_keys = [
            "total_return",
            "annualized_return",
            "volatility",
            "sharpe_ratio",
            "max_drawdown",
            "win_rate",
            "total_periods",
            "start_date",
            "end_date",
        ]

        for key in expected_keys:
            self.assertIn(key, metrics)

        self.assertIsInstance(metrics["total_return"], (int, float))
        self.assertIsInstance(metrics["volatility"], (int, float))
        self.assertGreaterEqual(metrics["win_rate"], 0)
        self.assertLessEqual(metrics["win_rate"], 1)

    def test_calculate_performance_metrics_empty_returns(self):
        """Test metrics calculation with empty returns."""
        empty_returns = pd.Series([], name="portfolio_returns")

        with self.assertRaises(AnalysisError):
            self.analyzer.calculate_performance_metrics(empty_returns)

    def test_get_portfolio_summary_without_analysis(self):
        """Test getting summary without running analysis first."""
        with self.assertRaises(AnalysisError):
            self.analyzer.get_portfolio_summary()

    def test_get_portfolio_summary_success(self):
        """Test successful portfolio summary generation."""
        # Run analysis first
        returns = self.analyzer.calculate_portfolio_returns(
            self.price_data, self.symbols, self.weights
        )

        summary = self.analyzer.get_portfolio_summary()

        self.assertIn("returns_data", summary)
        self.assertIn("metrics", summary)
        self.assertIn("data_points", summary)
        self.assertIn("analysis_timestamp", summary)

        self.assertEqual(summary["data_points"], len(returns))


if __name__ == "__main__":
    unittest.main()
