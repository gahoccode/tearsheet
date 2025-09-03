"""
Portfolio data models and structures.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
import pandas as pd
from datetime import datetime

from ..utils.exceptions import ValidationError
from ..utils.constants import MIN_WEIGHT, MAX_WEIGHT, WEIGHT_TOLERANCE


@dataclass
class Stock:
    """Represents a single stock in the portfolio."""

    symbol: str
    weight: float
    name: Optional[str] = None
    sector: Optional[str] = None

    def __post_init__(self):
        """Validate stock data after initialization."""
        if not self.symbol:
            raise ValidationError("Stock symbol cannot be empty")

        if not (MIN_WEIGHT <= self.weight <= MAX_WEIGHT):
            raise ValidationError(
                f"Weight must be between {MIN_WEIGHT} and {MAX_WEIGHT}"
            )

        # Convert symbol to uppercase
        self.symbol = self.symbol.upper().strip()


@dataclass
class Portfolio:
    """Represents a complete portfolio with validation."""

    stocks: List[Stock]
    capital: float
    start_date: str
    end_date: str
    name: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        """Validate portfolio data after initialization."""
        if not self.stocks:
            raise ValidationError("Portfolio must contain at least one stock")

        if self.capital <= 0:
            raise ValidationError("Capital must be positive")

        # Validate total weight sums to 1.0
        total_weight = sum(stock.weight for stock in self.stocks)
        if abs(total_weight - 1.0) > WEIGHT_TOLERANCE:
            raise ValidationError("Portfolio weights must sum to 1.0")

        # Validate date format
        try:
            start_dt = datetime.strptime(self.start_date, "%Y-%m-%d")
            end_dt = datetime.strptime(self.end_date, "%Y-%m-%d")
            if start_dt >= end_dt:
                raise ValidationError("Start date must be before end date")
        except ValueError:
            raise ValidationError("Dates must be in YYYY-MM-DD format")

    @property
    def symbols(self) -> List[str]:
        """Get list of stock symbols."""
        return [stock.symbol for stock in self.stocks]

    @property
    def weights(self) -> List[float]:
        """Get list of stock weights."""
        return [stock.weight for stock in self.stocks]

    @property
    def size(self) -> int:
        """Get number of stocks in portfolio."""
        return len(self.stocks)

    def get_stock_allocation(self) -> Dict[str, float]:
        """Get capital allocation per stock."""
        return {stock.symbol: stock.weight * self.capital for stock in self.stocks}

    def to_dict(self) -> Dict[str, Any]:
        """Convert portfolio to dictionary."""
        return {
            "name": self.name,
            "capital": self.capital,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "created_at": self.created_at.isoformat(),
            "stocks": [
                {
                    "symbol": stock.symbol,
                    "weight": stock.weight,
                    "name": stock.name,
                    "sector": stock.sector,
                    "allocation": stock.weight * self.capital,
                }
                for stock in self.stocks
            ],
            "summary": {
                "size": self.size,
                "total_weight": sum(self.weights),
                "symbols": self.symbols,
            },
        }

    @classmethod
    def from_form_data(
        cls,
        symbols: List[str],
        weights: List[str],
        capital: str,
        start_date: str,
        end_date: str,
        name: Optional[str] = None,
    ) -> "Portfolio":
        """
        Create portfolio from web form data.

        Args:
            symbols: List of stock symbols
            weights: List of weight strings
            capital: Capital amount string
            start_date: Start date string
            end_date: End date string
            name: Optional portfolio name

        Returns:
            Portfolio instance

        Raises:
            ValidationError: If validation fails
        """
        try:
            # Convert weights to float
            weight_floats = [float(w.strip()) for w in weights]
            capital_float = float(capital.strip())

            # Create Stock instances
            stocks = [
                Stock(symbol=sym.strip(), weight=wt)
                for sym, wt in zip(symbols, weight_floats)
            ]

            # Create portfolio
            return cls(
                stocks=stocks,
                capital=capital_float,
                start_date=start_date.strip(),
                end_date=end_date.strip(),
                name=name,
            )

        except ValueError as e:
            raise ValidationError(f"Invalid numeric data: {str(e)}")
        except Exception as e:
            raise ValidationError(f"Portfolio creation failed: {str(e)}")


@dataclass
class PortfolioAnalysis:
    """Represents portfolio analysis results."""

    portfolio: Portfolio
    returns_data: pd.Series
    metrics: Dict[str, float]
    individual_returns: Optional[pd.DataFrame] = None
    analysis_timestamp: datetime = field(default_factory=datetime.now)

    def get_summary_stats(self) -> Dict[str, Any]:
        """Get summary statistics."""
        return {
            "portfolio": self.portfolio.to_dict(),
            "performance": self.metrics,
            "data_points": len(self.returns_data),
            "period": {
                "start": self.returns_data.index.min().strftime("%Y-%m-%d"),
                "end": self.returns_data.index.max().strftime("%Y-%m-%d"),
                "days": len(self.returns_data),
            },
            "analysis_timestamp": self.analysis_timestamp.isoformat(),
        }

    def to_dict(self) -> Dict[str, Any]:
        """Convert analysis to dictionary for JSON serialization."""
        return {
            **self.get_summary_stats(),
            "returns": self.returns_data.to_dict()
            if not self.returns_data.empty
            else {},
            "individual_returns": (
                self.individual_returns.to_dict()
                if self.individual_returns is not None
                and not self.individual_returns.empty
                else {}
            ),
        }
