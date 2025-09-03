"""
Unit tests for validation service.
"""

import unittest
from src.services.validation_service import ValidationService
from src.utils.exceptions import ValidationError


class TestValidationService(unittest.TestCase):
    """Test cases for ValidationService class."""

    def setUp(self):
        """Set up test fixtures."""
        self.validator = ValidationService()

    def test_validate_symbols_success(self):
        """Test successful symbol validation."""
        symbols = ["REE", "FMC", "DHC"]
        result = self.validator.validate_symbols(symbols)

        self.assertEqual(result, symbols)
        self.assertEqual(len(result), 3)

    def test_validate_symbols_with_lowercase(self):
        """Test symbol validation with lowercase input."""
        symbols = ["ree", "fmc", "dhc"]
        result = self.validator.validate_symbols(symbols)

        self.assertEqual(result, ["REE", "FMC", "DHC"])

    def test_validate_symbols_with_whitespace(self):
        """Test symbol validation with whitespace."""
        symbols = [" REE ", " FMC", "DHC "]
        result = self.validator.validate_symbols(symbols)

        self.assertEqual(result, ["REE", "FMC", "DHC"])

    def test_validate_symbols_empty_list(self):
        """Test validation with empty symbol list."""
        with self.assertRaises(ValidationError):
            self.validator.validate_symbols([])

    def test_validate_symbols_duplicates(self):
        """Test validation with duplicate symbols."""
        symbols = ["REE", "FMC", "REE"]
        with self.assertRaises(ValidationError):
            self.validator.validate_symbols(symbols)

    def test_validate_symbols_invalid_format(self):
        """Test validation with invalid symbol format."""
        symbols = ["REE", "123", "DHC"]
        with self.assertRaises(ValidationError):
            self.validator.validate_symbols(symbols)

    def test_validate_weights_success(self):
        """Test successful weight validation."""
        weights = ["0.5", "0.3", "0.2"]
        result = self.validator.validate_weights(weights, 3)

        self.assertEqual(len(result), 3)
        self.assertAlmostEqual(sum(result), 1.0, places=10)

    def test_validate_weights_sum_not_one(self):
        """Test weight validation when sum is not 1.0."""
        weights = ["0.5", "0.3", "0.3"]  # Sum = 1.1
        with self.assertRaises(ValidationError):
            self.validator.validate_weights(weights, 3)

    def test_validate_weights_negative_weight(self):
        """Test weight validation with negative weight."""
        weights = ["0.6", "-0.1", "0.5"]
        with self.assertRaises(ValidationError):
            self.validator.validate_weights(weights, 3)

    def test_validate_weights_invalid_number(self):
        """Test weight validation with invalid number."""
        weights = ["0.5", "abc", "0.2"]
        with self.assertRaises(ValidationError):
            self.validator.validate_weights(weights, 3)

    def test_validate_capital_success(self):
        """Test successful capital validation."""
        capital = "10000000"
        result = self.validator.validate_capital(capital)

        self.assertEqual(result, 10000000.0)

    def test_validate_capital_negative(self):
        """Test capital validation with negative value."""
        capital = "-1000000"
        with self.assertRaises(ValidationError):
            self.validator.validate_capital(capital)

    def test_validate_capital_invalid_number(self):
        """Test capital validation with invalid number."""
        capital = "abc123"
        with self.assertRaises(ValidationError):
            self.validator.validate_capital(capital)

    def test_validate_capital_too_high(self):
        """Test capital validation with unreasonably high value."""
        capital = "1000000000000000"  # 1 quadrillion
        with self.assertRaises(ValidationError):
            self.validator.validate_capital(capital)

    def test_validate_date_range_success(self):
        """Test successful date range validation."""
        start_date = "2024-01-01"
        end_date = "2024-12-31"

        start_result, end_result = self.validator.validate_date_range(
            start_date, end_date
        )

        self.assertEqual(start_result, start_date)
        self.assertEqual(end_result, end_date)

    def test_validate_date_range_invalid_format(self):
        """Test date validation with invalid format."""
        start_date = "2024/01/01"  # Wrong format
        end_date = "2024-12-31"

        with self.assertRaises(ValidationError):
            self.validator.validate_date_range(start_date, end_date)

    def test_validate_date_range_start_after_end(self):
        """Test date validation with start date after end date."""
        start_date = "2024-12-31"
        end_date = "2024-01-01"

        with self.assertRaises(ValidationError):
            self.validator.validate_date_range(start_date, end_date)

    def test_validate_date_range_future_date(self):
        """Test date validation with future end date."""
        start_date = "2024-01-01"
        end_date = "2030-12-31"  # Future date

        with self.assertRaises(ValidationError):
            self.validator.validate_date_range(start_date, end_date)

    def test_validate_portfolio_form_success(self):
        """Test complete portfolio form validation."""
        symbols = ["REE", "FMC", "DHC"]
        weights = ["0.5", "0.3", "0.2"]
        capital = "10000000"
        start_date = "2024-01-01"
        end_date = "2024-06-30"

        result = self.validator.validate_portfolio_form(
            symbols, weights, capital, start_date, end_date
        )

        self.assertIn("symbols", result)
        self.assertIn("weights", result)
        self.assertIn("capital", result)
        self.assertIn("start_date", result)
        self.assertIn("end_date", result)
        self.assertIn("validation_timestamp", result)

        self.assertEqual(len(result["symbols"]), 3)
        self.assertAlmostEqual(sum(result["weights"]), 1.0, places=10)

    def test_sanitize_string_success(self):
        """Test string sanitization."""
        test_string = "  Test String  "
        result = self.validator.sanitize_string(test_string)

        self.assertEqual(result, "Test String")

    def test_sanitize_string_with_dangerous_chars(self):
        """Test string sanitization with dangerous characters."""
        test_string = "Test<script>alert(1)</script>"
        result = self.validator.sanitize_string(test_string)

        self.assertNotIn("<", result)
        self.assertNotIn(">", result)

    def test_sanitize_string_max_length(self):
        """Test string sanitization with length limit."""
        long_string = "A" * 200
        result = self.validator.sanitize_string(long_string, max_length=50)

        self.assertEqual(len(result), 50)


if __name__ == "__main__":
    unittest.main()
