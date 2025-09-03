"""
api.py
Flask API backend for portfolio analysis.
Serves JSON data for Next.js frontend.
"""

import os
import matplotlib
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Import new modular services
from src.core.data_fetcher import DataFetcher
from src.core.portfolio_analyzer import PortfolioAnalyzer
from src.services.validation_service import ValidationService
from src.services.vnstock_service import VnstockService
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

# Set up logging
setup_logging(level="INFO")

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")
if not app.secret_key:
    raise ValueError("SECRET_KEY environment variable must be set")

# Enable CORS for Next.js frontend
CORS(app, origins=["http://localhost:3000"])


@app.route("/api/health", methods=["GET"])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "healthy", "service": "portfolio-api"})


@app.route("/api/analyze", methods=["POST"])
def analyze():
    """Analyze portfolio and return JSON data."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        symbols = data.get("symbols", [])
        weights = data.get("weights", [])
        start_date = data.get("start_date", "").strip()
        end_date = data.get("end_date", "").strip()
        capital = data.get("capital", "")
        portfolio_name = data.get("name", "")

        # Basic field validation
        if not symbols or not weights or not start_date or not end_date or not capital:
            return jsonify({"error": "All fields are required"}), 400

        # Use validation service for comprehensive validation
        try:
            validated_data = validation_service.validate_portfolio_form(
                symbols, [str(w) for w in weights], str(capital), start_date, end_date
            )
        except ValidationError as e:
            return jsonify({"error": str(e)}), 400

        # Create portfolio model
        try:
            portfolio = Portfolio.from_form_data(
                symbols=validated_data["symbols"],
                weights=[str(w) for w in validated_data["weights"]],
                capital=str(validated_data["capital"]),
                start_date=validated_data["start_date"],
                end_date=validated_data["end_date"],
                name=portfolio_name,
            )
        except ValidationError as e:
            return jsonify({"error": f"Portfolio creation failed: {str(e)}"}), 400

        # Fetch historical data using new data fetcher
        try:
            historical_data = data_fetcher.fetch_historical_data(
                portfolio.symbols, portfolio.start_date, portfolio.end_date
            )
            close_prices = data_fetcher.get_close_prices(
                historical_data, portfolio.symbols
            )
        except DataFetchError as e:
            return jsonify({"error": f"Error fetching data: {str(e)}"}), 500

        # Calculate portfolio returns using analyzer
        try:
            portfolio_returns = portfolio_analyzer.calculate_portfolio_returns(
                close_prices, portfolio.symbols, portfolio.weights
            )
        except AnalysisError as e:
            return jsonify({"error": f"Analysis error: {str(e)}"}), 500

        # Calculate performance metrics
        try:
            metrics = portfolio_analyzer.calculate_performance_metrics(portfolio_returns)
        except AnalysisError as e:
            return jsonify({"error": f"Error calculating metrics: {str(e)}"}), 500

        # Prepare response data
        response_data = {
            "portfolio": portfolio.to_dict(),
            "metrics": metrics,
            "returns": {
                "data": {date.isoformat(): value for date, value in portfolio_returns.items()},
                "dates": [date.isoformat() for date in portfolio_returns.index],
                "values": portfolio_returns.tolist(),
            },
            "analysis_summary": {
                "data_points": len(portfolio_returns),
                "period": {
                    "start": portfolio.start_date,
                    "end": portfolio.end_date,
                    "days": len(portfolio_returns),
                },
                "portfolio_size": portfolio.size,
                "total_capital": portfolio.capital,
            },
        }

        return jsonify(response_data)

    except (ValidationError, DataFetchError, AnalysisError) as e:
        return jsonify({"error": str(e)}), 500
    except Exception as ex:
        return jsonify({"error": f"Unexpected error: {str(ex)}"}), 500


@app.route("/api/ratios", methods=["POST"])
def analyze_ratios():
    """Analyze financial ratios for selected symbols."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        symbols_input = data.get("symbols", "")
        period = data.get("period", "year")

        # Parse comma-separated symbols
        if not symbols_input.strip():
            return jsonify({"error": "At least one symbol is required"}), 400

        if isinstance(symbols_input, str):
            symbols = [s.strip().upper() for s in symbols_input.split(",") if s.strip()]
        else:
            symbols = [str(s).strip().upper() for s in symbols_input if str(s).strip()]

        # Clean and validate symbols
        try:
            validated_symbols = validation_service.validate_symbols(symbols)
        except ValidationError as e:
            return jsonify({"error": str(e)}), 400

        # Fetch financial ratios using VnstockService
        try:
            ratio_data = vnstock_service.fetch_multiple_ratios(
                validated_symbols, period=period
            )

            if not ratio_data:
                return jsonify({"error": "No financial ratio data available for the selected symbols"}), 404

            # Create fundamental summary
            summary_data = vnstock_service.get_fundamental_summary(validated_symbols)

            # Convert DataFrames to JSON-serializable format
            response_data = {
                "symbols": validated_symbols,
                "period": period,
                "ratio_data": {},
                "summary_data": summary_data.to_dict("records") if not summary_data.empty else [],
            }

            # Convert each DataFrame to records format
            for symbol, df in ratio_data.items():
                response_data["ratio_data"][symbol] = {
                    "data": df.to_dict("records"),
                    "columns": list(df.columns),
                    "index": [str(idx) for idx in df.index],
                }

            return jsonify(response_data)

        except DataFetchError as e:
            return jsonify({"error": f"Error fetching ratio data: {str(e)}"}), 500

    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500


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
            return jsonify({"error": str(e)}), 400

        # Fetch ratio data
        try:
            ratios = vnstock_service.fetch_financial_ratios(symbol, period=period)

            if ratios.empty:
                return jsonify({"error": "No ratio data available"}), 404

            # Convert to JSON-serializable format
            return jsonify({
                "symbol": symbol,
                "period": period,
                "data": ratios.to_dict("records"),
                "columns": list(ratios.columns),
                "rows": len(ratios),
            })

        except DataFetchError as e:
            return jsonify({"error": str(e)}), 500

    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500


@app.route("/api/validate", methods=["POST"])
def validate_input():
    """Validate portfolio input without running full analysis."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        symbols = data.get("symbols", [])
        weights = data.get("weights", [])
        start_date = data.get("start_date", "").strip()
        end_date = data.get("end_date", "").strip()
        capital = data.get("capital", "")

        try:
            validated_data = validation_service.validate_portfolio_form(
                symbols, [str(w) for w in weights], str(capital), start_date, end_date
            )
            return jsonify({
                "valid": True,
                "validated_data": validated_data
            })
        except ValidationError as e:
            return jsonify({
                "valid": False,
                "error": str(e)
            }), 400

    except Exception as e:
        return jsonify({"error": f"Validation error: {str(e)}"}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port, debug=True)