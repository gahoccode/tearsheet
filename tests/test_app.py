"""
tests/test_app.py
Integration tests for Flask app routes and POST behavior
"""

import unittest
from app import app
from flask import url_for

class FlaskAppIntegrationTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_index_route(self):
        """Test GET / returns 200 and contains form."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Vietnam Stock Portfolio Analyzer', response.data)
        self.assertIn(b'Symbol 1', response.data)

    def test_analyze_valid(self):
        """Test POST /analyze with valid input."""
        data = {
            'symbols[]': ['REE', 'FMC', 'DHC'],
            'weights[]': ['0.7', '0.2', '0.1'],
            'start_date': '2024-01-01',
            'end_date': '2024-03-01',
            'capital': '10000000'
        }
        response = self.app.post('/analyze', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Portfolio Analysis Results', response.data)

    def test_analyze_invalid_weights(self):
        """Test POST /analyze with weights not summing to 1."""
        data = {
            'symbols[]': ['REE', 'FMC', 'DHC'],
            'weights[]': ['0.5', '0.2', '0.1'],
            'start_date': '2024-01-01',
            'end_date': '2024-03-01',
            'capital': '10000000'
        }
        response = self.app.post('/analyze', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'weights must sum to 1', response.data.lower())

    def test_analyze_invalid_dates(self):
        """Test POST /analyze with invalid date format."""
        data = {
            'symbols[]': ['REE', 'FMC', 'DHC'],
            'weights[]': ['0.7', '0.2', '0.1'],
            'start_date': '2024/01/01',
            'end_date': '2024-03-01',
            'capital': '10000000'
        }
        response = self.app.post('/analyze', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'date format', response.data.lower())

    def test_analyze_invalid_symbol(self):
        """Test POST /analyze with invalid ticker symbol."""
        data = {
            'symbols[]': ['INVALIDTICKER', 'FMC', 'DHC'],
            'weights[]': ['0.7', '0.2', '0.1'],
            'start_date': '2024-01-01',
            'end_date': '2024-03-01',
            'capital': '10000000'
        }
        response = self.app.post('/analyze', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            b'error fetching data' in response.data.lower() or
            b'invalid symbol' in response.data.lower() or
            b'no historical data' in response.data.lower()
        )

if __name__ == '__main__':
    unittest.main()
