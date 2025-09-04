# System Context

## Overview

The Tearsheet Portfolio Analyzer is a modern **microservices-based** financial analysis application that provides comprehensive portfolio performance analysis for Vietnam stock market securities. It features a Next.js frontend and Flask API backend, enabling users to generate professional QuantStats HTML tearsheets and examine detailed financial ratios using the vnstock API.

## System Purpose and Scope

### Primary Functions
- **Portfolio Analysis**: Generate comprehensive QuantStats HTML tearsheet reports with performance metrics
- **Financial Ratio Analysis**: Analyze fundamental financial metrics for Vietnamese securities
- **Modern UI**: React-based responsive interface with TypeScript and Tailwind CSS
- **Real-time Processing**: Instant portfolio analysis with live data fetching

### Target Users
- **Individual Investors**: Personal portfolio analysis and stock research
- **Financial Advisors**: Client portfolio reporting and analysis
- **Research Analysts**: Fundamental analysis of Vietnamese securities
- **Portfolio Managers**: Performance tracking and risk assessment

## System Context Diagram

```mermaid
C4Context
    title System Context - Tearsheet Portfolio Analyzer (Microservices)
    
    Person(user, "End User", "Individual investors, financial advisors, analysts")
    Person(admin, "System Administrator", "Maintains system, monitors performance")
    
    System_Boundary(tearsheet_system, "Tearsheet Portfolio Analyzer") {
        System(frontend, "Next.js Frontend", "React-based web application (Port 3000)")
        System(backend, "Flask API Backend", "JSON API server (Port 5001)")
    }
    
    System_Ext(vnstock, "VNStock API", "Vietnam stock market data provider")
    System_Ext(quantstats, "QuantStats Library", "Portfolio analytics and HTML generation")
    System_Ext(browser, "Web Browser", "Modern browser with JavaScript support")
    System_Ext(cdn, "CDN/Static Assets", "Next.js optimized asset delivery")
    
    Rel(user, browser, "Accesses application")
    Rel(browser, frontend, "HTTP/HTTPS requests", "Port 3000")
    Rel(frontend, backend, "JSON API calls", "CORS-enabled Port 5001")
    
    Rel(backend, vnstock, "Fetches stock data and ratios", "HTTPS/API")
    Rel(backend, quantstats, "Generates HTML tearsheets", "Python Library")
    
    Rel(admin, tearsheet_system, "Monitors and maintains")
    Rel(frontend, cdn, "Loads optimized assets")
```

## External Systems and Integrations

### VNStock API Integration
- **Purpose**: Primary source for Vietnam stock market data
- **Data Types**: Historical prices, financial ratios, company fundamentals
- **Protocol**: HTTP REST API
- **Integration**: Backend-only access (Flask API)
- **Authentication**: API key-based (when required)

### QuantStats Library
- **Purpose**: Complete HTML tearsheet generation
- **Functionality**: Performance analytics, risk metrics, visualizations
- **Integration**: Server-side Python library (Backend only)
- **Output**: Complete HTML reports with embedded charts and styling

### Next.js Frontend
- **Technologies**: React 19, TypeScript, Tailwind CSS, TanStack Query
- **Compatibility**: Modern browsers with JavaScript support
- **Features**: Server-side rendering, automatic optimization, hot reloading
- **Security**: Built-in XSS protection, CSP headers

### Flask API Backend
- **Technologies**: Python Flask, CORS-enabled, JSON-only responses
- **Purpose**: Business logic, data processing, QuantStats integration
- **Endpoints**: RESTful API design with comprehensive error handling
- **Security**: Input validation, rate limiting, secure headers

## System Boundaries

### Internal Scope
- **Frontend Application**: Next.js React application with TypeScript
- **Backend API**: Flask JSON API with business logic
- **Data Processing**: Real-time portfolio analysis and validation
- **HTML Generation**: QuantStats tearsheet creation
- **Cross-service Communication**: JSON API between frontend and backend

### External Dependencies
- Vietnam stock market data availability (VNStock API)
- Modern web browser with JavaScript enabled
- Network connectivity for API communication
- Python and Node.js runtime environments

## Quality Attributes

### Performance
- **Response Time**: < 5 seconds for complete tearsheet generation
- **Frontend Performance**: Next.js optimizations, server-side rendering
- **API Performance**: Efficient Flask endpoints with minimal overhead
- **Scalability**: Independent scaling of frontend and backend services

### Reliability
- **Availability**: 99.5% uptime target for both services
- **Error Handling**: Comprehensive error boundaries and user feedback
- **Data Integrity**: Multi-layer validation (client + server)
- **Service Isolation**: Frontend/backend failures don't cascade

### Security
- **Multi-layer Validation**: Client-side Zod + server-side Python validation
- **CORS Security**: Properly configured cross-origin policies
- **XSS Protection**: React built-in protection + input sanitization
- **Data Privacy**: Stateless architecture with temporary file cleanup
- **Transport Security**: HTTPS encryption for all communications

### Maintainability
- **Microservices Architecture**: Independent frontend/backend development
- **Type Safety**: Full TypeScript integration across frontend
- **Code Quality**: Automated linting, formatting, and type checking
- **Documentation**: Comprehensive architecture and API documentation
- **Testing**: Component, API, and end-to-end testing strategies

## Constraints and Assumptions

### Technical Constraints
- **Backend**: Python 3.9+ runtime, Flask framework
- **Frontend**: Node.js 18+, React 19, modern browser support
- **External APIs**: VNStock API rate limits and availability
- **Architecture**: Microservices requiring dual-port deployment

### Business Constraints
- Vietnam stock market data focus
- Real-time data processing requirements
- Professional tearsheet quality standards
- Regulatory compliance for financial analysis

### Assumptions
- Stable internet connectivity for cross-service communication
- Modern web browsers with JavaScript enabled
- Development/production environment separation
- Container deployment capability for production