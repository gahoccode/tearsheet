# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common Commands

### Development with uv (Preferred)
- **Install dependencies**: `uv sync` (installs all dependencies from pyproject.toml)
- **Run locally**: `uv run python app.py` (starts Flask dev server on port 5000)
- **Run tests**: `uv run pytest tests/` (runs all tests)
- **Run specific test**: `uv run pytest tests/test_app.py::TestClassName::test_method_name`
- **Code formatting**: `uv run ruff format` (formats code using Ruff)
- **Linting**: `uv run ruff check` (checks code quality)
- **Add dependencies**: `uv add package-name` (adds to pyproject.toml)

### Development with pip (Alternative)
- **Activate virtual environment**: `source .venv/bin/activate` (macOS/Linux) or `.venv\Scripts\activate` (Windows)
- **Install dependencies**: `pip install -r requirements.txt` (or `pip install -e .` for pyproject.toml)
- **Run locally**: `python app.py`
- **Run tests**: `pytest tests/`

### Docker
- **Build**: `docker build -t tearsheet .`
- **Run container**: `docker run -p 5000:5000 -e PORT=5000 tearsheet`
- **Docker Compose**: `docker-compose up`

### Production
- **Gunicorn**: `gunicorn app:app --bind 0.0.0.0:${PORT:-5000} --timeout 120`

## Architecture

### Core Application Structure
- **app.py**: Main Flask application with two primary routes:
  - `GET /`: Renders portfolio input form using Bootstrap UI
  - `POST /analyze`: Validates input, fetches data, generates QuantStats tearsheet, redirects to HTML report
- **data_loader.py**: Data fetching module with error handling, uses vnstock API for Vietnam stock market data
- **templates/**: Jinja2 HTML templates with responsive Bootstrap UI
- **static/**: CSS, JavaScript, and dynamically generated reports directory
- **tests/**: Comprehensive unit and integration tests
- **backend/**: Additional backend functionality (separate from main Flask app)

### Data Processing Flow
1. User submits portfolio form with symbols, weights, date range, and initial capital
2. Flask validates all inputs (weights sum to 1.0, valid dates, positive capital)
3. `fetch_historical_data()` calls vnstock's `Quote.history()` for each symbol
4. Data merged on timestamps, close prices extracted for portfolio calculation
5. Portfolio returns computed as weighted sum of individual stock returns
6. QuantStats generates both embedded charts and full HTML tearsheet
7. User redirected to `/static/reports/quantstats-results.html` for complete analysis

### Key Dependencies and Configuration
- **Flask**: Web framework with secret key validation
- **vnstock**: Vietnam stock market API (primary data source)
- **quantstats**: Portfolio analytics, tearsheet generation, and performance metrics
- **pandas**: Time series data manipulation and merging
- **matplotlib**: Chart generation (configured with 'Agg' backend for server-side rendering)
- **tenacity**: Retry logic for API calls
- **gunicorn**: Production WSGI server

### Environment and Deployment
- **Python**: Requires >= 3.10 (specified in pyproject.toml)
- **SECRET_KEY**: Environment variable required for Flask sessions
- **PORT**: Environment variable for deployment (defaults to 5000)
- **uv**: Modern Python package manager with concurrent builds and caching
- **GitHub Container Registry**: Automated Docker image builds on push to main/master

### Error Handling Strategy
- Custom `DataLoaderError` exception for data fetching issues
- Comprehensive input validation with user-friendly flash messages
- Graceful handling of vnstock API failures with specific error messages
- Matplotlib backend configuration prevents GUI-related server errors

### Testing Approach
Tests verify complete request/response cycles, HTML report generation, input edge cases, and matplotlib backend configuration. Uses real vnstock API with valid Vietnamese stock symbols (REE, FMC, DHC) to ensure integration reliability.