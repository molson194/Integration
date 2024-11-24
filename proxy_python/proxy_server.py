from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.request
import urllib.error
import json

class ProxyRequestHandler(BaseHTTPRequestHandler):
    # API and frontend target ports
    API_PORT = 5000
    FRONTEND_PORT = 8000
    
    def do_request(self, method):
        try:
            # Get the path from the incoming request
            path = self.path
            
            # Determine target port based on path
            # Routes starting with /api go to API_PORT, others to FRONTEND_PORT
            target_port = self.API_PORT if path.startswith('/api') else self.FRONTEND_PORT
            
            # Construct target URL
            target_url = f'http://localhost:{target_port}{path}'
            
            # Get request headers
            headers = {}
            for key, value in self.headers.items():
                if key.lower() not in ['host', 'content-length']:
                    headers[key] = value
            
            # Get request body for POST/PUT requests
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length) if content_length > 0 else None
            
            # Create the request
            request = urllib.request.Request(
                url=target_url,
                data=body,
                headers=headers,
                method=method
            )
            
            # Forward the request and get the response
            with urllib.request.urlopen(request) as response:
                # Copy response status code
                self.send_response(response.status)
                
                # Copy response headers
                for key, value in response.headers.items():
                    if key.lower() not in ['transfer-encoding']:
                        self.send_header(key, value)
                self.end_headers()
                
                # Copy response body
                self.wfile.write(response.read())
                
        except urllib.error.HTTPError as e:
            # Handle HTTP errors
            self.send_response(e.code)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                'error': str(e),
                'code': e.code
            }).encode())
            
        except Exception as e:
            # Handle other errors
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                'error': str(e),
                'code': 500
            }).encode())
    
    # Handle different HTTP methods
    def do_GET(self):
        self.do_request('GET')
        
    def do_POST(self):
        self.do_request('POST')
        
    def do_PUT(self):
        self.do_request('PUT')
        
    def do_DELETE(self):
        self.do_request('DELETE')
        
    def do_PATCH(self):
        self.do_request('PATCH')

def run_proxy_server(port=3000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, ProxyRequestHandler)
    print(f'Starting proxy server on port {port}...')
    print(f'Routing API requests (/api/*) to port {ProxyRequestHandler.API_PORT}')
    print(f'Routing frontend requests to port {ProxyRequestHandler.FRONTEND_PORT}')
    httpd.serve_forever()

if __name__ == '__main__':
    run_proxy_server()
