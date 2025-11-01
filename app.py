from flask import Flask, request, Response
import requests
import urllib3
import json

# SSL warnings disable
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def proxy(path):
    try:
        url = f'https://api.sora2.ai/{path}'
        
        # Get all headers from request
        headers = {}
        for key, value in request.headers:
            if key.lower() not in ['host', 'content-length']:
                headers[key] = value
        
        # Add required headers
        headers['Origin'] = 'https://sora2.ai'
        headers['Referer'] = 'https://sora2.ai/'
        headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        
        # Log request details
        print(f"Request: {request.method} {url}")
        print(f"Headers: {json.dumps(headers, indent=2)}")
        
        if request.method in ['POST', 'PUT', 'PATCH']:
            body = request.get_data()
            print(f"Body: {body.decode('utf-8') if body else 'None'}")
        
        resp = requests.request(
            method=request.method,
            url=url,
            headers=headers,
            data=request.get_data() if request.method in ['POST', 'PUT', 'PATCH'] else None,
            params=request.args,
            verify=False,  # SSL verification disable
            timeout=60
        )
        
        print(f"Response Status: {resp.status_code}")
        print(f"Response Body: {resp.text[:500]}")  # First 500 chars
        
        # Create response
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        response_headers = [(name, value) for (name, value) in resp.raw.headers.items()
                          if name.lower() not in excluded_headers]
        
        return Response(
            resp.content,
            status=resp.status_code,
            headers=response_headers
        )
        
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return {'error': str(e), 'type': type(e).__name__}, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
