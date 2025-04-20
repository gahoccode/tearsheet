# QuantstatsWebApp

A Python web application for Vietnam stock portfolio analysis using Flask, vnstock, and quantstats.

## Features
- Fetches historical price data for user-selected Vietnam stock tickers using vnstock
- Simulates portfolio performance and computes key metrics (returns, Sharpe, drawdown, etc.)
- Generates interactive charts and quantstats tear sheet
- Responsive Bootstrap UI

## Project Structure
- app.py: Flask backend (to be implemented)
- data_loader.py: Data loader for historical prices
- templates/: HTML templates (to be implemented)
- static/: CSS and JS (to be implemented)
- tests/: Unit and integration tests (to be implemented)

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

### 3. Run the app (after implementing app.py)

```cmd
python app.py
```

## Data Loader Usage

The data loader is implemented in `data_loader.py`:

```python
from data_loader import fetch_historical_data, get_close_prices
symbols = ['REE', 'FMC', 'DHC']
data = fetch_historical_data(symbols, '2024-01-01', '2024-03-19')
close_prices = get_close_prices(data, symbols)
```

## Testing
- Unit and integration tests will be placed in `tests/`

## Python Version
- Requires Python >= 3.9

## License
MIT
