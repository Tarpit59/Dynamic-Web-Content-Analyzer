import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import nltk
from collections import Counter
from nltk.sentiment import SentimentIntensityAnalyzer
import textstat
import re
from cachetools import TTLCache, cached
import logging
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import matplotlib
import base64
from io import BytesIO
import traceback 

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

matplotlib.use('Agg')

nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()

cache = TTLCache(maxsize=1000, ttl=3600)  # Cache up to 1000 URLs for 1 hour

@cached(cache)
def scrape_page(url):
    """
    Scrapes the content of a single URL. Utilizes caching to prevent re-scraping
    recently accessed URLs within the TTL period.
    
    Args:
        url (str): URL to scrape.
    
    Returns:
        list: A dictionary with 'text' and 'error'.
    """
    try:
        logger.info(f"Scraping URL: {url}")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        text = soup.get_text(separator=' ', strip=True)
        logger.info(f"Successfully scraped URL: {url}")
        return {'text': text, 'error': None}
    
    except Exception as e:
        logger.error(f"Error scraping {url}: {e}")
        logger.error(traceback.format_exc())
        return {'text': None, 'error': f"Error: {str(e)}"}

def scrape_multiple_urls(urls):
    """
    Scrapes multiple URLs concurrently and returns structured data.
    
    Args:
        urls (list): List of URLs to scrape.
        
    Returns:
        list: List of dictionaries with 'text' and 'error'.
    """
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(scrape_page, urls))
    return results


def analyze_text(text):
    """
    Analyzes the given text for word frequency, sentiment, and readability.
    
    Args:
        text (str): The text to analyze.
        
    Returns:
        dict: A dictionary containing the analysis results, including:
            - word_count: A list of tuples representing the most common words and their frequencies.
            - sentiment: A dictionary containing sentiment scores (positive, negative, neutral, compound).
            - readability: A float value.
    """
    words = re.findall(r'\b\w+\b', text.lower())
    word_count = Counter(words).most_common(20)
    sentiment = sia.polarity_scores(text)
    readability = textstat.flesch_kincaid_grade(text)

    return {
        'word_count': word_count,
        'sentiment': sentiment,
        'readability': readability
    }

def analyze_multiple_texts(texts):
    """
    Analyzes multiple texts, providing detailed sentiment analysis.
    
    Args:
        texts (list[str]): A list of text strings to be analyzed.
        
    Returns:
        list: List of dictionary contains analysis results for each text.
    """
    analysis_results = []
    
    for result in texts:
        analysis_results.append(analyze_text(result))
        
    return analysis_results


def generate_word_cloud(word_freq):
    """
    Generates a word cloud image from a list of dictionaries containing word frequencies.

    Args:
        word_freq (dict): A dictionary has the following key and value:
            - 'word' (str): The word itself.
            - 'frequency' (int): The frequency of the word.

    Returns:
        str: A base64 encoded string representing the generated word cloud image in PNG format.
            If an error occurs during generation, None is returned.
    """
    try:
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(word_freq)
        
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        
        img = BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        img_b64 = base64.b64encode(img.getvalue()).decode('utf-8')
        plt.close()
        
        return img_b64
    
    except Exception as e:
        logging.error(f"Error generating word cloud: {e}")
        return None

def handle_scraping_error(url, error_message):
    """
    Handles different scraping errors and returns a user-friendly error message.

    Args:
        url (str): The URL that caused the error.
        error_message (str): The raw error message from the scraper.

    Returns:
        dict: A dictionary containing the URL and the user-friendly error issue.
"""
    if "Invalid URL" in error_message:
        return {'URL': url, 'issue': 'Invalid URL format. Please check the URL.'}
    elif "NameResolutionError" in error_message:
        return {'URL': url, 'issue': 'Unable to resolve the domain. Please check the domain name.'}
    elif "403 Client Error" in error_message:
        return {'URL': url, 'issue': 'Access denied (403 Forbidden). This site may restrict scraping.'}
    elif "401 Client Error" in error_message:
        return {'URL': url, 'issue': 'Unauthorized access (401 Unauthorized). Authentication may be required.'}
    elif "404 Client Error" in error_message:
        return {'URL': url, 'issue': 'Page not found (404 Error). The requested page may have been removed or the URL may be incorrect.'}
    elif "Max retries exceeded" in error_message:
        return {'URL': url, 'issue': 'Connection timeout or server is unresponsive. Please try again later.'}
    else:
        return {'URL': url, 'issue': 'An unexpected error occurred during scraping.'}
