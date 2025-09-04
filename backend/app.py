"""
app.py
Flask backend for QuantstatsWebApp.
Implements '/' and '/analyze' routes per PRD.
"""

import os
import matplotlib
from flask import Flask, render_template, request, flash
from dotenv import load_dotenv

# Import new modular services
from src.core.data_fetcher import DataFetcher
from src.core.portfolio_analyzer import PortfolioAnalyzer
from src.services.validation_service import ValidationService
from src.services.vnstock_service import VnstockService
from src.services.visualization_service import VisualizationService
from src.models.portfolio import Portfolio
from src.utils.exceptions import ValidationError, DataFetchError, AnalysisError
from src.utils.helpers import setup_logging

# Configure matplotlib
matplotlib.use("Agg")  # Use non-GUI backend for server-side image generation
matplotlib.rcParams["font.family"] = "DejaVu Sans"  # Use a Linux-safe font

load_dotenv()

# Initialize services
validation_service = ValidationService()
data_fetcher = DataFetcher()
portfolio_analyzer = PortfolioAnalyzer()
vnstock_service = VnstockService()
visualization_service = VisualizationService()

# Set up logging
setup_logging(level="INFO")

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")
if not app.secret_key:
    raise ValueError("SECRET_KEY environment variable must be set")


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        symbols = request.form.getlist("symbols[]")
        weights = request.form.getlist("weights[]")
        start_date = request.form.get("start_date", "").strip()
        end_date = request.form.get("end_date", "").strip()
        capital = request.form.get("capital", "").strip()

        # Basic field validation
        if not symbols or not weights or not start_date or not end_date or not capital:
            flash("All fields are required.")
            return render_template("index.html"), 200

        # Use validation service for comprehensive validation
        try:
            validated_data = validation_service.validate_portfolio_form(
                symbols, weights, capital, start_date, end_date
            )
        except ValidationError as e:
            flash(str(e))
            return render_template("index.html"), 200

        # Create portfolio model
        try:
            portfolio = Portfolio.from_form_data(
                symbols=validated_data["symbols"],
                weights=[str(w) for w in validated_data["weights"]],
                capital=str(validated_data["capital"]),
                start_date=validated_data["start_date"],
                end_date=validated_data["end_date"],
            )
        except ValidationError as e:
            flash(f"Portfolio creation failed: {str(e)}")
            return render_template("index.html"), 200

        # Fetch historical data using new data fetcher
        try:
            historical_data = data_fetcher.fetch_historical_data(
                portfolio.symbols, portfolio.start_date, portfolio.end_date
            )
            close_prices = data_fetcher.get_close_prices(
                historical_data, portfolio.symbols
            )
        except DataFetchError as e:
            flash(f"Error fetching data: {str(e)}")
            return render_template("index.html"), 200

        # Calculate portfolio returns using analyzer
        try:
            portfolio_returns = portfolio_analyzer.calculate_portfolio_returns(
                close_prices, portfolio.symbols, portfolio.weights
            )
        except AnalysisError as e:
            flash(f"Analysis error: {str(e)}")
            return render_template("index.html"), 200

        # Calculate performance metrics
        try:
            metrics = portfolio_analyzer.calculate_performance_metrics(
                portfolio_returns
            )
        except AnalysisError as e:
            flash(f"Error calculating metrics: {str(e)}")
            return render_template("index.html"), 200

        # Generate interactive Plotly charts
        try:
            performance_chart = (
                visualization_service.create_portfolio_performance_chart(
                    portfolio_returns, "Portfolio Performance Over Time"
                )
            )
            drawdown_chart = visualization_service.create_drawdown_chart(
                portfolio_returns, "Portfolio Drawdown Analysis"
            )
            monthly_heatmap = visualization_service.create_monthly_returns_heatmap(
                portfolio_returns, "Monthly Returns Heatmap"
            )
            metrics_dashboard = (
                visualization_service.create_performance_metrics_dashboard(
                    metrics, "Performance Metrics Dashboard"
                )
            )
            composition_chart = (
                visualization_service.create_portfolio_composition_chart(
                    portfolio.symbols, portfolio.weights, "Portfolio Composition"
                )
            )
        except AnalysisError as e:
            flash(f"Error generating charts: {str(e)}")
            return render_template("index.html"), 200

        # Render interactive analysis page instead of redirecting to static HTML
        return render_template(
            "analysis_results.html",
            portfolio=portfolio,
            metrics=metrics,
            performance_chart=performance_chart,
            drawdown_chart=drawdown_chart,
            monthly_heatmap=monthly_heatmap,
            metrics_dashboard=metrics_dashboard,
            composition_chart=composition_chart,
            returns_data=portfolio_returns,
        )
    except (ValidationError, DataFetchError, AnalysisError) as e:
        flash(f"Error: {str(e)}")
        return render_template("index.html"), 200
    except Exception as ex:
        flash(f"Unexpected error: {ex}")
        return render_template("index.html"), 200


@app.route("/ratios", methods=["GET"])
def ratios():
    """Render financial ratios analysis page."""
    return render_template("ratios.html")


@app.route("/ratios/analyze", methods=["POST"])
def analyze_ratios():
    """Analyze financial ratios for selected symbols."""
    try:
        symbols_input = request.form.get("symbols", "")
        period = request.form.get("period", "year")
        export_format = request.form.get("export_format", "table")

        # Parse comma-separated symbols
        if not symbols_input.strip():
            flash("At least one symbol is required.")
            return render_template("ratios.html"), 200

        symbols = [s.strip().upper() for s in symbols_input.split(",") if s.strip()]

        # Clean and validate symbols
        try:
            validated_symbols = validation_service.validate_symbols(symbols)
        except ValidationError as e:
            flash(str(e))
            return render_template("ratios.html"), 200

        # Fetch financial ratios using VnstockService
        try:
            ratio_data = vnstock_service.fetch_multiple_ratios(
                validated_symbols, period=period
            )

            if not ratio_data:
                flash("No financial ratio data available for the selected symbols.")
                return render_template("ratios.html"), 200

            # Create fundamental summary
            summary_data = vnstock_service.get_fundamental_summary(validated_symbols)

            # Handle export request
            if export_format == "excel":
                try:
                    output_path = vnstock_service.export_ratios_to_excel(
                        ratio_data, "financial_ratios"
                    )
                    flash(f"Financial ratios exported to {output_path}")
                except Exception as e:
                    flash(f"Export failed: {str(e)}")

            # Render results page with ratio data
            return render_template(
                "ratio_results.html",
                ratio_data=ratio_data,
                summary_data=summary_data.to_dict("records")
                if not summary_data.empty
                else [],
                symbols=validated_symbols,
                period=period,
                export_format=export_format,
            )

        except DataFetchError as e:
            flash(f"Error fetching ratio data: {str(e)}")
            return render_template("ratios.html"), 200

    except Exception as e:
        flash(f"Unexpected error: {str(e)}")
        return render_template("ratios.html"), 200


@app.route("/api/ratios/<symbol>", methods=["GET"])
def api_get_ratios(symbol):
    """API endpoint to get financial ratios for a single symbol."""
    try:
        period = request.args.get("period", "year")

        # Validate symbol
        try:
            validated_symbols = validation_service.validate_symbols([symbol])
            symbol = validated_symbols[0]
        except ValidationError as e:
            return {"error": str(e)}, 400

        # Fetch ratio data
        try:
            ratios = vnstock_service.fetch_financial_ratios(symbol, period=period)

            if ratios.empty:
                return {"error": "No ratio data available"}, 404

            # Convert to JSON-serializable format
            return {
                "symbol": symbol,
                "period": period,
                "data": ratios.to_dict("records"),
                "columns": list(ratios.columns),
                "rows": len(ratios),
            }

        except DataFetchError as e:
            return {"error": str(e)}, 500

    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}, 500


if __name__ == "__main__":
    import os

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
