"""
Production environment configuration.
"""

import os
from .base import BaseConfig


class ProductionConfig(BaseConfig):
    """Production configuration class."""

    # Flask settings
    DEBUG = False
    TESTING = False

    # Production server settings
    HOST = "0.0.0.0"
    PORT = int(os.environ.get("PORT", 5000))

    # Security
    SECRET_KEY = os.environ.get("SECRET_KEY")
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY environment variable must be set in production")

    # Logging
    LOG_LEVEL = "WARNING"

    # Production data settings
    USE_SAMPLE_DATA = False
    CACHE_REQUESTS = True
    CACHE_TIMEOUT = 3600  # 1 hour

    # Performance settings
    CONCURRENT_REQUESTS = 10
    REQUEST_TIMEOUT = 30

    # Production security headers
    SECURITY_HEADERS = {
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "X-XSS-Protection": "1; mode=block",
        "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
    }

    @classmethod
    def init_app(cls, app):
        """Initialize production-specific settings."""
        super().init_app(app)

        # Production logging setup
        import logging
        from logging.handlers import RotatingFileHandler

        if not app.debug and not app.testing:
            file_handler = RotatingFileHandler(
                "logs/tearsheet.log", maxBytes=10240000, backupCount=10
            )
            file_handler.setFormatter(
                logging.Formatter(
                    "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"
                )
            )
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)
            app.logger.setLevel(logging.INFO)
            app.logger.info("Tearsheet startup")
