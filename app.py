"""
app.py
Flask backend for QuantstatsWebApp.
Implements '/' and '/analyze' routes per PRD.
"""

from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_cors import CORS
from data_loader import fetch_historical_data, get_close_prices, DataLoaderError
import pandas as pd
import os
import io
import base64

import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend for server-side image generation
matplotlib.rcParams['font.family'] = 'DejaVu Sans'  # Use a Linux-safe font
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"])  # Vite dev server
app.secret_key = os.environ.get('SECRET_KEY')
if not app.secret_key:
    raise ValueError("SECRET_KEY environment variable must be set")

@app.route('/', methods=['GET'])
def index():
    # Check if React build exists, serve it; otherwise fallback to Flask template
    react_build_path = os.path.join(app.static_folder, 'react-build', 'index.html')
    if os.path.exists(react_build_path):
        return app.send_static_file('react-build/index.html')
    else:
        return render_template('index.html')

@app.route('/assets/<path:filename>')
def react_assets(filename):
    return app.send_static_file(f'react-build/assets/{filename}')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        symbols = request.form.getlist('symbols[]')
        weights = request.form.getlist('weights[]')
        start_date = request.form.get('start_date', '').strip()
        end_date = request.form.get('end_date', '').strip()
        capital = request.form.get('capital', '').strip()
        # Validate all fields present
        if not symbols or not weights or not start_date or not end_date or not capital:
            flash('All fields are required.')
            return render_template('index.html'), 200
        if len(symbols) != len(weights):
            flash('Number of symbols and weights must match.')
            return render_template('index.html'), 200
        # Validate weights
        try:
            weights_float = [float(w) for w in weights]
        except ValueError:
            flash('Weights must be numbers.')
            return render_template('index.html'), 200
        if any(w < 0 or w > 1 for w in weights_float):
            flash('Weights must be between 0 and 1.')
            return render_template('index.html'), 200
        if abs(sum(weights_float) - 1.0) > 0.0001:
            flash('Portfolio weights must sum to 1.0.')
            return render_template('index.html'), 200
        # Validate dates
        import re
        date_pattern = r'^\d{4}-\d{2}-\d{2}$'
        if not re.match(date_pattern, start_date) or not re.match(date_pattern, end_date):
            flash('Date format must be YYYY-MM-DD.')
            return render_template('index.html'), 200
        if start_date > end_date:
            flash('Start date must be before end date.')
            return render_template('index.html'), 200
        # Validate capital
        try:
            capital_float = float(capital)
            if capital_float <= 0:
                raise ValueError
        except ValueError:
            flash('Initial capital must be a positive number.')
            return render_template('index.html'), 200
        # Fetch and process data
        data = fetch_historical_data(symbols, start_date, end_date)
        close_prices = get_close_prices(data, symbols)
        # Set date as index and sort for time series analysis
        close_prices['time'] = pd.to_datetime(close_prices['time'])
        close_prices = close_prices.sort_values('time').set_index('time')
        # Portfolio returns calculation (weighted sum of returns)
        returns = close_prices.pct_change().dropna()
        portfolio_returns = (returns * weights_float).sum(axis=1)

        # Generate QuantStats static images (PNG/SVG) using quantstats.reports.full()
        import quantstats as qs
        import matplotlib.pyplot as plt
        import uuid
        # Ensure static directory exists
        static_dir = os.path.join(os.path.dirname(__file__), 'static')
        os.makedirs(static_dir, exist_ok=True)
        # Unique prefix for this analysis
        unique_id = uuid.uuid4().hex[:8]

        # Create charts directory for this session
        charts_dir = os.path.join(static_dir, 'charts')
        os.makedirs(charts_dir, exist_ok=True)
        
        # Generate QuantStats summary snapshot and save as file
        fig = qs.plots.snapshot(portfolio_returns, show=False)
        summary_chart_path = os.path.join(charts_dir, f'{unique_id}_summary.png')
        fig.savefig(summary_chart_path, format='png', bbox_inches='tight', dpi=150)
        plt.close(fig)

        # Generate QuantStats monthly returns heatmap and save as file
        fig = qs.plots.monthly_heatmap(portfolio_returns, show=False)
        monthly_chart_path = os.path.join(charts_dir, f'{unique_id}_monthly.png')
        fig.savefig(monthly_chart_path, format='png', bbox_inches='tight', dpi=150)
        plt.close(fig)

        # Generate QuantStats drawdown plot and save as file
        fig = qs.plots.drawdown(portfolio_returns, show=False)
        drawdown_chart_path = os.path.join(charts_dir, f'{unique_id}_drawdown.png')
        fig.savefig(drawdown_chart_path, format='png', bbox_inches='tight', dpi=150)
        plt.close(fig)

        # Generate QuantStats HTML report
        reports_dir = os.path.join(static_dir, 'reports')
        os.makedirs(reports_dir, exist_ok=True)
        html_report_path = os.path.join(reports_dir, 'quantstats-results.html')
        try:
            qs.reports.html(
                portfolio_returns,
                benchmark=None,
                rf=0.0,
                grayscale=False,
                title='Strategy Tearsheet',
                output=html_report_path,
                compounded=True,
                periods_per_year=252,
                download_filename='quantstats-results.html',
                figfmt='svg',
                template_path=None,
                match_dates=True
            )
        except Exception as report_ex:
            flash(f'Failed to generate QuantStats HTML report: {report_ex}')
            return render_template('index.html'), 200
        # Store results in session with file URLs instead of base64 data
        results_data = {
            'summary_chart_url': f'/static/charts/{unique_id}_summary.png',
            'monthly_chart_url': f'/static/charts/{unique_id}_monthly.png',
            'drawdown_chart_url': f'/static/charts/{unique_id}_drawdown.png',
            'portfolio_symbols': symbols,
            'portfolio_weights': weights,
            'start_date': start_date,
            'end_date': end_date,
            'capital': capital_float,
            'unique_id': unique_id
        }
        session['analysis_results'] = results_data
        
        # Check if request wants JSON response (from React)
        if request.headers.get('Accept') == 'application/json':
            return jsonify({'success': True, 'redirect': '/results'})
        else:
            return redirect(url_for('results'))
    except DataLoaderError as e:
        flash(f"Error fetching data: {str(e)}")
        return render_template('index.html'), 200
    except Exception as ex:
        flash(f'Unexpected error: {ex}')
        return render_template('index.html'), 200

@app.route('/results', methods=['GET'])
def results():
    # Get analysis results from session
    analysis_results = session.get('analysis_results')
    if not analysis_results:
        # Check if request is JSON (from React)
        if request.headers.get('Accept') == 'application/json' or request.is_json:
            return jsonify({'error': 'No analysis results found. Please run an analysis first.'}), 400
        else:
            flash('No analysis results found. Please run an analysis first.')
            return redirect(url_for('index'))
    
    # Check if request wants JSON (from React)
    if request.headers.get('Accept') == 'application/json' or request.is_json:
        return jsonify(analysis_results)
    else:
        # Return HTML template for traditional requests
        return render_template('results.html', 
                             summary_chart_url=analysis_results.get('summary_chart_url'),
                             monthly_chart_url=analysis_results.get('monthly_chart_url'), 
                             drawdown_chart_url=analysis_results.get('drawdown_chart_url'),
                             portfolio_symbols=analysis_results.get('portfolio_symbols'),
                             portfolio_weights=analysis_results.get('portfolio_weights'),
                             start_date=analysis_results.get('start_date'),
                             end_date=analysis_results.get('end_date'),
                             capital=analysis_results.get('capital'))

# Catch-all route for React Router (client-side routing)
@app.route('/<path:path>')
def react_routes(path):
    # Only serve React app for non-API routes
    if not path.startswith('api/') and not path.startswith('static/'):
        react_build_path = os.path.join(app.static_folder, 'react-build', 'index.html')
        if os.path.exists(react_build_path):
            return app.send_static_file('react-build/index.html')
    # For other routes, return 404
    return 'Not found', 404

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port, debug=True)
