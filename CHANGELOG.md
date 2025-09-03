# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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