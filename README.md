
# Dynamic Web Content Analyzer

This Flask-based web application allows users to input multiple URLs for analysis, including sentiment comparison, readability scoring, and word cloud generation. The results are presented in a user-friendly format with graphical visualizations.


## API Reference

### Analyze Multiple URLs
#### Description:
Analyzes multiple URLs provided by the user. The URLs are scraped, and the text is analyzed for sentiment, readability, and word frequencies. Word clouds are also generated for each URL.
```http
  POST/analysis
```
#### Request Body:
| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `urls`      | `list[str]` | **Required**. List of URLs to analyze |

#### Response Body:
| Field | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `sentiment_comparison`      | `list[dict]` | A list of sentiment analysis results for each URL, including positive, neutral, and negative sentiment scores. |
| `readability_comparison`      | `list[dict]` | A list of readability scores for each URL using the Flesch-Kincaid Grade.|
| `word_clouds`      | `list[dict]` | A list of base64 encoded word cloud images for each URL. |
| `invalid_urls`      | `list[dict] (if error)` | A list of URLs with the issues encountered (e.g., invalid format, access errors) if there are any invalid URLs. |

#### Example Request:
```
{
  "urls": [
    "https://example.com",
    "https://invalid-url"
  ]
}

```
#### Example Response:
```
{
  "sentiment_comparison": [
    {
      "URL": "URL 1",
      "Positive": 0.12,
      "Neutral": 0.75,
      "Negative": 0.13
    }
  ],
  "readability_comparison": [
    {
      "URL": "URL 1",
      "Readability": 8.5
    }
  ],
  "word_clouds": [
    {
      "URL": "URL 1",
      "word_cloud": "<base64 image string>"
    }
  ]
}

```

### Scrape Page

```http
  GET /scrape/{url}
```
#### Description:
Scrapes a single URL and returns the text content of the page.
#### Parameters:
| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `url` | `string` | **Required**. The URL to scrape. |

#### Response:
| Field | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `text` | `string` | The text content of the URL. |
| `error` | `string` | Any error encountered during scraping. |

## Tech Stack

**Frontend:**

- **HTML:** Structure and layout of the web pages.
- **CSS:** Styling and formatting the UI elements.
- **JavaScript:** Adds interactivity to the frontend.

**Backend:**

- **Python:** Core programming language used for backend logic.
- **Flask:** Web framework used to handle HTTP requests and server-side logic.

**Additional Libraries:**
- **Requests:** For making HTTP requests to scrape the URLs.
- **BeautifulSoup:** For parsing and extracting data from HTML content.
- **ThreadPoolExecutor:** For concurrent scraping of multiple URLs.
- **NLTK:** Used for sentiment analysis with the VADER sentiment analyzer.
- **TextStat:** To calculate readability scores.
- **WordCloud:** For generating word clouds based on word frequencies.
- **Matplotlib:** For rendering the word cloud images.
- **CacheTools:** To cache the results of scraped URLs and reduce repeated requests.








## Implementation

### 1. Clone the repository
Start by cloning the project repository from GitHub:

```bash
git clone https://github.com/Tarpit59/Dynamic-Web-Content-Analyzer.git
cd Dynamic Web Content Analyzer

```
### 2. Set up a virtual environment:

Create a virtual environment using venv with Python 3.9.7. This ensures the project dependencies are isolated.

```bash
python3.9 -m venv venv
```

### 3. Activate the virtual environment:

- On Windows:
```bash
venv\Scripts\activate
```
- On macOS/Linux:
```bash
source venv/bin/activate
```

### 4. Install dependencies:
Install all required dependencies from requirements.txt:
```bash
pip install -r requirements.txt
```

### 5. Run the Flask Server:
Start the Flask development server:
```bash
python app.py
```
This will start the server on http://127.0.0.1:5000/ You can now visit this URL in your browser to access the app.
## Running Tests

[Documentation](https://github.com/Tarpit59/Dynamic-Web-Content-Analyzer/blob/main/base/tests/README.md)

### 1. Activate the virtual environment:

- On Windows:
```bash
venv\Scripts\activate
```
- On macOS/Linux:
```bash
source venv/bin/activate
```

### 2. Go into base Direcrory:

```bash
  cd base
```

### 3. Run the following command:

```bash
  pytest -v
```
## Acknowledgements

 - [Concurrent Futures Documentation](https://docs.python.org/3/library/concurrent.futures.html)
 - [CacheTools](https://cachetools.readthedocs.io/en/stable/)
 - [WordCloud Library](https://amueller.github.io/word_cloud/)
 - [Flask Documentation](https://flask.palletsprojects.com/en/3.0.x/)

## Screenshots

![Web App Screenshot](https://github.com/Tarpit59/Dynamic-Web-Content-Analyzer/blob/main/base/static/images/ui_1.png)

![Web App Screenshot](https://github.com/Tarpit59/Dynamic-Web-Content-Analyzer/blob/main/base/static/images/ui_2.png)


## 🔗 Links
[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/tarpit-patel)

