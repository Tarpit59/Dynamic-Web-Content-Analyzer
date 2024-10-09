import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from base import app

class TestController(unittest.TestCase):

    def setUp(self):
        """Set up the test client."""
        self.app = app.test_client()
        self.app.testing = True

    def test_index_page(self):
        """Test the index page loads successfully."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Dynamic Web Content Analyzer', response.data)  # Check for the title

    def test_analyze_with_valid_urls(self):
        """Test the /analyze endpoint with valid URLs."""
        data = {'urls': ["http://example.com"]}
        response = self.app.post('/analyze', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'sentiment_comparison', response.data)  # Check if 'sentiment_comparison' is in response

    def test_analyze_with_invalid_urls(self):
        """Test the /analyze endpoint with invalid URLs."""
        data = {'urls': ["invalid-url"]}
        response = self.app.post('/analyze', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'invalid_urls', response.data)  # Check if 'invalid_urls' is in the response

    def test_analyze_with_mixed_urls(self):
        """Test the /analyze endpoint with both valid and invalid URLs."""
        data = {'urls': ["http://example.com", "invalid-url"]}
        response = self.app.post('/analyze', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'invalid_urls', response.data)  # Check if 'invalid_urls' is present

    def test_analyze_with_no_urls(self):
        """Test the /analyze endpoint when no URLs are provided."""
        data = {'urls': []}
        response = self.app.post('/analyze', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'No URLs provided.', response.data)

if __name__ == '__main__':
    unittest.main()
