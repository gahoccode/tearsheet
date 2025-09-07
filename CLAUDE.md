# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common Commands

### Development

#### Python Environment Setup
- **Create virtual environment**: `python -m venv venv`
- **Activate virtual environment**: `source venv/bin/activate` (macOS/Linux) or `venv\Scripts\activate` (Windows)
- **Install Python dependencies**: `uv pip install --all --upgrade --refresh`
- **Install dev dependencies**: `uv pip install --group dev`

#### Running the Application

##### React + Flask Development (Recommended)
- **Run Flask backend**: `python app.py` (starts Flask API server on port 5001)
- **Run React frontend**: `cd frontend && npm run dev` (starts Vite dev server on port 5173)
- **Install React dependencies**: `cd frontend && npm install`
- **Build React for production**: `cd frontend && npm run build` (builds to `/static/react-build/`)

##### Flask-only Development
- **Run Flask backend only**: `python app.py` (starts Flask dev server on port 5001, serves HTML templates)

#### Code Quality and Testing
- **Run all tests**: `pytest` or `pytest tests/`
- **Run specific test**: `pytest tests/test_app.py::TestClassName::test_method_name`
- **Test coverage**: `pytest --cov=. tests/`
- **Lint Python code**: `ruff check .`
- **Format Python code**: `black .` and `isort .`
- **Lint React code**: `cd frontend && npm run lint`
- **Type checking**: `mypy .`

### Docker
- **Build**: `docker build -t quantstatswebapp .`
- **Run container**: `docker run -p 5001:5001 -e PORT=5001 quantstatswebapp`
- **Docker Compose**: `docker-compose up`

### Production
- **Gunicorn**: `gunicorn app:app --bind 0.0.0.0:${PORT:-5001} --timeout 120`

### Package Management
- **Root package.json scripts**:
  - `npm run dev:frontend`: Start React dev server
  - `npm run dev:backend`: Start Flask backend
  - `npm run build`: Build React for production
  - `npm run changelog`: Generate changelog from commits
  - `npm run changelog:all`: Generate full changelog

## Architecture

### Core Components
- **app.py**: Flask application serving both HTML templates (legacy) and JSON API:
  - `GET /`: Serves React build or Flask template
  - `POST /analyze`: Processes portfolio data, returns JSON or redirects 
  - `GET /results`: Returns analysis results as JSON or HTML
- **frontend/**: Vite React application with Ant Design components
  - **PortfolioForm**: Portfolio input form with validation
  - **ResultsPage**: Displays charts and analysis results
- **data_loader.py**: Data fetching module using vnstock API for Vietnam stock market data
- **templates/**: HTML templates (legacy Flask UI)
- **static/**: CSS, JS, generated reports, and React build directory
- **tests/**: Integration and unit tests

### Data Flow (React)
1. User submits portfolio via React form (Ant Design components)
2. React sends FormData to Flask `/analyze` endpoint with JSON Accept header
3. Flask validates input and calls `fetch_historical_data()` from data_loader
4. vnstock API fetches Vietnam stock data via `Quote.history()`
5. Portfolio returns calculated using weighted sum of individual stock returns
6. QuantStats generates charts as base64 images and HTML report
7. Results stored in Flask session and returned to React
8. React displays charts inline and provides link to full HTML report

### Data Flow (Legacy)
1. User submits portfolio via HTML form
2. Flask processes form data and redirects to results page
3. Results displayed via Flask template with embedded charts

### Key Dependencies

#### Backend (Python)
- **Flask**: Web framework with CORS support
- **vnstock**: Vietnam stock market data API
- **quantstats**: Portfolio analytics and tearsheet generation
- **pandas**: Data manipulation
- **matplotlib**: Chart generation (backend set to 'Agg' for server-side rendering)

#### Frontend (React)
- **Vite**: Build tool and dev server
- **React**: UI framework with Router for client-side routing  
- **Ant Design**: Component library for forms, charts, and UI elements
- **axios**: HTTP client for API requests
- **dayjs**: Date manipulation library

### Environment Requirements
- Python >= 3.10 (as specified in pyproject.toml)
- SECRET_KEY environment variable required for Flask sessions
- PORT environment variable for deployment (defaults to 5001)
- Node.js for React frontend development

### Testing Strategy
Tests verify routing behavior, HTML report generation, input validation, and matplotlib backend configuration. All tests use real vnstock API calls with valid Vietnam stock symbols like REE, FMC, DHC.

## Code Style Guidelines

### Python Import Order
Always place imports at the top of Python files in the proper order:
1. Standard library imports (e.g., `import os`, `import sys`)
2. Third-party library imports (e.g., `import pandas`, `from flask import Flask`)  
3. Local application imports (e.g., `from data_loader import fetch_historical_data`)

### JavaScript/React Import Order
Always place imports at the top of JavaScript/React files in the proper order:
1. React and Node.js built-in imports (e.g., `import { useState } from 'react'`)
2. Third-party library imports (e.g., `import axios from 'axios'`, `import { Button } from 'antd'`)
3. Local imports (e.g., `import './App.css'`, `import Component from './Component'`)

### Commit Message Convention
Follow conventional commits for automatic changelog generation:

```bash
# Format: <type>(<scope>): <description>
feat(frontend): add portfolio form validation
fix(backend): resolve session cookie overflow
docs(readme): update setup instructions
style(components): format React components with prettier
refactor(api): reorganize Flask route handlers
test(integration): add portfolio analysis tests
chore(deps): update dependencies to latest versions
```

**Types**:
- `feat`: New features
- `fix`: Bug fixes  
- `docs`: Documentation changes
- `style`: Code formatting (no functional changes)
- `refactor`: Code restructuring (no functional changes)
- `test`: Adding or updating tests
- `chore`: Maintenance tasks (deps, build, etc.)

**Changelog Generation**:
```bash
# Generate changelog from commits
npm run changelog

# Generate full changelog 
npm run changelog:all
```

## Technical Issues and Solutions

### Issue 1: Vite Proxy Header Overflow Error
**Problem**: When running React dev server with Vite proxy, got error:
```
[vite] http proxy error: /analyze
Error: Parse Error: Header overflow
```

**Root Cause**: 
- QuantStats base64-encoded chart data was ~294KB per analysis
- Flask stored base64 charts in session cookies: `session['analysis_results']['summary_chart'] = 'iVBORw0KGgoAAAANSUhEUgAA...'`
- HTTP header size limit is 4KB for most browsers
- Session cookie exceeded limits: `294703 bytes but the limit is 4093 bytes`
- Vite proxy couldn't handle oversized headers during `/analyze` requests

**Solution**:
1. **Chart File Storage**: Modified Flask to save charts as static PNG files instead of base64 in session:
   ```python
   # Before: Stored base64 in session (294KB)
   summary_img_base64 = base64.b64encode(buf.read()).decode('utf-8')
   session['analysis_results']['summary_chart'] = summary_img_base64
   
   # After: Save as file and store URL (few bytes)
   summary_chart_path = os.path.join(charts_dir, f'{unique_id}_summary.png')
   fig.savefig(summary_chart_path, format='png', bbox_inches='tight', dpi=150)
   session['analysis_results']['summary_chart_url'] = f'/static/charts/{unique_id}_summary.png'
   ```

2. **Frontend Updates**: Updated React components to use image URLs:
   ```javascript
   // Before: Base64 data URLs
   <img src={`data:image/png;base64,${results.summary_chart}`} />
   
   // After: Static file URLs  
   <img src={results.summary_chart_url} />
   ```

3. **Flask Template Updates**: Updated Jinja2 templates to use file URLs instead of base64

**Result**: Session size reduced from 294KB to <1KB, eliminating header overflow errors

### Issue 2: Port Conflicts and Server Binding
**Problem**: 
- Flask defaulted to port 5000, conflicted with macOS AirPlay Receiver
- Vite dev server couldn't bind to localhost properly

**Solution**:
1. **Port Convention**: Changed Flask default from 5000 to 5001:
   ```python
   # .env file
   PORT=5001
   
   # app.py
   port = int(os.environ.get("PORT", 5001))  # Changed from 5000
   ```

2. **Vite Proxy Configuration**: Updated proxy targets:
   ```javascript
   // vite.config.js
   server: {
     proxy: {
       '/analyze': 'http://localhost:5001',  // Changed from 5000
       '/results': 'http://localhost:5001',
       '/static': 'http://localhost:5001',
     }
   }
   ```

3. **Server Binding**: Used explicit host binding for Vite:
   ```bash
   npx vite --host 127.0.0.1 --port 5173
   ```

### Issue 3: CORS and Content-Type Handling
**Problem**: React frontend couldn't communicate with Flask backend due to missing CORS headers and content-type issues

**Solution**:
1. **CORS Setup**: Added Flask-CORS with specific origin:
   ```python
   from flask_cors import CORS
   CORS(app, origins=["http://localhost:5173"])  # Vite dev server
   ```

2. **Content Negotiation**: Implemented dual response handling based on Accept headers:
   ```python
   # Check if request wants JSON (from React)
   if request.headers.get('Accept') == 'application/json':
       return jsonify(analysis_results)
   else:
       return render_template('results.html', ...)
   ```

3. **Frontend Headers**: Added explicit Accept headers in React:
   ```javascript
   const response = await axios.post('/analyze', formData, {
     headers: { 'Accept': 'application/json' }
   })
   ```

### Issue 4: Build Configuration and Asset Serving
**Problem**: React build output needed to be served by Flask for production deployment

**Solution**:
1. **Vite Build Configuration**: Output React build to Flask static directory:
   ```javascript
   // vite.config.js
   build: {
     outDir: '../static/react-build',
     emptyOutDir: true,
   }
   ```

2. **Flask Routing**: Added routes to serve React assets:
   ```python
   @app.route('/')
   def index():
       # Check if React build exists, serve it; otherwise fallback
       react_build_path = os.path.join(app.static_folder, 'react-build', 'index.html')
       if os.path.exists(react_build_path):
           return app.send_static_file('react-build/index.html')
       return render_template('index.html')
   
   @app.route('/assets/<path:filename>')
   def react_assets(filename):
       return app.send_static_file(f'react-build/assets/{filename}')
   
   # Catch-all for React Router
   @app.route('/<path:path>')
   def react_routes(path):
       if not path.startswith('api/') and not path.startswith('static/'):
           return app.send_static_file('react-build/index.html')
   ```