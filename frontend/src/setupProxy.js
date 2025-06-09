const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function(app) {
  app.use(
    ['/generate-images', '/generate-video'],
    createProxyMiddleware({
      target: 'https://localhost:5000',
      secure: false, // Accept self-signed certs
      changeOrigin: true,
    })
  );
};
