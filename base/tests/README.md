
# Testing Documentation

This project includes tests to validate both the backend services and controller endpoints. The tests are written using the pytest framework and cover two primary modules:

- **Service Tests:** Located in test_service.py, which tests the scraping, text analysis, word cloud generation, and error handling functionalities.
- **Controller Tests:** Located in test_controller.py, which tests the behavior of Flask endpoints.

### Prerequisites
#### 1. Install all the necessary dependencies
Before running the tests, ensure that you have installed all the necessary dependencies. You can install them using the requirements.txt file:

```bash
pip install -r requirements.txt
```

#### 2. Activate the virtual environment:

- On Windows:
```bash
venv\Scripts\activate
```
- On macOS/Linux:
```bash
source venv/bin/activate
```

#### 3. Go into base Direcrory:

```bash
  cd base
```

### Running Tests:

```bash
  pytest -v
```
#### Output Format
pytest provides a detailed output format by default, showing which tests passed, failed, or were skipped.:

- -v: Run in verbose mode, showing each test case.

### Running Specific Tests
To run a specific test file:
```bash
  pytest base/tests/test_file.py -v
```
### Test Cases Breakdown

### Service Tests (test_service.py)

These tests validate core backend functionalities, such as scraping content, text analysis, word cloud generation, and error handling.

#### 1. test_scrape_page_success
- **Purpose:** Tests if a valid URL returns text without any errors.
- **How:** Calls the scrape_page() function with a valid URL (https://example.com).
- **Expected Result:** The result contains a 'text' field, and 'error' should be None.
### 2. test_scrape_page_invalid_url
- **Purpose:** Tests behavior when scraping an invalid URL.
- **How:** Calls scrape_page() with an invalid URL (http://invalid-url).
- **Expected Result:** The text field should be None, and the 'error' field should contain an error message.
### 3. test_analyze_text
- **Purpose:** Verifies sentiment analysis and readability.
- **How:** Calls analyze_text() with a sample positive text.
- **Expected Result:** The positive sentiment should be greater than 0, and readability should return a valid value.
### 4. test_generate_word_cloud
- **Purpose:** Tests word cloud generation.
- **How:** Calls generate_word_cloud() with a Counter dictionary of word frequencies.
- **Expected Result:** The function should return a valid base64-encoded string.
### 5. test_handle_scraping_error_invalid_url
- **Purpose:** Tests the error handler for invalid URL format.
- **How:** Calls handle_scraping_error() with an invalid URL and an "Invalid URL format" message.
- **Expected Result:** The returned issue should state that the URL format is invalid.
### 6. test_handle_scraping_error_404
- **Purpose:** Tests the error handler for 404 errors.
- **How:** Calls handle_scraping_error() with a 404 error.
- **Expected Result:** The returned issue should state that the page was not found.
### 7. test_handle_scraping_error_timeout
- **Purpose:** Tests the error handler for connection timeouts.
- **How:** Calls handle_scraping_error() with a "Max retries exceeded" error.
- **Expected Result:** The returned issue should indicate a connection timeout.

### Controller Tests (test_controller.py)

These tests validate the behavior of your Flask application’s routes, including the /analyze endpoint.

### 1. test_index_page
- **Purpose:** Verifies that the index page loads successfully.
- **How:** Calls the / route using Flask's test client.
- **Expected Result:** The status code should be 200, and the response should contain the string "Dynamic Web Content Analyzer".
### 2. test_analyze_with_valid_urls
- **Purpose:** Tests the /analyze endpoint with valid URLs.
- **How:** Sends a POST request to /analyze with valid URLs.
- **Expected Result:** The status code should be 200, and the response should include sentiment_comparison.
### 3. test_analyze_with_invalid_urls
- **Purpose:** Tests the /analyze endpoint with invalid URLs.
- **How:** Sends a POST request to /analyze with an invalid URL.
- **Expected Result:** The status code should be 400, and the response should include invalid_urls.
### 4. test_analyze_with_mixed_urls
- **Purpose:** Tests the /analyze endpoint with both valid and invalid URLs.
- **How:** Sends a POST request to /analyze with one valid and one invalid URL.
- **Expected Result:** The status code should be 400, and the response should include invalid_urls.
### 5. test_analyze_with_no_urls
- **Purpose:** Tests the /analyze endpoint when no URLs are provided.
- **How:** Sends a POST request to /analyze with an empty URL list.
- **Expected Result:** The status code should be 400, and the response should indicate "No URLs provided."