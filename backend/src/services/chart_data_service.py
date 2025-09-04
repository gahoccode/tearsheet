"""
Chart data service for creating Plotly chart configurations.
"""

import pandas as pd
from typing import Dict, Any, List
import logging

from ..utils.exceptions import AnalysisError

logger = logging.getLogger(__name__)


class ChartDataService:
    """Service for creating Plotly chart data configurations."""

    def __init__(self):
        """Initialize chart data service."""
        self.default_colors = [
            "#1f77b4",
            "#ff7f0e",
            "#2ca02c",
            "#d62728",
            "#9467bd",
            "#8c564b",
        ]
        logger.debug("ChartDataService initialized")

    def create_portfolio_performance_data(
        self, returns: pd.Series, title: str = "Portfolio Performance Over Time"
    ) -> Dict[str, Any]:
        """
        Create portfolio performance chart data.

        Args:
            returns: Portfolio returns series
            title: Chart title

        Returns:
            Dictionary containing chart data and layout
        """
        try:
            if returns.empty:
                raise AnalysisError("Cannot create chart with empty returns data")

            # Calculate cumulative returns
            cumulative_returns = (1 + returns).cumprod() - 1

            data = [
                {
                    "x": [
                        date.strftime("%Y-%m-%d") for date in cumulative_returns.index
                    ],
                    "y": (cumulative_returns * 100).round(2).tolist(),
                    "type": "scatter",
                    "mode": "lines",
                    "name": "Cumulative Return (%)",
                    "line": {"color": "#1f77b4", "width": 2},
                    "hovertemplate": "<b>Date:</b> %{x}<br><b>Return:</b> %{y:.2f}%<extra></extra>",
                }
            ]

            layout = {
                "title": {
                    "text": title,
                    "x": 0.5,
                    "font": {"size": 16, "color": "#1a237e"},
                },
                "xaxis": {"title": "Date", "showgrid": True, "gridcolor": "#f0f0f0"},
                "yaxis": {
                    "title": "Cumulative Return (%)",
                    "showgrid": True,
                    "gridcolor": "#f0f0f0",
                },
                "hovermode": "x unified",
                "showlegend": True,
                "height": 400,
                "paper_bgcolor": "white",
                "plot_bgcolor": "white",
                "font": {"family": "Arial, sans-serif", "size": 12},
            }

            return {"data": data, "layout": layout}

        except Exception as e:
            logger.error(f"Error creating portfolio performance data: {e}")
            raise AnalysisError(f"Failed to create performance chart data: {str(e)}")

    def create_drawdown_data(
        self, returns: pd.Series, title: str = "Portfolio Drawdown Analysis"
    ) -> Dict[str, Any]:
        """
        Create drawdown chart data.

        Args:
            returns: Portfolio returns series
            title: Chart title

        Returns:
            Dictionary containing chart data and layout
        """
        try:
            if returns.empty:
                raise AnalysisError("Cannot create chart with empty returns data")

            # Calculate running maximum and drawdown
            cumulative_returns = (1 + returns).cumprod()
            running_max = cumulative_returns.expanding().max()
            drawdown = (cumulative_returns / running_max - 1) * 100

            data = [
                {
                    "x": [date.strftime("%Y-%m-%d") for date in drawdown.index],
                    "y": drawdown.round(2).tolist(),
                    "type": "scatter",
                    "mode": "lines",
                    "name": "Drawdown (%)",
                    "fill": "tonexty",
                    "fillcolor": "rgba(255, 99, 132, 0.3)",
                    "line": {"color": "#ff6384"},
                    "hovertemplate": "<b>Date:</b> %{x}<br><b>Drawdown:</b> %{y:.2f}%<extra></extra>",
                }
            ]

            layout = {
                "title": {
                    "text": title,
                    "x": 0.5,
                    "font": {"size": 16, "color": "#1a237e"},
                },
                "xaxis": {"title": "Date", "showgrid": True, "gridcolor": "#f0f0f0"},
                "yaxis": {
                    "title": "Drawdown (%)",
                    "showgrid": True,
                    "gridcolor": "#f0f0f0",
                },
                "hovermode": "x unified",
                "showlegend": True,
                "height": 400,
                "paper_bgcolor": "white",
                "plot_bgcolor": "white",
                "font": {"family": "Arial, sans-serif", "size": 12},
                "shapes": [
                    {
                        "type": "line",
                        "xref": "paper",
                        "x0": 0,
                        "x1": 1,
                        "yref": "y",
                        "y0": 0,
                        "y1": 0,
                        "line": {"color": "gray", "dash": "dash", "width": 1},
                    }
                ],
            }

            return {"data": data, "layout": layout}

        except Exception as e:
            logger.error(f"Error creating drawdown data: {e}")
            raise AnalysisError(f"Failed to create drawdown chart data: {str(e)}")

    def create_composition_data(
        self,
        symbols: List[str],
        weights: List[float],
        title: str = "Portfolio Composition",
    ) -> Dict[str, Any]:
        """
        Create portfolio composition chart data.

        Args:
            symbols: List of stock symbols
            weights: List of portfolio weights
            title: Chart title

        Returns:
            Dictionary containing chart data and layout
        """
        try:
            data = [
                {
                    "labels": symbols,
                    "values": [round(w * 100, 1) for w in weights],
                    "type": "pie",
                    "hole": 0.3,
                    "hovertemplate": "<b>%{label}</b><br>Weight: %{value:.1f}%<extra></extra>",
                    "textinfo": "label+percent",
                    "textposition": "auto",
                }
            ]

            layout = {
                "title": {
                    "text": title,
                    "x": 0.5,
                    "font": {"size": 16, "color": "#1a237e"},
                },
                "height": 400,
                "showlegend": True,
                "paper_bgcolor": "white",
                "plot_bgcolor": "white",
                "font": {"family": "Arial, sans-serif", "size": 12},
            }

            return {"data": data, "layout": layout}

        except Exception as e:
            logger.error(f"Error creating composition data: {e}")
            raise AnalysisError(f"Failed to create composition chart data: {str(e)}")

    def create_metrics_dashboard_data(
        self, metrics: Dict[str, float], title: str = "Performance Metrics Dashboard"
    ) -> Dict[str, Any]:
        """
        Create performance metrics dashboard data.

        Args:
            metrics: Dictionary of performance metrics
            title: Chart title

        Returns:
            Dictionary containing chart data and layout
        """
        try:
            # Create a bar chart with key metrics
            metric_names = []
            metric_values = []
            metric_colors = []

            # Total Return
            total_return = metrics.get("total_return", 0) * 100
            metric_names.append("Total Return (%)")
            metric_values.append(round(total_return, 2))
            metric_colors.append("#1f77b4" if total_return >= 0 else "#d62728")

            # Annualized Return
            ann_return = metrics.get("annualized_return", 0) * 100
            metric_names.append("Annualized Return (%)")
            metric_values.append(round(ann_return, 2))
            metric_colors.append("#1f77b4" if ann_return >= 0 else "#d62728")

            # Sharpe Ratio
            sharpe = metrics.get("sharpe_ratio", 0)
            metric_names.append("Sharpe Ratio")
            metric_values.append(round(sharpe, 3))
            metric_colors.append(
                "#2ca02c" if sharpe > 1 else "#ff7f0e" if sharpe > 0 else "#d62728"
            )

            # Max Drawdown
            max_dd = abs(metrics.get("max_drawdown", 0)) * 100
            metric_names.append("Max Drawdown (%)")
            metric_values.append(round(max_dd, 2))
            metric_colors.append("#d62728")

            # Volatility
            volatility = metrics.get("volatility", 0) * 100
            metric_names.append("Volatility (%)")
            metric_values.append(round(volatility, 2))
            metric_colors.append("#ff7f0e")

            # Win Rate
            win_rate = metrics.get("win_rate", 0) * 100
            metric_names.append("Win Rate (%)")
            metric_values.append(round(win_rate, 1))
            metric_colors.append("#2ca02c" if win_rate >= 50 else "#d62728")

            data = [
                {
                    "x": metric_names,
                    "y": metric_values,
                    "type": "bar",
                    "marker": {
                        "color": metric_colors,
                        "line": {"color": "white", "width": 1},
                    },
                    "text": [f"{v}" for v in metric_values],
                    "textposition": "auto",
                    "hovertemplate": "<b>%{x}</b><br>Value: %{y}<extra></extra>",
                }
            ]

            layout = {
                "title": {
                    "text": title,
                    "x": 0.5,
                    "font": {"size": 16, "color": "#1a237e"},
                },
                "xaxis": {"title": "Metrics", "tickangle": -45, "showgrid": False},
                "yaxis": {"title": "Value", "showgrid": True, "gridcolor": "#f0f0f0"},
                "height": 400,
                "showlegend": False,
                "paper_bgcolor": "white",
                "plot_bgcolor": "white",
                "font": {"family": "Arial, sans-serif", "size": 12},
                "margin": {"l": 60, "r": 20, "t": 60, "b": 100},
            }

            return {"data": data, "layout": layout}

        except Exception as e:
            logger.error(f"Error creating metrics dashboard data: {e}")
            raise AnalysisError(f"Failed to create dashboard chart data: {str(e)}")

    def create_ratio_comparison_data(
        self,
        ratio_data: Dict[str, pd.DataFrame],
        metric: str = "PE",
        title: str = "Financial Ratios Comparison",
    ) -> Dict[str, Any]:
        """
        Create financial ratios comparison chart data.

        Args:
            ratio_data: Dictionary of ratio dataframes by symbol
            metric: Metric to compare
            title: Chart title

        Returns:
            Dictionary containing chart data and layout
        """
        try:
            data = []
            color_idx = 0

            for symbol, df in ratio_data.items():
                if metric in df.columns and not df[metric].isna().all():
                    data.append(
                        {
                            "x": [str(idx) for idx in df.index],
                            "y": df[metric].round(2).tolist(),
                            "type": "bar",
                            "name": symbol,
                            "marker": {
                                "color": self.default_colors[
                                    color_idx % len(self.default_colors)
                                ]
                            },
                            "hovertemplate": f"<b>{symbol}</b><br>{metric}: %{{y:.2f}}<br>Period: %{{x}}<extra></extra>",
                        }
                    )
                    color_idx += 1

            layout = {
                "title": {
                    "text": f"{title} - {metric}",
                    "x": 0.5,
                    "font": {"size": 16, "color": "#1a237e"},
                },
                "xaxis": {"title": "Period", "showgrid": True, "gridcolor": "#f0f0f0"},
                "yaxis": {
                    "title": f"{metric} Ratio",
                    "showgrid": True,
                    "gridcolor": "#f0f0f0",
                },
                "barmode": "group",
                "hovermode": "x unified",
                "height": 400,
                "showlegend": True,
                "paper_bgcolor": "white",
                "plot_bgcolor": "white",
                "font": {"family": "Arial, sans-serif", "size": 12},
            }

            return {"data": data, "layout": layout}

        except Exception as e:
            logger.error(f"Error creating ratio comparison data: {e}")
            raise AnalysisError(
                f"Failed to create ratio comparison chart data: {str(e)}"
            )
