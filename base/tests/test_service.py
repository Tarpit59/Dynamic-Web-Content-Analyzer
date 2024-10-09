import unittest
import sys
import os
from collections import Counter
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))) 
from base.com.service.service import scrape_page, analyze_text, generate_word_cloud, handle_scraping_error

class TestServiceFunctions(unittest.TestCase):

    def test_scrape_page_success(self):
        """Test successful scraping of a valid URL."""
        url = "https://example.com"
        result = scrape_page(url)
        self.assertIn('text', result)
        self.assertIsNone(result['error'])

    def test_scrape_page_invalid_url(self):
        """Test scraping an invalid URL."""
        url = "http://invalid-url"
        result = scrape_page(url)
        self.assertIsNone(result['text'])
        self.assertIsNotNone(result['error'])

    def test_analyze_text(self):
        """Test text analysis for sentiment and readability."""
        text = "This is a sample text. It is positive and wonderful."
        analysis = analyze_text(text)
        self.assertGreater(analysis['sentiment']['pos'], 0)
        self.assertGreaterEqual(analysis['readability'], 0)

    def test_generate_word_cloud(self):
        """Test word cloud generation."""
        word_freq = Counter({'positive': 10, 'wonderful': 5, 'test': 3})
        word_cloud_b64 = generate_word_cloud(word_freq)
        self.assertIsNotNone(word_cloud_b64)
        self.assertTrue(isinstance(word_cloud_b64, str))

    def test_handle_scraping_error_invalid_url(self):
        """Test scraping error handler for invalid URL format."""
        error_result = handle_scraping_error('http://invalid-url', 'Invalid URL format')
        self.assertEqual(error_result['issue'], 'Invalid URL format. Please check the URL.')

    def test_handle_scraping_error_404(self):
        """Test scraping error handler for 404 error."""
        error_result = handle_scraping_error('http://example.com/unknown', '404 Client Error')
        self.assertEqual(error_result['issue'], 'Page not found (404 Error). The requested page may have been removed or the URL may be incorrect.')

    def test_handle_scraping_error_timeout(self):
        """Test scraping error handler for connection timeout."""
        error_result = handle_scraping_error('http://example.com', 'Max retries exceeded')
        self.assertEqual(error_result['issue'], 'Connection timeout or server is unresponsive. Please try again later.')

if __name__ == '__main__':
    unittest.main()
