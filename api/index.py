"""
Lightweight API handler for Vercel deployment.
This file calls the actual ML API hosted elsewhere to avoid size limits.
"""
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Try to import requests, fallback to basic response if not available
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False


@app.route('/')
@app.route('/api')
def index():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'message': 'Document Classifier API - Vercel Endpoint',
        'endpoints': {
            '/api/classify': 'POST - Classify document text',
            '/api/health': 'GET - Health check'
        }
    })


@app.route('/api/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'doc-classifier-proxy'
    })


@app.route('/api/classify', methods=['POST'])
def classify():
    """Classify document text by forwarding to ML API"""
    if not HAS_REQUESTS:
        return jsonify({
            'error': 'Requests library not available'
        }), 500
    
    # Get the ML API URL from environment variable
    ML_API_URL = os.environ.get('ML_API_URL', '')
    
    if not ML_API_URL:
        return jsonify({
            'error': 'ML_API_URL environment variable not set',
            'message': 'Please configure ML_API_URL in Vercel environment variables'
        }), 503
    
    try:
        data = request.get_json()
        
        # Forward request to actual ML API
        response = requests.post(
            f'{ML_API_URL}/predict',
            json=data,
            timeout=30
        )
        
        return response.json(), response.status_code
        
    except requests.exceptions.Timeout:
        return jsonify({
            'error': 'Request to ML API timed out'
        }), 504
        
    except requests.exceptions.ConnectionError:
        return jsonify({
            'error': 'Could not connect to ML API',
            'ml_api_url': ML_API_URL
        }), 503
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500
