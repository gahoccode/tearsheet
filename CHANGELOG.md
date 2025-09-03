# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- Claude Code configuration and documentation
- Comprehensive testing suite with integration and unit tests
- QuantStats HTML tearsheet generation and redirection
- Vietnam stock portfolio analysis functionality
- Custom CSS styling (replacing Bootstrap)
- Docker containerization support
- GitHub Container Registry (GHCR) workflow
- Render.com deployment configuration
- Dynamic port configuration for cloud deployment

### Changed
- Project renamed to "tearsheet"
- UI framework from Bootstrap to custom CSS styling
- Matplotlib font to DejaVu Sans for Linux compatibility
- Dependencies updated to latest versions

### Fixed
- Server-side rendering issues with matplotlib backend set to 'Agg'
- Cross-platform deployment compatibility

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