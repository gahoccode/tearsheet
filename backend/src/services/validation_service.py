"""
Input validation and sanitization service.
"""

import re
from typing import List, Dict, Any, Tuple
from datetime import datetime, timedelta
import logging

from ..utils.exceptions import ValidationError
from ..utils.constants import (
    MIN_PORTFOLIO_SIZE,
    MAX_PORTFOLIO_SIZE,
    MIN_WEIGHT,
    MAX_WEIGHT,
    WEIGHT_TOLERANCE,
    DATE_FORMAT,
    ERROR_MESSAGES,
    MAX_DATE_RANGE_DAYS,
)

logger = logging.getLogger(__name__)


class ValidationService:
    """Service for validating and sanitizing user inputs."""

    def __init__(self):
        """Initialize validation service."""
        self.date_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}$")
        logger.debug("ValidationService initialized")

    def validate_symbols(self, symbols: List[str]) -> List[str]:
        """
        Validate and sanitize stock symbols.

        Args:
            symbols: List of stock symbols

        Returns:
            List of validated and sanitized symbols

        Raises:
            ValidationError: If validation fails
        """
        if not symbols:
            raise ValidationError("No symbols provided")

        # Remove empty strings and whitespace
        cleaned_symbols = [s.strip().upper() for s in symbols if s and s.strip()]

        if not cleaned_symbols:
            raise ValidationError("No valid symbols provided")

        if len(cleaned_symbols) < MIN_PORTFOLIO_SIZE:
            raise ValidationError(
                f"Portfolio must have at least {MIN_PORTFOLIO_SIZE} symbol(s)"
            )

        if len(cleaned_symbols) > MAX_PORTFOLIO_SIZE:
            raise ValidationError(ERROR_MESSAGES["PORTFOLIO_TOO_LARGE"])

        # Check for duplicates
        if len(cleaned_symbols) != len(set(cleaned_symbols)):
            raise ValidationError("Duplicate symbols are not allowed")

        # Basic symbol format validation (Vietnam stock format)
        symbol_pattern = re.compile(r"^[A-Z]{3,4}$")
        invalid_symbols = [s for s in cleaned_symbols if not symbol_pattern.match(s)]

        if invalid_symbols:
            raise ValidationError(f"Invalid symbol format: {invalid_symbols}")

        logger.debug(f"Validated {len(cleaned_symbols)} symbols: {cleaned_symbols}")
        return cleaned_symbols

    def validate_weights(self, weights: List[str], num_symbols: int) -> List[float]:
        """
        Validate and convert portfolio weights.

        Args:
            weights: List of weight strings
            num_symbols: Expected number of weights

        Returns:
            List of validated float weights

        Raises:
            ValidationError: If validation fails
        """
        if not weights:
            raise ValidationError("No weights provided")

        if len(weights) != num_symbols:
            raise ValidationError("Number of weights must match number of symbols")

        try:
            # Convert to float
            float_weights = [float(w.strip()) for w in weights if w.strip()]

            if len(float_weights) != num_symbols:
                raise ValidationError("Some weights are missing or invalid")

            # Validate individual weights
            for i, weight in enumerate(float_weights):
                if not (MIN_WEIGHT <= weight <= MAX_WEIGHT):
                    raise ValidationError(ERROR_MESSAGES["INVALID_WEIGHT"])

            # Validate sum
            weight_sum = sum(float_weights)
            if abs(weight_sum - 1.0) > WEIGHT_TOLERANCE:
                raise ValidationError(ERROR_MESSAGES["WEIGHTS_NOT_SUM_ONE"])

            # Normalize to ensure exact sum of 1.0
            normalized_weights = [w / weight_sum for w in float_weights]

            logger.debug(
                f"Validated weights: {normalized_weights} (sum: {sum(normalized_weights)})"
            )
            return normalized_weights

        except ValueError:
            raise ValidationError("Weights must be valid numbers")

    def validate_capital(self, capital: str) -> float:
        """
        Validate and convert capital amount.

        Args:
            capital: Capital amount string

        Returns:
            Validated float capital

        Raises:
            ValidationError: If validation fails
        """
        if not capital or not capital.strip():
            raise ValidationError("Capital amount is required")

        try:
            capital_float = float(capital.strip())

            if capital_float <= 0:
                raise ValidationError("Initial capital must be positive")

            # Check for reasonable bounds (max 1 trillion VND)
            if capital_float > 1_000_000_000_000:
                raise ValidationError("Capital amount seems unreasonably high")

            logger.debug(f"Validated capital: {capital_float:,.0f}")
            return capital_float

        except ValueError:
            raise ValidationError("Capital must be a valid number")

    def validate_date_range(self, start_date: str, end_date: str) -> Tuple[str, str]:
        """
        Validate date range.

        Args:
            start_date: Start date string (YYYY-MM-DD)
            end_date: End date string (YYYY-MM-DD)

        Returns:
            Tuple of validated date strings

        Raises:
            ValidationError: If validation fails
        """
        # Check format
        if not self.date_pattern.match(start_date.strip()):
            raise ValidationError(ERROR_MESSAGES["INVALID_DATE_FORMAT"])

        if not self.date_pattern.match(end_date.strip()):
            raise ValidationError(ERROR_MESSAGES["INVALID_DATE_FORMAT"])

        try:
            # Parse dates
            start_dt = datetime.strptime(start_date.strip(), DATE_FORMAT)
            end_dt = datetime.strptime(end_date.strip(), DATE_FORMAT)

            # Validate range
            if start_dt >= end_dt:
                raise ValidationError(ERROR_MESSAGES["INVALID_DATE_RANGE"])

            # Check if range is reasonable
            date_diff = (end_dt - start_dt).days
            if date_diff > MAX_DATE_RANGE_DAYS:
                raise ValidationError(
                    f"Date range too large (max {MAX_DATE_RANGE_DAYS} days)"
                )

            # Check if dates are not in the future
            today = datetime.now().date()
            if end_dt.date() > today:
                raise ValidationError("End date cannot be in the future")

            # Check if start date is not too old (10 years)
            ten_years_ago = today - timedelta(days=10 * 365)
            if start_dt.date() < ten_years_ago:
                raise ValidationError("Start date cannot be more than 10 years ago")

            logger.debug(
                f"Validated date range: {start_date} to {end_date} ({date_diff} days)"
            )
            return start_date.strip(), end_date.strip()

        except ValueError as e:
            if "time data" in str(e):
                raise ValidationError(ERROR_MESSAGES["INVALID_DATE_FORMAT"])
            else:
                raise ValidationError(f"Date validation failed: {str(e)}")

    def validate_portfolio_form(
        self,
        symbols: List[str],
        weights: List[str],
        capital: str,
        start_date: str,
        end_date: str,
    ) -> Dict[str, Any]:
        """
        Validate complete portfolio form data.

        Args:
            symbols: List of stock symbols
            weights: List of weight strings
            capital: Capital amount string
            start_date: Start date string
            end_date: End date string

        Returns:
            Dictionary with validated data

        Raises:
            ValidationError: If any validation fails
        """
        logger.info("Validating portfolio form data")

        try:
            # Validate each component
            validated_symbols = self.validate_symbols(symbols)
            validated_weights = self.validate_weights(weights, len(validated_symbols))
            validated_capital = self.validate_capital(capital)
            validated_start, validated_end = self.validate_date_range(
                start_date, end_date
            )

            result = {
                "symbols": validated_symbols,
                "weights": validated_weights,
                "capital": validated_capital,
                "start_date": validated_start,
                "end_date": validated_end,
                "validation_timestamp": datetime.now().isoformat(),
            }

            logger.info(
                f"Portfolio form validation successful: {len(validated_symbols)} stocks"
            )
            return result

        except ValidationError:
            logger.warning("Portfolio form validation failed")
            raise
        except Exception as e:
            logger.error(f"Unexpected validation error: {e}")
            raise ValidationError(f"Validation failed: {str(e)}")

    def sanitize_string(self, value: str, max_length: int = 100) -> str:
        """
        Sanitize string input.

        Args:
            value: String to sanitize
            max_length: Maximum allowed length

        Returns:
            Sanitized string
        """
        if not value:
            return ""

        # Strip whitespace and limit length
        sanitized = value.strip()[:max_length]

        # Remove potentially dangerous characters
        sanitized = re.sub(r'[<>"\';\\]', "", sanitized)

        return sanitized

    def validate_optional_fields(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate optional portfolio fields.

        Args:
            data: Dictionary with optional fields

        Returns:
            Dictionary with validated optional fields
        """
        validated = {}

        if "portfolio_name" in data:
            validated["portfolio_name"] = self.sanitize_string(
                data["portfolio_name"], 50
            )

        if "include_ratios" in data:
            validated["include_ratios"] = bool(data.get("include_ratios", False))

        if "export_excel" in data:
            validated["export_excel"] = bool(data.get("export_excel", False))

        return validated
