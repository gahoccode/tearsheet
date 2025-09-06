# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.0] - 2025-01-06
### Added
- Full-width responsive layout for enhanced user experience
- Bootstrap 5 integration with modern UI components
- Enhanced form validation and user feedback
- Side-by-side layout for portfolio composition and analysis parameters
- Large form controls for improved usability
- Direct QuantStats HTML content injection (replacing iframe approach)
- Full viewport width utilization for tearsheet display
- Responsive design with mobile-first approach
- Enhanced CSS with flexible scaling based on viewport size
- Help modal with comprehensive usage instructions

### Changed
- UI framework upgraded from custom CSS to Bootstrap 5
- Form layout redesigned with improved column structure (8/4 split)
- QuantStats tearsheet display method from iframe to direct HTML injection
- Container layout from fixed-width to full-width flexible design
- Navigation bar enhanced with full-width support
- Form controls upgraded to large size for better accessibility
- Typography and spacing improved for better readability

### Fixed
- QuantStats report spinner freezing issue resolved
- Full-width tearsheet display implementation
- Mobile responsiveness across all device sizes
- Form validation and user experience improvements

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