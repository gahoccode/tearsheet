# Tearsheet

A modern Python web application for Vietnam stock portfolio analysis using Flask, vnstock, and QuantStats with a sleek Tailwind CSS + Flowbite UI.

**🎉 Version 1.0.0 - Production Ready**

## ✨ Features
- 📊 **Vietnam Stock Analysis**: Fetches historical price data for Vietnam stock tickers using vnstock API
- 📈 **Portfolio Analytics**: Computes comprehensive metrics (returns, Sharpe ratio, drawdown, volatility)
- 📋 **Interactive Reports**: Generates beautiful QuantStats HTML tearsheets with charts and analysis
- 🎨 **Modern UI**: Responsive design built with Tailwind CSS and Flowbite components
- 🐳 **Container Ready**: Full Docker support for easy deployment
- 🔧 **Production Deployment**: GitHub Actions CI/CD with Container Registry integration
- ✅ **Comprehensive Testing**: Integrated tests verify routing, report generation, and system functionality

## 🏗️ Project Structure
```
├── app.py                          # Flask application with routing logic
├── data_loader.py                  # Vietnam stock data fetching via vnstock
├── templates/                      # HTML templates with Tailwind CSS
│   ├── index.html                  # Portfolio input form
│   └── results.html               # Results page
├── static/                        # Static assets
│   ├── css/                       # Tailwind CSS files
│   ├── js/                        # JavaScript files  
│   └── reports/                   # Generated QuantStats reports
├── tests/                         # Comprehensive test suite
├── RELEASE_NOTES.md               # Version history and changes
└── CLAUDE.md                      # Development guidance
```

## 🚀 Quick Start

### Prerequisites
- Python 3.10.11
- Node.js (for CSS build process)
- Git

### 1. Clone and Setup
```bash
git clone <repository-url>
cd tearsheet

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# or .venv\Scripts\activate  # Windows

# Install Python dependencies
pip install -r requirements.txt
# or using uv: uv pip install --all --upgrade --refresh

# Install frontend dependencies
npm install
```

### 2. Build Assets
```bash
# Build CSS (required for proper styling)
npx tailwindcss -i ./static/css/input.css -o ./static/css/style.css --minify

# For development with auto-rebuild:
npm run build-css
```

### 3. Run Application
```bash
python app.py
```

Visit http://127.0.0.1:5001 to access the portfolio analyzer.

### 4. Example Usage
1. Enter Vietnam stock symbols (e.g., `REE`, `FMC`, `DHC`)
2. Set portfolio weights and date range
3. Specify initial capital
4. Click "Analyze Portfolio" to generate your QuantStats tearsheet

## Data Loader Usage

The data loader is implemented in `data_loader.py`:

```python
from data_loader import fetch_historical_data, get_close_prices
symbols = ['REE', 'FMC', 'DHC']
data = fetch_historical_data(symbols, '2024-01-01', '2024-03-19')
close_prices = get_close_prices(data, symbols)
```

## 🧪 Testing
Run the comprehensive test suite to verify functionality:

```bash
# Run all tests
pytest

# Run specific test files
pytest tests/test_app.py
pytest tests/test_data_loader.py

# Run with verbose output
pytest -v

# Run specific test
pytest tests/test_app.py::FlaskAppIntegrationTest::test_analyze_valid_redirects_to_html_report
```

**Test Coverage:**
- Flask routing and request handling
- Portfolio data processing and validation
- QuantStats report generation
- Matplotlib backend configuration
- vnstock API integration with real Vietnam stock data

## 🔧 Technical Requirements
- **Python**: 3.10.11 (exact version specified for consistency)
- **Node.js**: For CSS build process (Tailwind CSS compilation)
- **Environment Variables**:
  - `SECRET_KEY`: Required for Flask sessions
  - `PORT`: Deployment port (defaults to 5001)

## Troubleshooting & Notes
- **Matplotlib GUI errors:** The backend is set to `'Agg'` for server-side image generation. If you see errors about "main thread is not in main loop", ensure this setting is present at the top of `app.py`:
  ```python
  import matplotlib
  matplotlib.use('Agg')
  ```
- **Navigation:** For best UX, add a "Back to Home" button/link in the QuantStats HTML report pointing to `/`.
- **Static report cleanup:** The generated HTML report (`static/reports/quantstats-results.html`) may be overwritten on each new analysis.

## 🐳 Container Deployment

### Local Docker Development
```bash
# Build the image
docker build -t tearsheet .

# Run locally
docker run -p 5001:5001 -e PORT=5001 tearsheet

# Using Docker Compose
docker-compose up
```

### GitHub Container Registry (GHCR) 

Automated CI/CD workflow builds and publishes Docker images to GHCR on every push to main branch.

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
docker pull ghcr.io/{your-username}/tearsheet:latest
```

#### Run the container

```bash
docker run -p 5001:5001 -e PORT=5001 ghcr.io/{your-username}/tearsheet:latest
```

#### Manual Build (Optional)

If you want to build locally:

```bash
docker build -t tearsheet .
docker run -p 5001:5001 -e PORT=5001 tearsheet
```

## 📋 Release History

**v1.0.0** (Current) - Initial Production Release
- ✨ Complete UI migration to Tailwind CSS + Flowbite components
- 🐳 Full Docker containerization support  
- 🔧 GitHub Actions CI/CD pipeline
- 📊 Production-ready Vietnam stock portfolio analytics
- ✅ Comprehensive testing suite
- 📚 Complete documentation and setup guides

See [RELEASE_NOTES.md](RELEASE_NOTES.md) for detailed changelog.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes and test thoroughly
4. Build CSS assets: `npx tailwindcss -i ./static/css/input.css -o ./static/css/style.css --minify`
5. Run tests: `pytest`
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## License
MIT
