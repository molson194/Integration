const http = require('http');
const httpProxy = require('http-proxy');

const proxy = httpProxy.createProxyServer({});
const frontendPort = 8000;
const backendPort = 5000;

const server = http.createServer((req, res) => {
  // If the request starts with /api, forward to the backend
  if (req.url.startsWith('/api')) {
    proxy.web(req, res, { target: `http://127.0.0.1:${backendPort}` });
  } else {
    // Otherwise, serve the frontend
    proxy.web(req, res, { target: `http://127.0.0.1:${frontendPort}` });
  }
});

server.listen(3000, () => {
  console.log('Proxy server is running on http://127.0.0.1:3000');
});
