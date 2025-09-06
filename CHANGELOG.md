# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2.0.0] - 2025-09-06
### Added
- **Modern React Frontend**: Complete Vite + React + Ant Design frontend application
- **Dual Interface Support**: Both modern React SPA and legacy HTML templates supported
- **Portfolio Form Component**: Modern form with Ant Design components, real-time validation
- **Results Display Component**: Interactive results page with embedded charts
- **Client-side Routing**: React Router for seamless navigation between form and results
- **File-based Chart Storage**: Charts now saved as static PNG files instead of base64 session data
- **CORS Support**: Flask-CORS integration for React development server
- **Content Negotiation**: Dual response handling (JSON for React, HTML for legacy)
- **Production Build System**: Vite builds React app to Flask static directory
- **Chart File Serving**: Dedicated routes for serving chart images
- **Development Workflow**: Hot reload React development with Flask API backend
- **Responsive Design**: Mobile-first design with Ant Design's grid system
- **Form Validation**: Client-side validation with Ant Design Form components
- **Loading States**: Proper loading indicators during analysis processing
- **Error Handling**: Comprehensive error handling with user-friendly messages

### Changed
- **Port Convention**: Flask now runs on port 5001 (was 5000) to avoid macOS conflicts
- **Session Storage**: Results stored as file URLs instead of base64 data (294KB → <1KB)
- **Chart Generation**: Enhanced chart quality with 150 DPI and improved formatting
- **Asset Serving**: React build automatically served by Flask when available
- **API Endpoints**: All routes now support both JSON and HTML responses
- **Documentation**: Comprehensive technical troubleshooting guide added to CLAUDE.md
- **Development Commands**: Updated for dual React/Flask development workflow

### Fixed
- **Vite Proxy Header Overflow**: Resolved HTTP header size limits causing proxy errors
- **Session Cookie Size**: Eliminated 294KB session cookies exceeding browser limits  
- **Port Conflicts**: Fixed macOS AirPlay Receiver conflicts on port 5000
- **CORS Issues**: Added proper CORS configuration for React-Flask communication
- **Asset Routing**: Fixed React Router fallbacks and static asset serving
- **Import Order**: Standardized Python and JavaScript import conventions

### Technical Details
- **Frontend Stack**: Vite 7.1.4, React 19.1.1, Ant Design 5.27.3, React Router 7.8.2
- **Build Output**: `npm run build` outputs to `/static/react-build/`
- **Chart Storage**: Charts saved to `/static/charts/{unique_id}_{type}.png`
- **Proxy Configuration**: Vite dev server proxies API calls to Flask backend
- **Session Optimization**: Reduced session size by 99.7% (294KB → <1KB)

## [1.0.0] - 2025-09-05
### Added
- **Flask Backend**: Core Flask application with portfolio analysis
- **QuantStats Integration**: Portfolio analytics and tearsheet generation
- **Vietnam Stock Data**: vnstock API integration for historical price data
- **Portfolio Analysis**: Weighted return calculations and risk metrics
- **HTML Templates**: Bootstrap-styled templates for portfolio input and results
- **Static Chart Generation**: PNG chart generation with matplotlib
- **Form Validation**: Server-side validation for portfolio inputs
- **HTML Report Generation**: Full QuantStats HTML tearsheet reports
- **Docker Support**: Containerization with GitHub Container Registry workflow
- **Testing Suite**: Integration and unit tests for core functionality
- **Environment Configuration**: .env file support for configuration
- **Static File Serving**: CSS, JS, and generated reports
- **Error Handling**: Comprehensive error handling and user feedback

### Technical Details
- **Backend Stack**: Flask 3.0.3, QuantStats 0.0.69, vnstock 3.2.6, pandas 2.2.2
- **Chart Generation**: matplotlib with 'Agg' backend for server-side rendering
- **Data Processing**: Portfolio returns calculation with weighted sum approach
- **Report Output**: HTML reports saved to `/static/reports/quantstats-results.html`
- **Testing**: pytest with real vnstock API calls for Vietnam stock symbols (REE, FMC, DHC)

### Changed (Historical)
- Project renamed to "tearsheet"
- UI framework from Bootstrap to custom CSS styling (later to React + Ant Design)
- Matplotlib font to DejaVu Sans for Linux compatibility
- Dependencies updated to latest versions

### Fixed (Historical)
- Server-side rendering issues with matplotlib backend set to 'Agg'
- Cross-platform deployment compatibility

## [1.0.0] - 2025-09-05
### Added
- **Flask Backend**: Core Flask application with portfolio analysis
- **QuantStats Integration**: Portfolio analytics and tearsheet generation
- **Vietnam Stock Data**: vnstock API integration for historical price data
- **Portfolio Analysis**: Weighted return calculations and risk metrics
- **HTML Templates**: Bootstrap-styled templates for portfolio input and results
- **Static Chart Generation**: PNG chart generation with matplotlib
- **Form Validation**: Server-side validation for portfolio inputs
- **HTML Report Generation**: Full QuantStats HTML tearsheet reports
- **Docker Support**: Containerization with GitHub Container Registry workflow
- **Testing Suite**: Integration and unit tests for core functionality
- **Environment Configuration**: .env file support for configuration
- **Static File Serving**: CSS, JS, and generated reports
- **Error Handling**: Comprehensive error handling and user feedback
- **Claude Code Integration**: Configuration and documentation
- **GitHub Container Registry (GHCR) workflow**: Automated Docker builds
- **Render.com deployment**: Cloud deployment configuration

### Technical Details
- **Backend Stack**: Flask 3.0.3, QuantStats 0.0.69, vnstock 3.2.6, pandas 2.2.2
- **Chart Generation**: matplotlib with 'Agg' backend for server-side rendering
- **Data Processing**: Portfolio returns calculation with weighted sum approach
- **Report Output**: HTML reports saved to `/static/reports/quantstats-results.html`
- **Testing**: pytest with real vnstock API calls for Vietnam stock symbols (REE, FMC, DHC)

[Unreleased]: https://github.com/gahoccode/tearsheet/compare/v2.0.0...HEAD
[2.0.0]: https://github.com/gahoccode/tearsheet/compare/v1.0.0...v2.0.0
[1.0.0]: https://github.com/gahoccode/tearsheet/releases/tag/v1.0.0
