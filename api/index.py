"""
Lightweight API handler for Vercel deployment.
This file calls the actual ML API hosted elsewhere to avoid size limits.
"""
import json
import os
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import requests


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        response = {
            'status': 'ok',
            'message': 'Document Classifier API - Vercel Endpoint',
            'endpoints': {
                '/api/classify': 'POST - Classify document text',
                '/api/health': 'GET - Health check'
            }
        }
        self.wfile.write(json.dumps(response).encode())
        return
    
    def do_POST(self):
        """Handle POST requests"""
        # Get the ML API URL from environment variable
        ML_API_URL = os.environ.get('ML_API_URL', 'http://localhost:5001')
        
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
            
            # Parse the path
            parsed_path = urlparse(self.path)
            
            if parsed_path.path == '/api/classify':
                # Forward request to actual ML API
                response = requests.post(
                    f'{ML_API_URL}/predict',
                    json=data,
                    timeout=30
                )
                
                self.send_response(response.status_code)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(response.content)
                
            else:
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                error_response = {'error': 'Endpoint not found'}
                self.wfile.write(json.dumps(error_response).encode())
                
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            error_response = {'error': str(e)}
            self.wfile.write(json.dumps(error_response).encode())
