"""
Interactive visualization service using Plotly.
"""

import pandas as pd
from typing import Dict, List
import logging
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.offline as pyo

from ..utils.exceptions import AnalysisError

logger = logging.getLogger(__name__)


class VisualizationService:
    """Service for creating interactive charts using Plotly."""

    def __init__(self):
        """Initialize visualization service."""
        self.default_theme = {
            "layout": {
                "paper_bgcolor": "white",
                "plot_bgcolor": "white",
                "font": {"family": "Arial, sans-serif", "size": 12},
                "colorway": [
                    "#1f77b4",
                    "#ff7f0e",
                    "#2ca02c",
                    "#d62728",
                    "#9467bd",
                    "#8c564b",
                ],
            }
        }
        logger.debug("VisualizationService initialized")

    def create_portfolio_performance_chart(
        self, returns: pd.Series, title: str = "Portfolio Performance"
    ) -> str:
        """
        Create interactive portfolio performance chart.

        Args:
            returns: Portfolio returns series
            title: Chart title

        Returns:
            HTML div string containing the chart
        """
        try:
            if returns.empty:
                raise AnalysisError("Cannot create chart with empty returns data")

            # Calculate cumulative returns
            cumulative_returns = (1 + returns).cumprod() - 1

            fig = go.Figure()

            # Add cumulative returns line
            fig.add_trace(
                go.Scatter(
                    x=cumulative_returns.index,
                    y=cumulative_returns.values * 100,
                    mode="lines",
                    name="Cumulative Return (%)",
                    line=dict(color="#1f77b4", width=2),
                    hovertemplate="<b>Date:</b> %{x}<br>"
                    + "<b>Return:</b> %{y:.2f}%<br>"
                    + "<extra></extra>",
                )
            )

            # Update layout
            fig.update_layout(
                title={
                    "text": title,
                    "x": 0.5,
                    "font": {"size": 16, "color": "#1a237e"},
                },
                xaxis_title="Date",
                yaxis_title="Cumulative Return (%)",
                hovermode="x unified",
                showlegend=True,
                height=400,
                **self.default_theme["layout"],
            )

            # Add grid
            fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor="#f0f0f0")
            fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="#f0f0f0")

            # Convert to HTML
            return pyo.plot(fig, output_type="div", include_plotlyjs="cdn")

        except Exception as e:
            logger.error(f"Error creating portfolio performance chart: {e}")
            raise AnalysisError(f"Failed to create performance chart: {str(e)}")

    def create_drawdown_chart(
        self, returns: pd.Series, title: str = "Portfolio Drawdown"
    ) -> str:
        """
        Create interactive drawdown chart.

        Args:
            returns: Portfolio returns series
            title: Chart title

        Returns:
            HTML div string containing the chart
        """
        try:
            if returns.empty:
                raise AnalysisError("Cannot create chart with empty returns data")

            # Calculate running maximum and drawdown
            cumulative_returns = (1 + returns).cumprod()
            running_max = cumulative_returns.expanding().max()
            drawdown = (cumulative_returns / running_max - 1) * 100

            fig = go.Figure()

            # Add drawdown area chart
            fig.add_trace(
                go.Scatter(
                    x=drawdown.index,
                    y=drawdown.values,
                    fill="tonexty",
                    mode="none",
                    name="Drawdown (%)",
                    fillcolor="rgba(255, 99, 132, 0.3)",
                    line=dict(color="#ff6384"),
                    hovertemplate="<b>Date:</b> %{x}<br>"
                    + "<b>Drawdown:</b> %{y:.2f}%<br>"
                    + "<extra></extra>",
                )
            )

            # Add zero line
            fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)

            fig.update_layout(
                title={
                    "text": title,
                    "x": 0.5,
                    "font": {"size": 16, "color": "#1a237e"},
                },
                xaxis_title="Date",
                yaxis_title="Drawdown (%)",
                hovermode="x unified",
                showlegend=True,
                height=400,
                **self.default_theme["layout"],
            )

            # Add grid
            fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor="#f0f0f0")
            fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="#f0f0f0")

            return pyo.plot(fig, output_type="div", include_plotlyjs="cdn")

        except Exception as e:
            logger.error(f"Error creating drawdown chart: {e}")
            raise AnalysisError(f"Failed to create drawdown chart: {str(e)}")

    def create_monthly_returns_heatmap(
        self, returns: pd.Series, title: str = "Monthly Returns Heatmap"
    ) -> str:
        """
        Create interactive monthly returns heatmap.

        Args:
            returns: Portfolio returns series
            title: Chart title

        Returns:
            HTML div string containing the chart
        """
        try:
            if returns.empty:
                raise AnalysisError("Cannot create chart with empty returns data")

            # Calculate monthly returns
            monthly_returns = returns.resample("M").apply(lambda x: (1 + x).prod() - 1)

            # Create pivot table for heatmap
            monthly_returns.index = pd.to_datetime(monthly_returns.index)
            pivot_table = (
                monthly_returns.groupby(
                    [monthly_returns.index.year, monthly_returns.index.month]
                )
                .first()
                .unstack()
            )

            # Convert to percentage
            pivot_table = pivot_table * 100

            # Create month labels
            month_labels = [
                "Jan",
                "Feb",
                "Mar",
                "Apr",
                "May",
                "Jun",
                "Jul",
                "Aug",
                "Sep",
                "Oct",
                "Nov",
                "Dec",
            ]

            fig = go.Figure(
                data=go.Heatmap(
                    z=pivot_table.values,
                    x=month_labels,
                    y=pivot_table.index.astype(str),
                    colorscale="RdYlGn",
                    zmid=0,
                    hovertemplate="<b>Year:</b> %{y}<br>"
                    + "<b>Month:</b> %{x}<br>"
                    + "<b>Return:</b> %{z:.2f}%<br>"
                    + "<extra></extra>",
                    colorbar=dict(title="Return (%)", titleside="right"),
                )
            )

            fig.update_layout(
                title={
                    "text": title,
                    "x": 0.5,
                    "font": {"size": 16, "color": "#1a237e"},
                },
                xaxis_title="Month",
                yaxis_title="Year",
                height=400,
                **self.default_theme["layout"],
            )

            return pyo.plot(fig, output_type="div", include_plotlyjs="cdn")

        except Exception as e:
            logger.error(f"Error creating monthly returns heatmap: {e}")
            raise AnalysisError(f"Failed to create heatmap: {str(e)}")

    def create_performance_metrics_dashboard(
        self, metrics: Dict[str, float], title: str = "Performance Metrics"
    ) -> str:
        """
        Create performance metrics dashboard.

        Args:
            metrics: Dictionary of performance metrics
            title: Chart title

        Returns:
            HTML div string containing the dashboard
        """
        try:
            # Create subplot with 2x2 grid
            fig = make_subplots(
                rows=2,
                cols=2,
                subplot_titles=(
                    "Total Return",
                    "Sharpe Ratio",
                    "Max Drawdown",
                    "Volatility",
                ),
                specs=[
                    [{"type": "indicator"}, {"type": "indicator"}],
                    [{"type": "indicator"}, {"type": "indicator"}],
                ],
            )

            # Total Return
            total_return = metrics.get("total_return", 0) * 100
            fig.add_trace(
                go.Indicator(
                    mode="gauge+number+delta",
                    value=total_return,
                    domain={"x": [0, 1], "y": [0, 1]},
                    title={"text": "Total Return (%)"},
                    gauge={
                        "axis": {"range": [-50, 100]},
                        "bar": {"color": "darkblue"},
                        "steps": [
                            {"range": [-50, 0], "color": "lightgray"},
                            {"range": [0, 50], "color": "gray"},
                            {"range": [50, 100], "color": "lightgreen"},
                        ],
                        "threshold": {
                            "line": {"color": "red", "width": 4},
                            "thickness": 0.75,
                            "value": 90,
                        },
                    },
                ),
                row=1,
                col=1,
            )

            # Sharpe Ratio
            sharpe_ratio = metrics.get("sharpe_ratio", 0)
            fig.add_trace(
                go.Indicator(
                    mode="number+delta",
                    value=sharpe_ratio,
                    title={"text": "Sharpe Ratio"},
                    number={"font": {"size": 40}},
                ),
                row=1,
                col=2,
            )

            # Max Drawdown
            max_drawdown = abs(metrics.get("max_drawdown", 0)) * 100
            fig.add_trace(
                go.Indicator(
                    mode="number+delta",
                    value=max_drawdown,
                    title={"text": "Max Drawdown (%)"},
                    number={"font": {"size": 40, "color": "red"}},
                ),
                row=2,
                col=1,
            )

            # Volatility
            volatility = metrics.get("volatility", 0) * 100
            fig.add_trace(
                go.Indicator(
                    mode="number+delta",
                    value=volatility,
                    title={"text": "Volatility (%)"},
                    number={"font": {"size": 40}},
                ),
                row=2,
                col=2,
            )

            fig.update_layout(
                title={
                    "text": title,
                    "x": 0.5,
                    "font": {"size": 16, "color": "#1a237e"},
                },
                height=500,
                **self.default_theme["layout"],
            )

            return pyo.plot(fig, output_type="div", include_plotlyjs="cdn")

        except Exception as e:
            logger.error(f"Error creating performance dashboard: {e}")
            raise AnalysisError(f"Failed to create dashboard: {str(e)}")

    def create_portfolio_composition_chart(
        self,
        symbols: List[str],
        weights: List[float],
        title: str = "Portfolio Composition",
    ) -> str:
        """
        Create portfolio composition pie chart.

        Args:
            symbols: List of stock symbols
            weights: List of portfolio weights
            title: Chart title

        Returns:
            HTML div string containing the chart
        """
        try:
            fig = go.Figure(
                data=[
                    go.Pie(
                        labels=symbols,
                        values=[w * 100 for w in weights],
                        hole=0.3,
                        hovertemplate="<b>%{label}</b><br>"
                        + "Weight: %{value:.1f}%<br>"
                        + "<extra></extra>",
                    )
                ]
            )

            fig.update_layout(
                title={
                    "text": title,
                    "x": 0.5,
                    "font": {"size": 16, "color": "#1a237e"},
                },
                height=400,
                showlegend=True,
                **self.default_theme["layout"],
            )

            return pyo.plot(fig, output_type="div", include_plotlyjs="cdn")

        except Exception as e:
            logger.error(f"Error creating composition chart: {e}")
            raise AnalysisError(f"Failed to create composition chart: {str(e)}")

    def create_ratio_comparison_chart(
        self,
        ratio_data: Dict[str, pd.DataFrame],
        metric: str = "PE",
        title: str = "Financial Ratios Comparison",
    ) -> str:
        """
        Create financial ratios comparison chart.

        Args:
            ratio_data: Dictionary of ratio dataframes by symbol
            metric: Metric to compare (e.g., 'PE', 'PB', 'ROE')
            title: Chart title

        Returns:
            HTML div string containing the chart
        """
        try:
            fig = go.Figure()

            for symbol, df in ratio_data.items():
                if metric in df.columns:
                    fig.add_trace(
                        go.Bar(
                            name=symbol,
                            x=df.index.astype(str),
                            y=df[metric],
                            hovertemplate=f"<b>{symbol}</b><br>"
                            + f"{metric}: %{{y:.2f}}<br>"
                            + "Period: %{x}<br>"
                            + "<extra></extra>",
                        )
                    )

            fig.update_layout(
                title={
                    "text": f"{title} - {metric}",
                    "x": 0.5,
                    "font": {"size": 16, "color": "#1a237e"},
                },
                xaxis_title="Period",
                yaxis_title=f"{metric} Ratio",
                barmode="group",
                hovermode="x unified",
                height=400,
                **self.default_theme["layout"],
            )

            # Add grid
            fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor="#f0f0f0")
            fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="#f0f0f0")

            return pyo.plot(fig, output_type="div", include_plotlyjs="cdn")

        except Exception as e:
            logger.error(f"Error creating ratio comparison chart: {e}")
            raise AnalysisError(f"Failed to create ratio comparison chart: {str(e)}")

    def export_chart_as_image(
        self,
        chart_html: str,
        output_path: str,
        format: str = "png",
        width: int = 800,
        height: int = 600,
    ) -> str:
        """
        Export chart as static image.

        Args:
            chart_html: Chart HTML content
            output_path: Output file path
            format: Image format (png, svg, pdf)
            width: Image width
            height: Image height

        Returns:
            Path to exported image
        """
        try:
            # This would require extracting the figure from HTML
            # For now, return placeholder implementation
            logger.info(f"Chart export requested: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"Error exporting chart: {e}")
            raise AnalysisError(f"Failed to export chart: {str(e)}")
