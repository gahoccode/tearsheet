# QuantstatsWebApp

A modern web application for Vietnam stock portfolio analysis featuring a React frontend with Ant Design and Flask backend using vnstock and quantstats.

## Features
- **Modern React UI**: Built with Vite, React Router, and Ant Design components
- **Dual Interface**: Both modern React SPA and legacy HTML templates supported
- **Real-time Analysis**: Fetches historical price data for Vietnam stock tickers using vnstock
- **Interactive Results**: Displays portfolio performance metrics, charts, and downloadable QuantStats HTML tearsheet
- **Responsive Design**: Mobile-first design with Ant Design's responsive grid system
- **Form Validation**: Client-side and server-side validation for portfolio inputs
- **Session Management**: Results stored in Flask sessions for seamless user experience

## Project Structure
- **app.py**: Flask backend with JSON API and HTML template support
- **frontend/**: Vite React application with Ant Design components
  - **src/components/**: React components (PortfolioForm, ResultsPage)
  - **src/App.jsx**: Main app with routing configuration
- **data_loader.py**: Data fetching module for Vietnam stock data
- **templates/**: Legacy HTML templates (Flask/Jinja2)
- **static/**: Static assets, CSS, JS, generated reports, and React build output
- **tests/**: Unit and integration tests

## Setup Instructions

### Backend Setup

1. **Create and activate a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows
```

2. **Install Python dependencies**
```bash
pip install uv
uv pip install --all --upgrade --refresh
```

3. **Set environment variables**
```bash
export SECRET_KEY=your-secret-key-here
```

### Frontend Setup

1. **Install Node.js dependencies**
```bash
cd frontend
npm install
```

2. **Build React app for production** (optional)
```bash
npm run build
```

### Development

#### Option 1: React Development (Recommended)
```bash
# Terminal 1: Start Flask backend
python app.py

# Terminal 2: Start React frontend  
cd frontend && npm run dev
```
- Flask API: http://localhost:5001
- React App: http://localhost:5173

#### Option 2: Flask-only Development
```bash
python app.py
```
- Full app: http://localhost:5001

### Production
The React app builds to `/static/react-build/` and is automatically served by Flask when built.

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
- `PORT`: Port to run the application on (default: 5001)

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for detailed version history and release notes.

## License
MIT
