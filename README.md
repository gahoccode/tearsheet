# Tearsheet

A modern Python web application for Vietnam stock portfolio analysis using Flask, vnstock, and QuantStats with a full-width responsive Bootstrap 5 interface.

## ✨ Features
- **Full-Width Responsive Design**: Modern Bootstrap 5 UI with flexible layout optimization
- **Enhanced User Experience**: Side-by-side form layout with large controls and comprehensive validation
- **Vietnam Stock Data**: Fetches historical price data using vnstock API for Vietnamese stocks
- **Advanced Portfolio Analytics**: Comprehensive performance metrics, Sharpe ratio, drawdown analysis
- **Interactive Tearsheet**: Direct HTML injection of QuantStats reports with full viewport utilization
- **Mobile-First Design**: Responsive across all device sizes with adaptive scaling
- **Real-time Validation**: Enhanced form validation with user-friendly feedback
- **Professional Charts**: Performance summary, monthly returns heatmap, and drawdown analysis

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

## Container Deployment with GHCR

### GitHub Container Registry (GHCR) Workflow

This repository includes an automated workflow to build and publish Docker images to GitHub Container Registry (GHCR) on every push to `main` or `master` branches.

#### How it works
- **Trigger**: Workflow runs automatically on push to main/master branches
- **Build**: Uses Docker Buildx for multi-platform builds
- **Publish**: Pushes to `ghcr.io/{username}/quantstatswebapp`
- **Tags**: Includes branch name, commit SHA, and `latest` for main branch

#### Usage

1. **Enable GitHub Packages**: Ensure GitHub Packages is enabled for your repository
2. **Set Permissions**: The workflow automatically uses `GITHUB_TOKEN` for authentication
3. **View Images**: Published images appear in your repository's "Packages" section

#### Pull the image

```bash
docker pull ghcr.io/{your-username}/quantstatswebapp:latest
```

#### Run the container

```bash
docker run -p 5000:5000 -e PORT=5000 ghcr.io/{your-username}/quantstatswebapp:latest
```

#### Manual Build (Optional)

If you want to build locally:

```bash
docker build -t quantstatswebapp .
docker run -p 5000:5000 -e PORT=5000 quantstatswebapp
```

### Environment Variables

The container accepts the following environment variables:
- `PORT`: Port to run the application on (default: 5000)

## License
MIT
