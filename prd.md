Create a Python-based web application with the following specifications:

**Framework & Libraries:**
- Backend: Flask
- Frontend: HTML, CSS, Bootstrap
- Data Loader: `vnstock` (to fetch Vietnam stock prices)
- Analysis: `QuantStats` (for performance metrics, tear sheets, plots)

**Frontend Structure:**

1. **HTML Templates (in `templates/` folder):**
   - `index.html`:
     - Form fields:
       - List of stock tickers (textarea or tag-based input)
       - Date range: start date and end date (date inputs)
       - Initial capital (numeric input)
     - Bootstrap-powered responsive layout
     - Submits form data to `/analyze` via POST
   - `results.html`:
     - Displays portfolio performance metrics (returns, volatility, Sharpe, drawdowns)
     - Embeds charts and/or tear sheet visuals from QuantStats
     - Bootstrap layout for summary stats and graphics

2. **Static Assets (in `static/` folder):**
   - `css/style.css`: Custom styles for layout, charts, forms
   - `js/script.js`: UI interactivity and input validation (e.g., check ticker format, date range logic)

**Backend Structure (`app.py`):**
- `/`: Renders `index.html`
- `/analyze`: 
   - Receives user input
   - Uses `vnstock` to fetch historical data for selected tickers
   - Simulates equal-weight portfolio or custom logic
   - Computes portfolio returns
   - Uses `quantstats` to generate:
     - Key performance stats (Sharpe, Sortino, max drawdown)
     - HTML tear sheet (saved to `templates/qs_report.html`)
     - Plots (saved to static folder and rendered in `results.html`)
   - Returns `results.html` with embedded performance visuals and stats

**Testing (`tests/test_app.py`):**
- Unit tests:
   - Data fetching from `vnstock` for various edge cases (invalid ticker, market holiday gaps)
   - Portfolio return calculation logic
   - QuantStats output parsing and file generation
- Integration tests:
   - Route validation (`/`, `/analyze`)
   - POST request behavior with valid/invalid inputs
- Frontend tests (optional):
   - Validation logic on client side
   - Test rendering of metrics and embedded visualizations

**User Experience:**
- Bootstrap-based responsive layout
- Interactive charts (optional: download or zoom)
- Clear display of portfolio health and performance over time
- Tear sheet download option for detailed offline review