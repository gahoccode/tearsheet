# Add Package to Python Workspace

Add and configure new Python packages/modules to the finance-bro project

## Instructions

1. **Package Definition and Analysis**
   - Parse package name and type from arguments: `$ARGUMENTS` (format: name [type])
   - If no arguments provided, prompt for package name and type
   - Validate package name follows Python naming conventions (lowercase, underscores)
   - Determine package type: library, application, tool, shared, service, component-library
   - Check for naming conflicts with existing packages in `src/` directory

2. **Package Structure Creation**
   - Create package directory in appropriate workspace location:
     - `src/` for main packages
     - `tests/` for test files (mirrors src structure)
     - `docs/` for documentation
   - Set up standard Python package directory structure:
     - `__init__.py` for package initialization
     - `main.py` or `app.py` for applications
     - `cli.py` for CLI tools
     - `config.py` for configuration
     - `models/` for data models
     - `utils/` for utilities
     - `services/` for service classes
   - Create package-specific configuration files

3. **Package Configuration Setup**
   - Update `pyproject.toml` with new package dependencies:
     - Add package to `[project]` dependencies if needed
     - Add development dependencies to `[project.optional-dependencies]`
     - Configure entry points for CLI tools
   - Configure Python package structure:
     - Set up proper `__init__.py` with exports
     - Configure type hints and mypy settings
     - Set up package-specific linting rules in `.ruff.toml`
   - Create `requirements.txt` if standalone package

4. **Package Type-Specific Setup**
   - **Library**: Configure setup for PyPI publishing
     - Add proper `setup.py` or `pyproject.toml`
     - Configure package metadata and classifiers
     - Set up API documentation with Sphinx
   - **Application**: Configure Streamlit/FastAPI setup
     - Set up Streamlit pages structure
     - Configure FastAPI routers and endpoints
     - Set up environment configuration
   - **Tool**: Configure CLI interface
     - Set up Click or Typer CLI framework
     - Configure command-line arguments
     - Set up entry points in pyproject.toml
   - **Shared**: Set up common utilities
     - Configure shared constants and types
     - Set up configuration management
     - Create shared helper functions
   - **Service**: Configure service architecture
     - Set up service classes and interfaces
     - Configure database models (SQLAlchemy)
     - Set up API endpoints
   - **Component Library**: Configure UI components
     - Set up Streamlit component structure
     - Configure component styling
     - Set up component documentation

5. **Workspace Integration**
   - Register package in workspace configuration:
     - Update `pyproject.toml` with new dependencies
     - Configure import paths in `PYTHONPATH`
     - Set up package discovery in `__init__.py`
   - Configure package dependencies:
     - Add internal package dependencies
     - Configure external package requirements
     - Set up version constraints
   - Configure workspace-wide imports:
     - Update `src/__init__.py` for package exports
     - Configure relative vs absolute imports
     - Set up package aliases

6. **Development Environment**
   - Configure package-specific development:
     - Set up Python virtual environment
     - Configure development dependencies
     - Set up pre-commit hooks
   - Configure hot reloading:
     - Set up Streamlit auto-reload
     - Configure file watchers for development
   - Configure debugging:
     - Set up VS Code launch configurations
     - Configure Python debugger settings
     - Set up logging configuration

7. **Testing Infrastructure**
   - Set up pytest configuration:
     - Create `conftest.py` for package-specific fixtures
     - Configure test discovery patterns
     - Set up test data and mocks
   - Create initial test files:
     - `test_<package_name>.py` for unit tests
     - `test_integration.py` for integration tests
     - `test_e2e.py` for end-to-end tests
   - Configure test coverage:
     - Set up pytest-cov configuration
     - Configure coverage reporting
     - Set up CI/CD test pipeline

8. **Build and Deployment**
   - Configure build system:
     - Set up build scripts in `pyproject.toml`
     - Configure wheel building
     - Set up package versioning
   - Configure deployment:
     - Set up Docker configuration
     - Configure environment variables
     - Set up deployment scripts
   - Configure package publishing:
     - Set up PyPI publishing
     - Configure version bumping
     - Set up release automation

9. **Documentation and Examples**
   - Create package README:
     - Installation instructions
     - Usage examples
     - API documentation
   - Set up documentation:
     - Configure Sphinx documentation
     - Set up docstring standards
     - Configure auto-generated docs
   - Create usage examples:
     - Jupyter notebooks for tutorials
     - Example scripts
     - Integration examples

10. **Validation and Integration Testing**
    - Verify package imports correctly:
      - Test import statements
      - Check for circular imports
      - Validate package structure
    - Test development workflow:
      - Verify development server starts
      - Test hot reloading
      - Validate debugging setup
    - Verify CI/CD pipeline:
      - Test GitHub Actions workflow
      - Validate test execution
      - Check deployment pipeline
    - Test cross-package functionality:
      - Test package integration
      - Validate shared utilities
      - Check service dependencies
