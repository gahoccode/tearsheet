# QuantstatsWebApp

A Python web application for Vietnam stock portfolio analysis using Flask, vnstock, and quantstats.

## Features
- Fetches historical price data for user-selected Vietnam stock tickers using vnstock
- Simulates portfolio performance and computes key metrics (returns, Sharpe, drawdown, etc.)
- Generates interactive charts and downloadable QuantStats HTML tear sheet
- Responsive Bootstrap UI
- **/analyze** route generates a QuantStats HTML report and redirects users to `/static/reports/quantstats-results.html` for a full tear sheet
- "Back to Home" navigation is recommended for user-friendly return to the main page
- Integrated tests verify routing, HTML file creation, and Matplotlib backend

## Project Structure
- app.py: Flask backend (**implemented**)
- data_loader.py: Data loader for historical prices (**implemented**)
- templates/: HTML templates (**implemented**)
- static/: CSS and JS (**implemented**)
- tests/: Unit and integration tests (**implemented**)

## Setup Instructions

### 1. Create and activate a virtual environment (Windows, Command Prompt)

```cmd
python -m venv venv
venv\Scripts\activate
```

### 2. Install dependencies

```cmd
pip install -r requirements.txt
```

Alternatively, using uv:

```cmd
pip install uv
uv pip install --all --upgrade --refresh
```

### 3. Run the app

```cmd
python app.py
```

The app will be available at http://127.0.0.1:5000

After analyzing a portfolio, you will be redirected to a full QuantStats HTML report (tear sheet) at `/static/reports/quantstats-results.html`.

## Data Loader Usage

The data loader is implemented in `data_loader.py`:

```python
from data_loader import fetch_historical_data, get_close_prices
symbols = ['REE', 'FMC', 'DHC']
data = fetch_historical_data(symbols, '2024-01-01', '2024-03-19')
close_prices = get_close_prices(data, symbols)
```

## Testing
- Unit and integration tests are located in `tests/`
- Tests verify:
  - Routing and redirection to the QuantStats HTML report
  - HTML report file creation
  - Matplotlib backend is set to 'Agg' (for server-side rendering)

To run all tests:

```cmd
pytest tests/test_app.py
```

## Python Version
- Requires Python >= 3.9

## Troubleshooting & Notes
- **Matplotlib GUI errors:** The backend is set to `'Agg'` for server-side image generation. If you see errors about "main thread is not in main loop", ensure this setting is present at the top of `app.py`:
  ```python
  import matplotlib
  matplotlib.use('Agg')
  ```
- **Navigation:** For best UX, add a "Back to Home" button/link in the QuantStats HTML report pointing to `/`.
- **Static report cleanup:** The generated HTML report (`static/reports/quantstats-results.html`) may be overwritten on each new analysis.

## License
MIT
