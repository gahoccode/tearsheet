# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common Commands

### Development
- **Run locally**: `python app.py` (starts Flask dev server on port 5000)
- **Run all tests**: `pytest` (runs all tests in tests/ directory)
- **Run specific test file**: `pytest tests/test_app.py` or `pytest tests/test_data_loader.py`
- **Run specific test**: `pytest tests/test_app.py::FlaskAppIntegrationTest::test_analyze_valid_redirects_to_html_report`
- **Install dependencies**: `pip install -r requirements.txt` or `uv pip install --all --upgrade --refresh`
- **Install frontend dependencies**: `npm install` (installs Tailwind CSS and Flowbite)
- **Build CSS**: `npx tailwindcss -i ./static/css/input.css -o ./static/css/style.css --minify`
- **Activate virtual environment**: `source .venv/bin/activate` (macOS/Linux) or `.venv\Scripts\activate` (Windows)

### Docker
- **Build**: `docker build -t quantstatswebapp .`
- **Run container**: `docker run -p 5000:5000 -e PORT=5000 quantstatswebapp`
- **Docker Compose**: `docker-compose up`

### Production
- **Gunicorn**: `gunicorn app:app --bind 0.0.0.0:${PORT:-5000} --timeout 120`

## Architecture

### Core Components
- **app.py**: Main Flask application with two routes:
  - `GET /`: Renders portfolio input form
  - `POST /analyze`: Processes portfolio data, generates QuantStats report, redirects to HTML tearsheet
- **data_loader.py**: Data fetching module using vnstock API for Vietnam stock market data
- **templates/**: HTML templates (Bootstrap UI)
- **static/**: CSS, JS, and generated reports directory
- **tests/**: Integration and unit tests

### Data Flow
1. User submits portfolio via web form (symbols, weights, dates, capital)
2. Flask validates input and calls `fetch_historical_data()` from data_loader
3. vnstock API fetches Vietnam stock data via `Quote.history()`
4. Portfolio returns calculated using weighted sum of individual stock returns
5. QuantStats generates interactive HTML report saved to `static/reports/quantstats-results.html`
6. User redirected to view the complete tearsheet report

### Key Dependencies
- **Flask**: Web framework
- **vnstock**: Vietnam stock market data API
- **quantstats**: Portfolio analytics and tearsheet generation
- **pandas**: Data manipulation
- **matplotlib**: Chart generation (backend set to 'Agg' for server-side rendering)

### Environment Requirements
- Python 3.10.11 (exact version specified in pyproject.toml)
- SECRET_KEY environment variable required for Flask sessions
- PORT environment variable for deployment (defaults to 5000)
- Virtual environment strongly recommended

### Testing Strategy
Tests verify routing behavior, HTML report generation, input validation, and matplotlib backend configuration. All tests use real vnstock API calls with valid Vietnam stock symbols like REE, FMC, DHC.

### Important Notes
- **Matplotlib backend**: Must be set to 'Agg' at the top of app.py for server-side rendering
- **Vietnam stock symbols**: Use valid Vietnam stock tickers (REE, FMC, DHC, etc.) for testing
- **Report output**: Generated HTML reports are saved to `static/reports/quantstats-results.html`