"""
tests/test_app.py
Integration tests for Flask API routes
"""

import unittest
from api import app
import matplotlib


class FlaskAppIntegrationTest(unittest.TestCase):
    def test_matplotlib_backend_is_agg(self):
        """Test that matplotlib backend is set to 'Agg' for server-side rendering."""
        self.assertEqual(matplotlib.get_backend().lower(), "agg")

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_health_endpoint(self):
        """Test GET /api/health returns 200."""
        response = self.app.get("/api/health")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["status"], "healthy")

    def test_tearsheet_api_valid_input(self):
        """Test POST /api/tearsheet with valid input returns HTML tearsheet."""
        data = {
            "symbols": ["REE", "FMC", "DHC"],
            "weights": [0.7, 0.2, 0.1],
            "start_date": "2024-01-01",
            "end_date": "2024-03-01",
            "capital": 10000000,
        }
        response = self.app.post(
            "/api/tearsheet", json=data, content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        result = response.get_json()
        self.assertIn("html", result)
        self.assertIn("portfolio_name", result)

    def test_validate_api_invalid_dates(self):
        """Test POST /api/validate with invalid date format."""
        data = {
            "symbols": ["REE", "FMC", "DHC"],
            "weights": [0.7, 0.2, 0.1],
            "start_date": "2024/01/01",
            "end_date": "2024-03-01",
            "capital": 10000000,
        }
        response = self.app.post(
            "/api/validate", json=data, content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        result = response.get_json()
        self.assertFalse(result["valid"])
        self.assertIn("date", result["error"].lower())

    def test_ratios_api_endpoint(self):
        """Test GET /api/ratios/<symbol> endpoint returns financial data."""
        response = self.app.get("/api/ratios/REE?period=year")
        self.assertEqual(response.status_code, 200)
        result = response.get_json()
        self.assertIn("symbol", result)
        self.assertEqual(result["symbol"], "REE")

    def test_tearsheet_invalid_symbol(self):
        """Test POST /api/tearsheet with invalid stock symbol."""
        data = {
            "symbols": ["INVALID123"],
            "weights": [1.0],
            "start_date": "2024-01-01",
            "end_date": "2024-03-01",
            "capital": 10000000,
        }
        response = self.app.post(
            "/api/tearsheet", json=data, content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        result = response.get_json()
        self.assertIn("error", result)

    def test_tearsheet_invalid_weights(self):
        """Test POST /api/tearsheet with invalid weights (don't sum to 1.0)."""
        data = {
            "symbols": ["REE", "FMC", "DHC"],
            "weights": [0.5, 0.3, 0.3],  # Sum > 1
            "start_date": "2024-01-01",
            "end_date": "2024-03-01",
            "capital": 10000000,
        }
        response = self.app.post(
            "/api/tearsheet", json=data, content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        result = response.get_json()
        self.assertIn("error", result)


if __name__ == "__main__":
    unittest.main()
