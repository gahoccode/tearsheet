# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common Commands

### Ground Rules
- **Imports placement**: Always place imports on top of the file.
- **Code formatting and linting**: Use `uv run ruff format` for code formatting and `uv run ruff check --fix` for fixing linting errors automatically.
- **Dependency management**: Keep both `requirements.txt` and `pyproject.toml` consistent when adding new dependencies.

### Development

#### Backend Development (Flask API)
- **Run backend**: `cd backend && PORT=5001 uv run python api.py` (starts Flask API on port 5001)
- **Run tests**: `cd backend && pytest tests/test_app.py` (runs all tests)
- **Install dependencies**: `cd backend && uv pip install --all --upgrade --refresh`
- **Activate virtual environment**: `source .venv/bin/activate` (macOS/Linux)

#### Frontend Development (Next.js)
- **Run frontend**: `cd frontend && npm run dev` (starts Next.js dev server on port 3000)
- **Install dependencies**: `cd frontend && npm install`
- **Build for production**: `cd frontend && npm run build`
- **Type checking**: `cd frontend && npm run type-check`
- **Linting**: `cd frontend && npm run lint`

#### Full Stack Development
- **Start both servers**: Run backend and frontend in separate terminals
  - Terminal 1: `cd backend && PORT=5001 uv run python api.py`
  - Terminal 2: `cd frontend && npm run dev`
- **Access application**: Frontend at http://localhost:3000, API at http://localhost:5001

### Docker
- **Build**: `docker build -t quantstatswebapp .`
- **Run container**: `docker run -p 5000:5000 -e PORT=5000 quantstatswebapp`
- **Docker Compose**: `docker-compose up`

### Production
- **Gunicorn**: `gunicorn app:app --bind 0.0.0.0:${PORT:-5000} --timeout 120`

## Architecture

### Modern Next.js + Flask API Architecture
The application follows a **modern full-stack architecture** with complete separation of frontend and backend:

```
tearsheet/
├── backend/           # Flask API server (Port 5001)
│   ├── api.py        # Main API endpoints
│   ├── src/          # Core business logic
│   └── tests/        # API tests
└── frontend/         # Next.js application (Port 3000)
    ├── src/          # React components & utilities
    └── public/       # Static assets
```

### Backend Components (Flask API)
- **api.py**: JSON API endpoints:
  - `GET /api/health`: Health check
  - `POST /api/analyze`: Portfolio analysis
  - `POST /api/validate`: Input validation
  - `POST /api/ratios`: Financial ratios analysis
- **src/**: Modular service architecture with core business logic
- **tests/**: Integration and unit tests

### Frontend Components (Next.js)
- **Next.js 15**: App Router with Server Components and Turbopack
- **TypeScript**: Full type safety throughout the application
- **Tailwind CSS**: Utility-first responsive design
- **Plotly.js**: Interactive chart library with advanced visualizations
- **React Query**: Advanced data fetching and caching
- **React Hook Form + Zod**: Form handling with schema validation

### Data Flow
1. User interacts with Next.js frontend at http://localhost:3000
2. Frontend validates input using React Hook Form + Zod schemas
3. API requests sent to Flask backend at http://localhost:5001 (CORS enabled)
4. Flask API validates input and processes portfolio data
5. vnstock API fetches Vietnam stock data via `Quote.history()`
6. Portfolio returns calculated using weighted sum of individual stock returns
7. JSON response sent back to frontend with metrics and analysis data
8. Frontend renders interactive charts and analytics using Plotly.js

### Key Dependencies

#### Backend Dependencies
- **Flask**: JSON API web framework with Flask-CORS for cross-origin requests
- **vnstock**: Vietnam stock market data API integration
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computations for portfolio analysis
- **matplotlib**: Chart generation (backend set to 'Agg' for server-side rendering)
- **uv**: Modern Python package manager

#### Frontend Dependencies
- **Next.js 15**: React framework with App Router and Server Components
- **React 19**: Latest React with improved performance
- **TypeScript**: Type safety and development experience
- **Tailwind CSS 4**: Utility-first CSS framework
- **Plotly.js**: Interactive chart library with advanced visualizations (v2.35.2)
- **TanStack Query**: Data fetching, caching, and state management
- **React Hook Form**: Form handling with performance optimization
- **Zod**: TypeScript-first schema validation
- **Axios**: HTTP client for API requests

### Environment Requirements

#### Backend Requirements
- Python >= 3.9
- SECRET_KEY environment variable required for Flask sessions
- PORT environment variable (use 5001 for local development)
- uv package manager installed

#### Frontend Requirements  
- Node.js >= 18
- npm or yarn package manager
- NEXT_PUBLIC_API_URL environment variable (http://localhost:5001 for development)

#### Development Environment Variables
**Backend (.env):**
```bash
SECRET_KEY=your-secret-key-here
PORT=5001
```

**Frontend (.env.local):**
```bash
NEXT_PUBLIC_API_URL=http://localhost:5001
NODE_ENV=development
NEXT_PUBLIC_API_TIMEOUT=30000
```

### Plotly.js Chart Implementation

#### Chart Data Service (Backend)
- **File**: `backend/src/services/chart_data_service.py`
- **Purpose**: Generates Plotly chart data configurations instead of HTML
- **Returns**: JSON objects with `data` and `layout` properties for frontend consumption
- **Chart Types**:
  - Portfolio Performance: Line chart showing cumulative returns over time
  - Drawdown Analysis: Area chart displaying portfolio drawdowns
  - Portfolio Composition: Pie chart with asset allocation percentages
  - Metrics Dashboard: Bar chart with key performance indicators

#### Dynamic Plotly Component (Frontend)
- **File**: `frontend/src/components/charts/DynamicPlotlyChart.tsx`
- **CDN Version**: Plotly.js v2.35.2 (loads dynamically from CDN)
- **Features**: 
  - Responsive design with automatic resizing
  - Interactive controls (zoom, pan, hover tooltips)
  - Error handling with fallback UI
  - TypeScript support with proper type definitions
- **Usage**: Accepts `data`, `layout`, and optional `config` props

#### Chart Integration Notes
- **Backend Response**: API returns chart configurations as JSON objects
- **Frontend Rendering**: Charts render client-side using dynamically loaded Plotly.js
- **Performance**: CDN loading reduces bundle size, charts cached after first load
- **Compatibility**: Works with React 19 and Next.js 15 with Turbopack

### Testing Strategy

#### Backend Testing
- **API Integration Tests**: Verify JSON endpoint responses and error handling  
- **Service Layer Tests**: Test portfolio analysis calculations and data validation
- **External API Tests**: Real vnstock API calls with valid Vietnam stock symbols (REE, FMC, DHC)
- **Data Serialization Tests**: Ensure proper JSON serialization of pandas objects

#### Frontend Testing
- **Component Testing**: React component rendering and user interactions
- **API Integration**: Frontend-to-backend API communication
- **Form Validation**: Client-side validation with Zod schemas
- **Chart Rendering**: Plotly.js visualization accuracy

#### Full Stack Testing
- **End-to-End**: Complete user workflows from form submission to chart display
- **Cross-Origin**: CORS configuration between frontend and backend
- **Error Handling**: Graceful error handling across both applications