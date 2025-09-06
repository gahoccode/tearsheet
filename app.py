"""
app.py
Flask backend for QuantstatsWebApp.
Implements '/' and '/analyze' routes per PRD.
"""

from flask import Flask, render_template, request, redirect, url_for, flash, session
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
app.secret_key = os.environ.get('SECRET_KEY')
if not app.secret_key:
    raise ValueError("SECRET_KEY environment variable must be set")

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

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

        # Generate QuantStats summary snapshot
        fig = qs.plots.snapshot(portfolio_returns, show=False)
        buf = io.BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        summary_img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        plt.close(fig)

        # Generate QuantStats monthly returns heatmap
        fig = qs.plots.monthly_heatmap(portfolio_returns, show=False)
        buf = io.BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        monthly_img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        plt.close(fig)

        # Generate QuantStats drawdown plot
        fig = qs.plots.drawdown(portfolio_returns, show=False)
        buf = io.BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        drawdown_img_base64 = base64.b64encode(buf.read()).decode('utf-8')
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
        # Store analysis metadata in session (not the large image data)
        session['analysis_results'] = {
            'symbols': symbols,
            'weights': weights_float,
            'start_date': start_date,
            'end_date': end_date,
            'capital': capital_float,
            'timestamp': str(pd.Timestamp.now())
        }
        
        # Save images to temporary files
        import tempfile
        import json
        temp_dir = os.path.join('static', 'temp')
        os.makedirs(temp_dir, exist_ok=True)
        
        temp_data = {
            'summary_img': summary_img_base64,
            'monthly_img': monthly_img_base64,
            'drawdown_img': drawdown_img_base64
        }
        
        # Create a unique filename based on session
        import hashlib
        session_id = hashlib.md5(str(session.get('analysis_results', {})).encode()).hexdigest()[:10]
        temp_file = os.path.join(temp_dir, f'analysis_{session_id}.json')
        
        with open(temp_file, 'w') as f:
            json.dump(temp_data, f)
        
        session['temp_file'] = f'analysis_{session_id}.json'
        return redirect(url_for('results'))
    except DataLoaderError as e:
        flash(f"Error fetching data: {str(e)}")
        return render_template('index.html'), 200
    except Exception as ex:
        flash(f'Unexpected error: {ex}')
        return render_template('index.html'), 200

@app.route('/results', methods=['GET'])
def results():
    try:
        # Get results from session
        analysis_results = session.get('analysis_results')
        temp_file_name = session.get('temp_file')
        
        if not analysis_results or not temp_file_name:
            flash('No analysis results found. Please run a new analysis.')
            return redirect(url_for('index'))
        
        # Load image data from temporary file
        import json
        temp_file_path = os.path.join('static', 'temp', temp_file_name)
        summary_img = ''
        monthly_img = ''
        drawdown_img = ''
        
        if os.path.exists(temp_file_path):
            with open(temp_file_path, 'r') as f:
                temp_data = json.load(f)
                summary_img = temp_data.get('summary_img', '')
                monthly_img = temp_data.get('monthly_img', '')
                drawdown_img = temp_data.get('drawdown_img', '')
        
        # Extract metadata from session
        symbols = analysis_results.get('symbols', [])
        weights = analysis_results.get('weights', [])
        start_date = analysis_results.get('start_date', '')
        end_date = analysis_results.get('end_date', '')
        capital = analysis_results.get('capital', 0)
        
        # Read the QuantStats HTML file content directly
        html_report_path = os.path.join('static', 'reports', 'quantstats-results.html')
        quantstats_html_content = ""
        if os.path.exists(html_report_path):
            with open(html_report_path, 'r', encoding='utf-8') as f:
                quantstats_html_content = f.read()
        
        return render_template('results.html',
                             summary_img=summary_img,
                             monthly_img=monthly_img,
                             drawdown_img=drawdown_img,
                             symbols=symbols,
                             weights=weights,
                             start_date=start_date,
                             end_date=end_date,
                             capital=capital,
                             quantstats_html_content=quantstats_html_content)
    except Exception as e:
        flash(f'Error displaying results: {e}')
        return redirect(url_for('index'))

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
