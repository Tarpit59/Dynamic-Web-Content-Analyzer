from flask import render_template, request, jsonify
from base.com.service.service import scrape_multiple_urls, analyze_multiple_texts, generate_word_cloud, handle_scraping_error
from base import app
import logging
import re

logging.basicConfig(level=logging.INFO)

url_regex = re.compile(
    r'^(?:http|ftp)s?://'  # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain
    r'localhost|'  # localhost
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # IPv4
    r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # IPv6
    r'(?::\d+)?'  # port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        urls = request.json.get('urls', [])
        if not urls:
            return jsonify({"error": "No URLs provided."}), 400
        
        invalid_urls = []
        
        for url in urls:
            if not re.match(url_regex, url):
                invalid_urls.append(handle_scraping_error(url, "Invalid URL format"))
        
        if invalid_urls:
            return jsonify({"invalid_urls": invalid_urls}), 400
        
        scrape_results = scrape_multiple_urls(urls)
        
        valid_texts = []
        
        for i, result in enumerate(scrape_results):
            if not isinstance(result, dict):
                logging.error(f"Unexpected result type for URL {urls[i]}: {type(result)}")
                invalid_urls.append(handle_scraping_error(urls[i], 'Unexpected result format'))
                continue

            if result['error'] != None:
                invalid_urls.append(handle_scraping_error(urls[i], result['error']))
            else:
                valid_texts.append(result['text'])

        if invalid_urls:
            return jsonify({"invalid_urls": invalid_urls}), 400

        analysis = analyze_multiple_texts(valid_texts)

        sentiment_comparison = []
        readability_comparison = []
        word_frequencies = []

        for i, a in enumerate(analysis):
            url_label = f"URL {i+1}"
            
            sentiment_comparison.append({
                'URL': url_label,
                'Positive': a['sentiment']['pos'],
                'Neutral': a['sentiment']['neu'],
                'Negative': a['sentiment']['neg']
            })

            readability_comparison.append({
                'URL': url_label,
                'Readability': a['readability']
            })

            word_frequencies.append({
                'URL': url_label,
                'words': [w for w, c in a['word_count']],
                'counts': [c for w, c in a['word_count']]
            })

        word_clouds = []
        
        for freq_data in word_frequencies:
            word_freq_dict = dict(zip(freq_data['words'], freq_data['counts']))
            word_cloud_img = generate_word_cloud(word_freq_dict)
            if word_cloud_img:
                word_clouds.append({
                    'URL': freq_data['URL'],
                    'word_cloud': word_cloud_img
                })
                
            else:
                word_clouds.append({
                    'URL': freq_data['URL'],
                    'word_cloud': None
                })

        return jsonify({
            'sentiment_comparison': sentiment_comparison,
            'readability_comparison': readability_comparison,
            'word_clouds': word_clouds
        })

    except Exception as e:
        logging.error(f"Error occured: {e}")
        return jsonify({"error": "An error occurred."}), 500