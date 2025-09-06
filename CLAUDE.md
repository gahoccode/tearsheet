# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common Commands

### Development
- **Run locally**: `python app.py` (starts Flask dev server on port 5001)
- **Run all tests**: `pytest` (runs all tests in tests/ directory)
- **Run specific test file**: `pytest tests/test_app.py` or `pytest tests/test_data_loader.py`
- **Run specific test**: `pytest tests/test_app.py::FlaskAppIntegrationTest::test_analyze_valid_redirects_to_html_report`
- **Install dependencies**: `pip install -r requirements.txt` or `uv pip install --all --upgrade --refresh`
- **Install frontend dependencies**: `npm install` (installs Tailwind CSS and Flowbite)
- **Build CSS**: `npx tailwindcss -i ./static/css/input.css -o ./static/css/style.css --minify`
- **Activate virtual environment**: `source .venv/bin/activate` (macOS/Linux) or `.venv\Scripts\activate` (Windows)

### Docker
- **Build**: `docker build -t tearsheet .`
- **Run container**: `docker run -p 5001:5001 -e PORT=5001 tearsheet`
- **Docker Compose**: `docker-compose up`

### Production
- **Gunicorn**: `gunicorn app:app --bind 0.0.0.0:${PORT:-5001} --timeout 120`

## Architecture

### Core Components
- **app.py**: Main Flask application with two routes:
  - `GET /`: Renders portfolio input form
  - `POST /analyze`: Processes portfolio data, generates QuantStats report, redirects to HTML tearsheet
- **data_loader.py**: Data fetching module using vnstock API for Vietnam stock market data
- **templates/**: HTML templates (Tailwind CSS + Flowbite UI)
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
- **Tailwind CSS**: Utility-first CSS framework for styling
- **Flowbite**: Component library built on Tailwind CSS

### Environment Requirements
- Python 3.10.11 (exact version specified in pyproject.toml)
- SECRET_KEY environment variable required for Flask sessions
- PORT environment variable for deployment (defaults to 5001)
- Virtual environment strongly recommended

### Testing Strategy
Tests verify routing behavior, HTML report generation, input validation, and matplotlib backend configuration. All tests use real vnstock API calls with valid Vietnam stock symbols like REE, FMC, DHC.

### Important Notes
- **Port Configuration**: ALWAYS use port 5001 for this project (default changed from 5000 to avoid conflicts)
- **Matplotlib backend**: Must be set to 'Agg' at the top of app.py for server-side rendering
- **Vietnam stock symbols**: Use valid Vietnam stock tickers (REE, FMC, DHC, etc.) for testing
- **Report output**: Generated HTML reports are saved to `static/reports/quantstats-results.html`

## Release Management

### Version Control
- Current version: 1.0.0 (specified in pyproject.toml and package.json)
- Use semantic versioning (MAJOR.MINOR.PATCH)
- Create annotated tags for releases: `git tag -a v1.0.0 -m "Release message"`

### Release Process
1. Update version numbers in pyproject.toml and package.json
2. Create comprehensive release notes in RELEASE_NOTES.md
3. Run tests to ensure functionality
4. Build CSS assets: `npx tailwindcss -i ./static/css/input.css -o ./static/css/style.css --minify`
5. Commit changes and create release tag
6. Push to remote with tags: `git push origin main && git push origin v1.0.0`

## UI Framework Migration Notes

### Tailwind CSS + Flowbite Implementation
- **CSS Build Process**: Use `npx tailwindcss -i ./static/css/input.css -o ./static/css/style.css --minify` for production builds
- **Flowbite Components**: Leverages pre-built components for forms, alerts, and responsive layouts
- **Custom Configuration**: See tailwind.config.js for project-specific theming and Flowbite integration
- **Color Palette**: Uses primary colors (blue) and semantic colors (red for errors, green for success)

### Best Practices Discovered
- **CSS Watch Mode**: Use `npm run build-css` for development with --watch flag
- **Component Consistency**: Maintain consistent spacing (p-4, mb-6, etc.) across components
- **Responsive Design**: Leverage Tailwind's responsive prefixes (sm:, md:, lg:) for mobile-first design
- **Error Handling**: Use Flowbite alert components for user feedback and validation errors

## Development Workflow Lessons

### Release Preparation Best Practices
1. **Version Synchronization**: Always ensure version numbers match across pyproject.toml and package.json
2. **Asset Building**: CSS must be built before testing UI changes: `npx tailwindcss -i ./static/css/input.css -o ./static/css/style.css --minify`
3. **Release Documentation**: Comprehensive release notes improve project maintainability and user understanding
4. **Tag Management**: Use annotated tags with detailed messages for better release tracking

### CSS Framework Migration Insights
- **Build Process**: Tailwind requires compilation step, unlike Bootstrap CDN approach
- **Component Integration**: Flowbite provides pre-built components that reduce custom CSS needs
- **Configuration**: tailwind.config.js centralizes theming and component imports
- **Development Experience**: Watch mode significantly improves development velocity during UI work

### Testing Considerations
- **Real API Integration**: Tests use actual vnstock API calls, requiring network connectivity
- **Backend Configuration**: Matplotlib 'Agg' backend essential for headless server environments
- **File Generation**: Tests verify actual HTML report generation, not just HTTP responses

### Deployment Architecture
- **Multi-Environment Support**: Configuration supports local development, Docker, and cloud deployment
- **Asset Management**: Static files require proper serving configuration in production
- **Environment Variables**: SECRET_KEY and PORT provide deployment flexibility