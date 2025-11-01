from flask import Flask, request, Response
import requests
import urllib3

# SSL warnings disable
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def proxy(path):
    try:
        url = f'https://api.sora2.ai/{path}'
        
        headers = dict(request.headers)
        headers['Origin'] = 'https://sora2.ai'
        headers['Referer'] = 'https://sora2.ai/'
        headers.pop('Host', None)
        
        resp = requests.request(
            method=request.method,
            url=url,
            headers=headers,
            data=request.get_data(),
            params=request.args,
            verify=False,  # SSL verification disable
            timeout=30
        )
        
        return Response(
            resp.content,
            status=resp.status_code,
            headers=dict(resp.headers)
        )
    except Exception as e:
        return {'error': str(e)}, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
