"""
Development environment configuration.
"""

import os
from .base import BaseConfig


class DevelopmentConfig(BaseConfig):
    """Development configuration class."""

    # Flask settings
    DEBUG = True
    TESTING = False

    # Development server settings
    HOST = "0.0.0.0"
    PORT = int(os.environ.get("PORT", 5000))

    # Logging
    LOG_LEVEL = "DEBUG"

    # Development data settings
    USE_SAMPLE_DATA = os.environ.get("USE_SAMPLE_DATA", "False").lower() == "true"
    CACHE_REQUESTS = False

    # Development-specific paths
    CACHE_DIR = BaseConfig.PROJECT_ROOT / ".cache"
    LOG_DIR = BaseConfig.PROJECT_ROOT / "logs"

    @classmethod
    def init_app(cls, app):
        """Initialize development-specific settings."""
        super().init_app(app)

        # Create development directories
        cls.CACHE_DIR.mkdir(exist_ok=True)
        cls.LOG_DIR.mkdir(exist_ok=True)

        # Enable detailed error pages
        app.config["PROPAGATE_EXCEPTIONS"] = True
