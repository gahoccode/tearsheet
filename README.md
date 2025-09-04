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
- **TypeScript**: Full type safety throughout the application
- **Tailwind CSS**: Utility-first responsive design
- **React Query**: Advanced data fetching and state management
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
Create `.env` file in backend directory:
```bash
SECRET_KEY=your-secret-key-here
PORT=5001
```

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
Create `.env.local` file in frontend directory:
```bash
NEXT_PUBLIC_API_URL=http://localhost:5001
NODE_ENV=development
```

4. **Start Next.js development server**:
```bash
npm run dev
```

Frontend will be available at http://localhost:3000

### Full Stack Development

Run both servers simultaneously:
- **Terminal 1**: `cd backend && PORT=5001 uv run python api.py`
- **Terminal 2**: `cd frontend && npm run dev`

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
