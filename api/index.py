from http.server import BaseHTTPRequestHandler
import json
import os

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
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
        if not HAS_REQUESTS:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'Requests not available'}).encode())
            return
        
        ML_API_URL = os.environ.get('ML_API_URL', '')
        
        if not ML_API_URL:
            self.send_response(503)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            error_msg = {
                'error': 'ML_API_URL environment variable not set',
                'message': 'Please configure ML_API_URL in Vercel settings'
            }
            self.wfile.write(json.dumps(error_msg).encode())
            return
        
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 0:
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
            else:
                data = {}
            
            response = requests.post(
                f'{ML_API_URL}/predict',
                json=data,
                timeout=30
            )
            
            self.send_response(response.status_code)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(response.content)
            
        except requests.exceptions.Timeout:
            self.send_response(504)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'ML API timeout'}).encode())
            
        except requests.exceptions.ConnectionError:
            self.send_response(503)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            error_msg = {'error': 'Cannot connect to ML API', 'url': ML_API_URL}
            self.wfile.write(json.dumps(error_msg).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode())
