"""
Lightweight API handler for Vercel deployment.
This file calls the actual ML API hosted elsewhere to avoid size limits.
"""
import json
import os

# Try to import requests
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False


def handler(event, context):
    """
    Main handler function for Vercel serverless
    """
    # Get request method and path
    method = event.get('httpMethod', event.get('method', 'GET'))
    path = event.get('path', event.get('rawPath', '/'))
    
    # GET request - return API info
    if method == 'GET':
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'status': 'ok',
                'message': 'Document Classifier API - Vercel Endpoint',
                'endpoints': {
                    '/api/classify': 'POST - Classify document text',
                    '/api/health': 'GET - Health check'
                }
            })
        }
    
    # POST request - forward to ML API
    if method == 'POST':
        if not HAS_REQUESTS:
            return {
                'statusCode': 500,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'Requests library not available'})
            }
        
        # Get the ML API URL from environment variable
        ML_API_URL = os.environ.get('ML_API_URL', '')
        
        if not ML_API_URL:
            return {
                'statusCode': 503,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({
                    'error': 'ML_API_URL environment variable not set',
                    'message': 'Please configure ML_API_URL in Vercel environment variables'
                })
            }
        
        try:
            # Parse request body
            body = event.get('body', '{}')
            if isinstance(body, str):
                data = json.loads(body)
            else:
                data = body
            
            # Forward request to actual ML API
            response = requests.post(
                f'{ML_API_URL}/predict',
                json=data,
                timeout=30
            )
            
            return {
                'statusCode': response.status_code,
                'headers': {'Content-Type': 'application/json'},
                'body': response.text
            }
            
        except requests.exceptions.Timeout:
            return {
                'statusCode': 504,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'Request to ML API timed out'})
            }
            
        except requests.exceptions.ConnectionError:
            return {
                'statusCode': 503,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({
                    'error': 'Could not connect to ML API',
                    'ml_api_url': ML_API_URL
                })
            }
            
        except Exception as e:
            return {
                'statusCode': 500,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': str(e)})
            }
    
    # Method not allowed
    return {
        'statusCode': 405,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps({'error': 'Method not allowed'})
    }
