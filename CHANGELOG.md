# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **shadcn/ui Integration**: Modern, accessible UI components with black/white theme
- **TailwindCSS v4.0**: CSS-first configuration using @theme directive
- **Dark/Light Theme Toggle**: Seamless theme switching with next-themes
- **TypeScript Component Types**: Proper type definitions for all UI components

### Changed
- **UI Framework**: Complete transformation to shadcn/ui component system
- **Theme Configuration**: Migrated to TailwindCSS v4.0 CSS-first approach
- **Component Architecture**: All forms, tables, and UI elements now use shadcn/ui patterns
- **Ratios Page**: Full shadcn/ui transformation with proper TypeScript types

### Fixed
- **TypeScript Errors**: Resolved table component type definition issues
- **TailwindCSS Configuration**: Fixed v3/v4 configuration conflicts
- **Component Compatibility**: Ensured all components work with TailwindCSS v4.0

### Documentation
- **CLAUDE.md Updates**: Added TailwindCSS v4.0 integration guide and common TypeScript fixes

## [2.1.0] - 2025-01-04
### Changed
- **Visualization Approach**: Replaced complex Plotly.js charts with simple QuantStats HTML tearsheet rendering
- **Frontend Simplification**: Simplified React components to display QuantStats-generated HTML reports using dangerouslySetInnerHTML
- **Backend API**: Added new `/api/tearsheet` endpoint that generates complete HTML tearsheets using `qs.reports.html()`
- **Component Architecture**: Created streamlined `QuantStatsTearsheet` component for HTML display

### Removed
- **Plotly.js Dependencies**: Removed plotly.js and react-plotly.js packages from frontend
- **Custom Chart Components**: Eliminated DynamicPlotlyChart and PlotlyChart components
- **Chart Data Services**: Removed ChartDataService and related chart data processing
- **Complex Visualizations**: Simplified from custom interactive charts to proven QuantStats tearsheets

### Fixed
- **Performance**: Improved rendering performance by eliminating heavy Plotly.js bundle
- **Reliability**: Enhanced stability using proven QuantStats HTML generation instead of custom chart implementations

## [2.0.0] - 2025-01-03
### Added
- **Modern Next.js Frontend**: Complete Next.js 15 application with App Router and Server Components
- **TypeScript Integration**: Full type safety throughout the frontend application
- **Interactive Visualizations**: Recharts-based charts replacing static HTML reports
- **Real-time Data Fetching**: TanStack Query (React Query) for advanced data fetching and caching
- **Modern UI Framework**: Tailwind CSS 4 utility-first responsive design
- **Form Validation**: React Hook Form with Zod schema validation
- **Financial Ratios Page**: Comprehensive financial ratios analysis interface
- **API Health Checks**: Backend health monitoring endpoints
- **CORS Support**: Cross-origin resource sharing for API communication
- **Error Boundaries**: Comprehensive error handling across frontend and backend
- **Development Tooling**: ESLint, Prettier, and TypeScript configuration
- **Production Optimization**: Next.js build optimization with Turbopack

### Changed
- **Architecture**: Transformed from monolithic Flask SSR to modern Next.js + Flask API microservices
- **Data Flow**: JSON API communication replacing server-side rendering
- **Port Configuration**: Backend moved to port 5001 (avoiding macOS AirPlay conflicts)
- **Visualization Engine**: Replaced static QuantStats reports with interactive Recharts
- **Directory Structure**: Separated backend/ and frontend/ directories
- **Development Workflow**: Dual-terminal development with independent frontend/backend servers
- **Documentation**: Updated architecture documentation and development guides

### Removed
- **Server-side Rendering**: Replaced Flask templates with React components
- **Static HTML Reports**: Removed QuantStats HTML tearsheet generation
- **Bootstrap Dependency**: Replaced with Tailwind CSS
- **Monolithic Structure**: Split into microservices architecture

### Fixed
- **JSON Serialization**: Resolved pandas Timestamp serialization issues in API responses
- **Data Structure**: Fixed portfolio symbols data structure mismatch
- **Cross-origin Requests**: Proper CORS configuration between frontend and backend
- **Type Safety**: Eliminated runtime type errors with comprehensive TypeScript integration

## [1.0.0] - 2024-08-01
### Added
- Initial release of tearsheet application
- Flask web application with portfolio input form
- vnstock integration for Vietnam stock market data
- QuantStats integration for portfolio analytics and tearsheet generation
- Historical price data fetching for Vietnamese stocks (REE, FMC, DHC)
- Portfolio performance calculation with weighted returns
- Interactive HTML tearsheet generation
- Form validation for portfolio weights, dates, and capital
- Static file serving for CSS, JS, and generated reports
- Error handling and user feedback system
- Python virtual environment support
- Requirements.txt with core dependencies

### Security
- SECRET_KEY environment variable requirement for Flask sessions
- Input validation for all form fields
- Safe file handling for generated reports