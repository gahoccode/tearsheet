"""
Portfolio analysis and calculation engine for tearsheet application.

This module handles portfolio construction, returns calculation,
and performance metrics computation.
"""

from typing import List, Dict
import pandas as pd
import numpy as np
import logging

from ..utils.exceptions import PortfolioError, AnalysisError
from ..utils.constants import (
    MIN_PORTFOLIO_SIZE,
    MAX_PORTFOLIO_SIZE,
    MIN_WEIGHT,
    MAX_WEIGHT,
    WEIGHT_TOLERANCE,
    ERROR_MESSAGES,
)

logger = logging.getLogger(__name__)


class PortfolioAnalyzer:
    """
    Portfolio analysis engine for calculating returns and performance metrics.
    """

    def __init__(self):
        """Initialize portfolio analyzer."""
        self.portfolio_data = None
        self.returns = None
        self.portfolio_returns = None
        logger.debug("PortfolioAnalyzer initialized")

    def validate_portfolio(
        self, symbols: List[str], weights: List[float], capital: float
    ) -> Dict[str, any]:
        """
        Validate portfolio inputs and return normalized data.

        Args:
            symbols: List of stock symbols
            weights: List of portfolio weights
            capital: Initial capital amount

        Returns:
            Dictionary with validated portfolio data

        Raises:
            PortfolioError: If validation fails
        """
        logger.info(f"Validating portfolio: {len(symbols)} symbols")

        # Basic validation
        if not symbols:
            raise PortfolioError("No symbols provided")

        if len(symbols) < MIN_PORTFOLIO_SIZE:
            raise PortfolioError(
                f"Portfolio must have at least {MIN_PORTFOLIO_SIZE} symbol(s)"
            )

        if len(symbols) > MAX_PORTFOLIO_SIZE:
            raise PortfolioError(ERROR_MESSAGES["PORTFOLIO_TOO_LARGE"])

        if len(symbols) != len(weights):
            raise PortfolioError("Number of symbols and weights must match")

        # Weight validation
        if any(w < MIN_WEIGHT or w > MAX_WEIGHT for w in weights):
            raise PortfolioError(ERROR_MESSAGES["INVALID_WEIGHT"])

        weight_sum = sum(weights)
        if abs(weight_sum - 1.0) > WEIGHT_TOLERANCE:
            raise PortfolioError(ERROR_MESSAGES["WEIGHTS_NOT_SUM_ONE"])

        # Capital validation
        if capital <= 0:
            raise PortfolioError("Initial capital must be positive")

        # Normalize weights to ensure they sum exactly to 1.0
        normalized_weights = [w / weight_sum for w in weights]

        portfolio_data = {
            "symbols": symbols,
            "weights": normalized_weights,
            "capital": capital,
            "size": len(symbols),
        }

        logger.info(f"Portfolio validated: {symbols} with weights {normalized_weights}")
        return portfolio_data

    def calculate_portfolio_returns(
        self, price_data: pd.DataFrame, symbols: List[str], weights: List[float]
    ) -> pd.Series:
        """
        Calculate portfolio returns from price data and weights.

        Args:
            price_data: DataFrame with price data (time as index)
            symbols: List of stock symbols
            weights: List of portfolio weights

        Returns:
            Portfolio returns as pandas Series

        Raises:
            AnalysisError: If calculation fails
        """
        try:
            logger.info("Calculating portfolio returns")

            # Ensure price_data has time as index
            if "time" in price_data.columns:
                price_data = price_data.set_index("time")

            # Convert time index to datetime if not already
            if not isinstance(price_data.index, pd.DatetimeIndex):
                price_data.index = pd.to_datetime(price_data.index)

            # Sort by time
            price_data = price_data.sort_index()

            # Calculate individual stock returns
            returns = price_data.pct_change().dropna()

            # Ensure we have the expected columns
            expected_cols = [f"{symbol}_close" for symbol in symbols]
            missing_cols = [col for col in expected_cols if col not in returns.columns]
            if missing_cols:
                raise AnalysisError(f"Missing price columns: {missing_cols}")

            # Calculate weighted portfolio returns
            portfolio_returns = pd.Series(
                0.0, index=returns.index, name="portfolio_returns"
            )

            for symbol, weight in zip(symbols, weights):
                col_name = f"{symbol}_close"
                if col_name in returns.columns:
                    portfolio_returns += returns[col_name] * weight
                else:
                    logger.warning(f"Missing data for symbol {symbol}")

            # Store for later use
            self.returns = returns
            self.portfolio_returns = portfolio_returns

            logger.info(
                f"Portfolio returns calculated: {len(portfolio_returns)} periods"
            )
            return portfolio_returns

        except Exception as e:
            raise AnalysisError(f"Failed to calculate portfolio returns: {str(e)}")

    def calculate_performance_metrics(
        self, portfolio_returns: pd.Series, risk_free_rate: float = 0.0
    ) -> Dict[str, float]:
        """
        Calculate key performance metrics for the portfolio.

        Args:
            portfolio_returns: Portfolio returns series
            risk_free_rate: Risk-free rate for Sharpe ratio calculation

        Returns:
            Dictionary of performance metrics
        """
        try:
            logger.info("Calculating performance metrics")

            if portfolio_returns.empty:
                raise AnalysisError("No returns data available for metrics calculation")

            # Basic statistics
            total_return = (1 + portfolio_returns).prod() - 1
            annualized_return = (
                1 + portfolio_returns.mean()
            ) ** 252 - 1  # Assuming daily data
            volatility = portfolio_returns.std() * np.sqrt(252)  # Annualized volatility

            # Sharpe ratio
            excess_return = annualized_return - risk_free_rate
            sharpe_ratio = excess_return / volatility if volatility > 0 else 0

            # Drawdown calculation
            cumulative_returns = (1 + portfolio_returns).cumprod()
            rolling_max = cumulative_returns.expanding().max()
            drawdowns = (cumulative_returns - rolling_max) / rolling_max
            max_drawdown = drawdowns.min()

            # Additional metrics
            positive_periods = len(portfolio_returns[portfolio_returns > 0])
            total_periods = len(portfolio_returns)
            win_rate = positive_periods / total_periods if total_periods > 0 else 0

            metrics = {
                "total_return": total_return,
                "annualized_return": annualized_return,
                "volatility": volatility,
                "sharpe_ratio": sharpe_ratio,
                "max_drawdown": max_drawdown,
                "win_rate": win_rate,
                "total_periods": total_periods,
                "start_date": portfolio_returns.index.min(),
                "end_date": portfolio_returns.index.max(),
            }

            logger.info("Performance metrics calculated successfully")
            return metrics

        except Exception as e:
            raise AnalysisError(f"Failed to calculate performance metrics: {str(e)}")

    def get_portfolio_summary(self) -> Dict[str, any]:
        """
        Get comprehensive portfolio analysis summary.

        Returns:
            Dictionary with portfolio summary data
        """
        if self.portfolio_returns is None:
            raise AnalysisError(
                "No portfolio analysis available. Run calculate_portfolio_returns first."
            )

        summary = {
            "returns_data": self.portfolio_returns,
            "individual_returns": self.returns,
            "metrics": self.calculate_performance_metrics(self.portfolio_returns),
            "data_points": len(self.portfolio_returns),
            "analysis_timestamp": pd.Timestamp.now(),
        }

        return summary
