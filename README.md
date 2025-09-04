# Vietnam Stock Portfolio Analyzer

A modern full-stack application for analyzing Vietnamese stock portfolios with comprehensive QuantStats tearsheet reports and performance metrics.

## Architecture

This application follows a modern **Next.js + Flask API** architecture with complete separation of frontend and backend:

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

## Features

### 📊 Portfolio Analysis
- **QuantStats Tearsheets**: Professional HTML reports with comprehensive analytics
- **Risk Metrics**: Sharpe ratio, volatility, maximum drawdown analysis
- **Performance Tracking**: Returns, win rate, risk assessment
- **Vietnamese Market Data**: Real-time integration with vnstock API
- **Interactive Interface**: Modern React-based portfolio input forms

### 🎨 Modern Frontend
- **Next.js 15**: App Router with Server Components and Turbopack
- **React 19**: Latest React with improved performance
- **TypeScript**: Full type safety throughout the application
- **TailwindCSS v4.0**: CSS-first configuration with @theme directive
- **shadcn/ui**: Modern, accessible component library with black/white theme
- **next-themes**: Seamless dark/light mode theme switching
- **TanStack Query**: Advanced data fetching and state management
- **React Hook Form + Zod**: Form handling with schema validation

### 🔧 Robust Backend
- **Flask API**: JSON-only endpoints with CORS support
- **QuantStats Integration**: Complete HTML tearsheet generation using `qs.reports.html()`
- **Data Validation**: Comprehensive input validation and error handling
- **Modular Architecture**: Clean separation of concerns

## Development Setup

### Prerequisites
- Python >= 3.9
- Node.js >= 18
- uv (Python package manager)
- npm or yarn

### Quick Start

1. **Clone and setup environment files**:
```bash
# Backend environment
cd backend
cp .env.example .env
# Edit .env and generate SECRET_KEY: python -c "import secrets; print(secrets.token_hex(32))"

# Frontend environment  
cd ../frontend
cp .env.example .env.local
# Edit .env.local if needed (defaults should work for development)
```

2. **Install dependencies and start servers**:
```bash
# Terminal 1 - Backend
cd backend && uv pip install --all --upgrade --refresh && PORT=5001 uv run python api.py

# Terminal 2 - Frontend  
cd frontend && npm install && npm run dev
```

3. **Access the application**:
- Frontend: http://localhost:3000
- Backend API: http://localhost:5001

### Backend Setup

1. **Navigate to backend directory**:
```bash
cd backend
```

2. **Install dependencies**:
```bash
uv pip install --all --upgrade --refresh
```

3. **Set environment variables**:
```bash
# Copy example environment file and configure
cp .env.example .env
```

Then edit `.env` file and update the values:
- Generate a secure `SECRET_KEY` using: `python -c "import secrets; print(secrets.token_hex(32))"`
- Verify `PORT=5001` (recommended to avoid macOS AirPlay conflicts)
- Set appropriate Flask environment settings

4. **Start Flask API**:
```bash
PORT=5001 uv run python api.py
```

Backend will be available at http://localhost:5001

### Frontend Setup

1. **Navigate to frontend directory**:
```bash
cd frontend
```

2. **Install dependencies**:
```bash
npm install
```

3. **Set environment variables**:
```bash
# Copy example environment file and configure
cp .env.example .env.local
```

Then edit `.env.local` file and update the values:
- Verify `NEXT_PUBLIC_API_URL=http://localhost:5001` matches backend port
- Adjust timeout and theme settings as needed
- All variables starting with `NEXT_PUBLIC_` are accessible in client-side code

4. **Start Next.js development server**:
```bash
npm run dev
```

Frontend will be available at http://localhost:3000

### Full Stack Development

Run both servers simultaneously:
- **Terminal 1**: `cd backend && PORT=5001 uv run python api.py`
- **Terminal 2**: `cd frontend && npm run dev`

## Environment Configuration

### Production Environment Variables

#### Backend Production (`.env`)
```bash
# Production Flask settings
SECRET_KEY=your-production-secret-key-32-characters-minimum
PORT=5000
FLASK_ENV=production
FLASK_DEBUG=false

# Optional: Database settings (if using database)
# DATABASE_URL=postgresql://user:password@host:port/database

# Optional: Monitoring and logging
# LOG_LEVEL=INFO
# SENTRY_DSN=your-sentry-dsn-here
```

#### Frontend Production (`.env.production` or deployment platform)
```bash
# Production API URL
NEXT_PUBLIC_API_URL=https://your-backend-domain.com

# Next.js optimizations
NODE_ENV=production

# Optional: Analytics and monitoring
# NEXT_PUBLIC_ANALYTICS_ID=your-analytics-id
# NEXT_PUBLIC_SENTRY_DSN=your-sentry-dsn
```

### Environment File Security

**Important Security Notes:**
- ⚠️ **Never commit `.env` files to version control**
- ✅ Add `.env*` to `.gitignore` file
- ✅ Use different SECRET_KEY values for development and production
- ✅ Generate secure random strings for SECRET_KEY (minimum 32 characters)
- ✅ Use environment variables in deployment platforms (Vercel, Railway, etc.)

**Generate Secure SECRET_KEY:**
```python
# Python method to generate secure key
import secrets
print(secrets.token_hex(32))
```

```bash
# Or use openssl
openssl rand -hex 32
```

Access the application at http://localhost:3000

## API Endpoints

### Backend API (Port 5001)
- `GET /api/health`: Health check endpoint
- `POST /api/validate`: Validate portfolio input data
- `POST /api/tearsheet`: Generate QuantStats HTML tearsheet
- `POST /api/ratios`: Financial ratios analysis

### Example API Usage

```python
# Generate tearsheet
response = requests.post('http://localhost:5001/api/tearsheet', json={
    'symbols': ['REE', 'FMC', 'DHC'],
    'weights': [0.4, 0.3, 0.3],
    'capital': 100000000,
    'start_date': '2024-01-01',
    'end_date': '2024-12-31',
    'name': 'My Portfolio'
})
```

## Testing

### Backend Testing
```bash
cd backend && pytest tests/test_app.py
```

### Frontend Testing
```bash
cd frontend && npm run type-check
cd frontend && npm run lint
```

### Full Integration Test
1. Start both servers
2. Visit http://localhost:3000
3. Submit portfolio analysis form
4. Verify QuantStats tearsheet displays correctly

## Technical Details

### Data Flow
1. User submits portfolio form in Next.js frontend
2. Frontend validates input using Zod schemas
3. API request sent to Flask backend at `/api/tearsheet`
4. Backend fetches Vietnam stock data via vnstock API
5. QuantStats generates complete HTML tearsheet using `qs.reports.html()`
6. HTML content returned to frontend as JSON response
7. Frontend renders tearsheet using `dangerouslySetInnerHTML`

### Key Technologies
- **Backend**: Flask + vnstock + QuantStats + pandas
- **Frontend**: Next.js 15 + React 19 + TypeScript + Tailwind CSS
- **Data**: Vietnamese stock market data via vnstock API
- **Visualization**: QuantStats HTML tearsheets with built-in charts

## Troubleshooting

### Common Issues
- **Port conflicts**: Backend uses 5001, frontend uses 3000 (avoiding macOS AirPlay)
- **CORS errors**: Ensure `NEXT_PUBLIC_API_URL=http://localhost:5001` in frontend `.env.local`
- **API timeout**: Large portfolios may take time to process - timeout set to 30s
- **Stock symbols**: Use Vietnamese stock symbols (REE, FMC, DHC, etc.)

## Deployment

### Docker Deployment

```bash
# Build the application
docker build -t tearsheet-app .

# Run with environment variables
docker run -p 5000:5000 -e PORT=5000 tearsheet-app
```

### Production Environment Variables

**Backend**:
```bash
SECRET_KEY=your-production-secret-key
PORT=5001
FLASK_ENV=production
```

**Frontend**:
```bash
NEXT_PUBLIC_API_URL=https://your-api-domain.com
NODE_ENV=production
```

### GitHub Container Registry (GHCR)

Automated builds available at `ghcr.io/{username}/quantstatswebapp:latest`:

```bash
docker pull ghcr.io/{your-username}/quantstatswebapp:latest
docker run -p 5000:5000 -e PORT=5000 ghcr.io/{your-username}/quantstatswebapp:latest
```

## License
MIT
