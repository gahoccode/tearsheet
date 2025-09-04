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
  - `POST /api/tearsheet`: QuantStats HTML tearsheet generation
  - `POST /api/validate`: Input validation
  - `POST /api/ratios`: Financial ratios analysis
- **src/**: Modular service architecture with core business logic
- **tests/**: Integration and unit tests

### Frontend Components (Next.js)
- **Next.js 15**: App Router with Server Components and Turbopack
- **TypeScript**: Full type safety throughout the application
- **Tailwind CSS**: Utility-first responsive design
- **TanStack Query**: Advanced data fetching and caching
- **React Hook Form + Zod**: Form handling with schema validation

### Data Flow
1. User interacts with Next.js frontend at http://localhost:3000
2. Frontend validates input using React Hook Form + Zod schemas
3. API requests sent to Flask backend at http://localhost:5001 (CORS enabled)
4. Flask API validates input and processes portfolio data
5. vnstock API fetches Vietnam stock data via `Quote.history()`
6. Portfolio returns calculated using weighted sum of individual stock returns
7. QuantStats generates complete HTML tearsheet with embedded visualizations
8. JSON response sent back to frontend with HTML content
9. Frontend renders tearsheet using React's dangerouslySetInnerHTML

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
- **shadcn/ui**: Modern component library with black/white theme
- **next-themes**: Theme switching and dark mode support
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

### QuantStats HTML Tearsheet Implementation

#### Tearsheet Generation (Backend)
- **File**: `backend/api.py` - `/api/tearsheet` endpoint
- **Purpose**: Generates complete QuantStats HTML tearsheets using `qs.reports.html()`
- **Process**: 
  - Creates temporary HTML file
  - Generates comprehensive tearsheet with all visualizations
  - Returns HTML content as JSON response
  - Cleans up temporary files automatically
- **Features**:
  - Professional financial report formatting
  - Built-in performance charts and metrics
  - Comprehensive risk analysis visualizations
  - Industry-standard tearsheet layout

#### Tearsheet Display Component (Frontend)
- **File**: `frontend/src/components/QuantStatsTearsheet.tsx`
- **Purpose**: Displays QuantStats HTML content in React application
- **Implementation**: Uses `dangerouslySetInnerHTML` for HTML rendering
- **Features**: 
  - Responsive design with proper styling
  - Error handling and loading states
  - Professional tearsheet presentation
  - TypeScript support with proper interfaces

#### Integration Benefits
- **Simplicity**: Single API endpoint vs. multiple chart endpoints
- **Performance**: No heavy client-side chart libraries
- **Reliability**: Proven QuantStats library with consistent output
- **Professional Quality**: Industry-standard financial tearsheet format

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
- **Tearsheet Rendering**: QuantStats HTML display accuracy

#### Full Stack Testing
- **End-to-End**: Complete user workflows from form submission to tearsheet display
- **Cross-Origin**: CORS configuration between frontend and backend
- **Error Handling**: Graceful error handling across both applications

## Lessons Learned

### Architecture Decisions
- **Simplicity Over Complexity**: Choose proven solutions (QuantStats) over custom implementations (Plotly.js)
- **Library Evaluation**: Thoroughly evaluate existing solutions before building custom components
- **Microservices Benefits**: Independent frontend/backend development and deployment
- **TypeScript Value**: Full type safety significantly improves development experience

### Implementation Best Practices
- **API Design**: Single-purpose endpoints are easier to maintain than complex multi-function APIs
- **HTML Generation**: Server-side HTML generation (QuantStats) is more reliable than client-side chart libraries
- **Error Handling**: Multi-layer validation (client + server) provides better user experience
- **Cleanup Strategy**: Always clean up temporary files and unused dependencies

### Development Workflow
- **Dual Terminal Setup**: Running frontend and backend in separate terminals enables efficient development
- **Environment Variables**: Proper environment configuration prevents CORS and connectivity issues
- **Testing Strategy**: Test both individual services and full stack integration
- **Documentation**: Keep architecture documentation updated with implementation changes

### shadcn/ui Integration with TailwindCSS v4.0

#### TailwindCSS v4.0 CSS-First Configuration
- **Configuration approach**: Uses CSS-first configuration with `@theme` directive in `globals.css`
- **No JavaScript config**: TailwindCSS v4.0 eliminates the need for `tailwind.config.js/ts` files
- **Built-in PostCSS**: Uses `@tailwindcss/postcss` plugin in `postcss.config.mjs`
- **CSS Variables**: Theme tokens defined directly in CSS using `--color-*` naming convention

#### Installation Commands
- **Manual shadcn/ui setup**: Install dependencies manually since CLI has compatibility issues with TailwindCSS v4.0
- **Core dependencies**: `npm install @radix-ui/react-label @radix-ui/react-slot class-variance-authority next-themes lucide-react`
- **Component creation**: Create components manually using shadcn/ui patterns

#### Component Setup
- **Utils file**: `src/lib/utils.ts` - Contains `cn()` utility for class merging with clsx/tailwind-merge
- **Components directory**: `src/components/ui/` - Houses manually created shadcn/ui components
- **Theme configuration**: 
  - Uses TailwindCSS v4.0 `@theme` directive for CSS variables
  - Class-based dark mode with `.dark` selector for next-themes compatibility
  - Black/white theme with proper contrast ratios
- **Theme Provider**: `next-themes` for seamless dark/light mode switching

#### TailwindCSS v4.0 Specific Considerations
- **CSS Variable Format**: Use `--color-*` format instead of plain variable names
- **Dark Mode**: Use `.dark` class selector instead of `@media (prefers-color-scheme: dark)`
- **No JavaScript Config**: All configuration happens in CSS using `@theme` blocks

#### Common TypeScript Issues and Fixes
- **Table component types**: Use `React.HTMLAttributes<HTMLTableCellElement>` for TableHead, not `React.ThHTMLAttributes` (which doesn't exist)
- **Select component**: Use standard `React.SelectHTMLAttributes<HTMLSelectElement>` interface
- **Component refs**: Always use proper HTML element types for forwardRef components

## Troubleshooting Guide

### Frontend Server Won't Start

#### Symptoms
- `npm run dev` appears to start but frontend is not accessible on port 3000
- Connection timeout errors when accessing http://localhost:3000
- Server process appears to run but no actual HTTP service

#### Investigation Process
1. **Check for existing processes**: `lsof -ti:3000` to see if port is already in use
2. **Run with verbose output**: Use debug flags to see actual error output instead of assuming server is up
3. **Check configuration files**: Verify all config files are properly formatted
4. **Test direct Next.js**: Try `npx next dev --port 3000` to bypass npm scripts

#### Root Cause Discovery (TailwindCSS v4.0 Configuration Conflicts)
- **Problem**: Mixed TailwindCSS v3 and v4 configurations causing CSS compilation failures
- **Evidence**: CSS compilation errors prevent server from fully starting
- **Files involved**: `tailwind.config.ts` (deprecated) vs `globals.css` (@theme directive)

#### Resolution Steps
1. **Remove deprecated config**: Delete `tailwind.config.ts` file completely
2. **Update PostCSS**: Ensure `postcss.config.mjs` uses `@tailwindcss/postcss`
3. **Fix globals.css**: Use proper `@theme` directive with CSS variables
4. **Test compilation**: Verify CSS compiles without errors

### shadcn/ui Installation Issues

#### Symptoms
- `npx shadcn-ui@latest init` fails or hangs
- CLI can't find configuration files
- Component installation commands don't work

#### Root Cause
- shadcn/ui CLI expects JavaScript configuration file (`tailwind.config.js`)
- TailwindCSS v4.0 uses CSS-first configuration without JavaScript config
- CLI incompatibility with modern TailwindCSS approach

#### Workaround Process
1. **Manual dependency installation**: Install required packages manually
   ```bash
   npm install @radix-ui/react-label @radix-ui/react-slot class-variance-authority next-themes lucide-react
   ```
2. **Create utils manually**: Set up `src/lib/utils.ts` with cn() function
3. **Copy component code**: Manually create components in `src/components/ui/`
4. **Adapt for project**: Modify components to work with TailwindCSS v4.0

### TypeScript Compilation Errors

#### Debugging TypeScript Errors
1. **Use TypeScript compiler directly**: `npx tsc --noEmit` to see all errors
2. **Check component by component**: Isolate errors to specific files
3. **Verify React types**: Ensure using correct React DOM element types
4. **Test in isolation**: Create minimal component to test type definitions

### Key Learning: Always Check Latest Documentation
- **Critical moment**: When facing configuration issues, always research latest version practices
- **Discovery**: TailwindCSS v4.0 eliminated JavaScript config files entirely
- **Lesson**: Don't assume compatibility - verify CLI tool compatibility with your stack

### Debugging Methodology That Worked
1. **Question assumptions**: Don't assume server is running just because command appears to execute
2. **Use verbose output**: Always check actual error output when troubleshooting
3. **Systematic investigation**: Check each layer - configuration, dependencies, compilation
4. **Research current practices**: Use Context7 to get latest documentation when stuck
5. **Test incrementally**: Make one change at a time to isolate issues
- **Built-in Features**: Container queries, nesting, and modern CSS features included by default