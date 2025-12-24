from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
import logging
from typing import List, Dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

df = None
vectorizer = None
tfidf_matrix = None


def ensure_csv_exists():
    csv_file = os.environ.get('CSV_FILE', 'scrapping_results.csv')
    if not os.path.exists(csv_file):
        logger.warning(f"CSV file not found: {csv_file}. Generating sample data...")
        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location("generate_1000_articles", "generate_1000_articles.py")
            if spec and spec.loader:
                generate_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(generate_module)
                generate_module.create_1000_articles_csv(csv_file)
                logger.info(f"Sample data generated: {csv_file}")
                return True
        except Exception as e:
            logger.error(f"Failed to generate CSV: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
    return os.path.exists(csv_file)


def load_data(csv_file: str = 'scrapping_results.csv'):
    global df, vectorizer, tfidf_matrix
    
    try:
        if not os.path.exists(csv_file):
            logger.error(f"CSV file not found: {csv_file}")
            return False
        
        df = pd.read_csv(csv_file)
        logger.info(f"Loaded {len(df)} articles from {csv_file}")
        
        df['combined_text'] = (
            df['title'].fillna('') + ' ' +
            df['subtitle'].fillna('') + ' ' +
            df['text'].fillna('') + ' ' +
            df['keywords'].fillna('')
        )
        
        df['claps'] = pd.to_numeric(df['claps'], errors='coerce').fillna(0)
        df['combined_text'] = df['combined_text'].fillna('')
        
        vectorizer = TfidfVectorizer(
            max_features=5000,
            stop_words='english',
            ngram_range=(1, 2),
            min_df=2
        )
        
        tfidf_matrix = vectorizer.fit_transform(df['combined_text'])
        logger.info("TF-IDF matrix created successfully")
        
        return True
        
    except Exception as e:
        logger.error(f"Error loading data: {str(e)}")
        return False


def find_similar_articles(query: str, top_n: int = 10) -> List[Dict]:
    global df, vectorizer, tfidf_matrix
    
    if df is None or vectorizer is None or tfidf_matrix is None:
        return []
    
    try:
        query_vector = vectorizer.transform([query])
        
        similarities = cosine_similarity(query_vector, tfidf_matrix).flatten()
        
        df_temp = df.copy()
        df_temp['similarity'] = similarities
        
        df_temp = df_temp[df_temp['similarity'] > 0]
        
        df_sorted = df_temp.sort_values(
            by=['claps', 'similarity'],
            ascending=[False, False]
        )
        
        top_results = df_sorted.head(top_n)
        
        results = []
        for _, row in top_results.iterrows():
            results.append({
                'url': str(row['url']),
                'title': str(row['title']),
                'claps': int(row['claps']) if pd.notna(row['claps']) else 0,
                'similarity_score': float(row['similarity'])
            })
        
        return results
        
    except Exception as e:
        logger.error(f"Error finding similar articles: {str(e)}")
        return []


@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'healthy',
        'data_loaded': df is not None,
        'articles_count': len(df) if df is not None else 0
    })


@app.route('/search', methods=['POST', 'GET'])
def search():
    try:
        if request.method == 'POST':
            data = request.get_json() or {}
            query = data.get('query', '') or request.form.get('query', '')
            top_n = int(data.get('top_n', 10) or request.form.get('top_n', 10))
        else:
            query = request.args.get('query', '')
            top_n = int(request.args.get('top_n', 10))
        
        if not query:
            return jsonify({
                'error': 'Query parameter is required',
                'usage': 'Send "query" parameter with text or keywords'
            }), 400
        
        if df is None:
            return jsonify({
                'error': 'Data not loaded. Please ensure scrapping_results.csv exists.'
            }), 500
        
        results = find_similar_articles(query, top_n)
        
        if not results:
            return jsonify({
                'message': 'No similar articles found',
                'query': query,
                'results': []
            })
        
        return jsonify({
            'query': query,
            'count': len(results),
            'results': results
        })
        
    except Exception as e:
        logger.error(f"Error in search endpoint: {str(e)}")
        return jsonify({
            'error': str(e)
        }), 500


@app.route('/', methods=['GET'])
def index():
    return jsonify({
        'name': 'Medium Article Search API',
        'version': '1.0.0',
        'endpoints': {
            '/health': 'GET - Health check',
            '/search': 'POST/GET - Search for similar articles',
            '/': 'GET - This documentation'
        },
        'usage': {
            'search': {
                'method': 'POST or GET',
                'parameters': {
                    'query': 'Text or keywords to search for (required)',
                    'top_n': 'Number of results to return (optional, default: 10)'
                },
                'example_post': {
                    'url': '/search',
                    'method': 'POST',
                    'body': {'query': 'machine learning', 'top_n': 10}
                },
                'example_get': {
                    'url': '/search?query=machine+learning&top_n=10',
                    'method': 'GET'
                }
            }
        }
    })


csv_file = os.environ.get('CSV_FILE', 'scrapping_results.csv')
ensure_csv_exists()
if load_data(csv_file):
    logger.info("API ready to serve requests")
else:
    logger.error("Data not loaded. API will return errors until data is available.")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
