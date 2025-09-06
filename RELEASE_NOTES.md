# Release Notes v1.0.0

## 🎉 Initial Release

This is the first major release of Tearsheet - a Vietnam stock portfolio analysis tool built with Flask, vnstock, and QuantStats.

## ✨ Features

- **Portfolio Analysis**: Complete portfolio analytics using Vietnam stock market data via vnstock API
- **Interactive Reports**: Generate comprehensive QuantStats HTML tearsheets with performance metrics
- **Modern UI**: Clean, responsive interface built with Tailwind CSS and Flowbite components
- **Vietnam Market Focus**: Specialized for Vietnam stock market with symbols like REE, FMC, DHC
- **Web Interface**: Simple form-based input for portfolio configuration (symbols, weights, dates, capital)

## 🔧 Technical Highlights

- **UI Migration**: Complete migration from Bootstrap to Tailwind CSS with Flowbite components for modern, responsive design
- **Containerization**: Full Docker support for easy deployment and scaling
- **CI/CD**: GitHub Actions workflow with Container Registry integration
- **Production Ready**: Gunicorn configuration with proper timeout settings
- **Flexible Deployment**: Support for various hosting platforms including Render

## 🚀 Deployment Options

- **Docker**: `docker build -t quantstatswebapp .` and `docker run -p 5000:5000 quantstatswebapp`
- **Docker Compose**: `docker-compose up` for orchestrated deployment
- **Direct**: `python app.py` for local development
- **Production**: `gunicorn app:app --bind 0.0.0.0:${PORT:-5000} --timeout 120`

## 📋 Requirements

- Python 3.10.11
- Flask 3.0.3
- vnstock 3.2.6 (Vietnam stock data API)
- quantstats 0.0.69 (Portfolio analytics)
- Node.js (for CSS build process)

## 🔄 Installation

```bash
# Install Python dependencies
pip install -r requirements.txt

# Install frontend dependencies
npm install

# Build CSS
npx tailwindcss -i ./static/css/input.css -o ./static/css/style.css --minify

# Run application
python app.py
```

## 📊 Usage

1. Navigate to the web interface
2. Enter Vietnam stock symbols (e.g., REE, FMC, DHC)
3. Specify portfolio weights and date range
4. Set initial capital amount
5. Generate comprehensive QuantStats tearsheet report

## 🛠️ Architecture

- **Flask Backend**: Main application server with two primary routes
- **Data Layer**: vnstock API integration for Vietnam market data
- **Analytics Engine**: QuantStats for portfolio performance analysis
- **Frontend**: Tailwind CSS + Flowbite for modern UI components
- **Reports**: Generated HTML tearsheets saved to `static/reports/`

## 📝 Next Steps

This release provides a solid foundation for Vietnam stock portfolio analysis. Future releases may include:
- Additional market support
- Enhanced portfolio optimization features
- User authentication and saved portfolios
- API endpoints for programmatic access

---

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>