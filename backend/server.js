const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
// Remove HTTPS server and run HTTP server for development

const https = require('https');
const fs = require('fs');
const path = require('path');

const app = express();
const port = process.env.PORT || 5000;

app.use(cors({
  origin: '*', // Allow all origins for testing
}));
app.use(bodyParser.json());

// Middleware to log incoming requests
app.use((req, res, next) => {
  console.log('Incoming request: ' + req.method + ' ' + req.url);
  next();
});

// Health check endpoint
app.get('/', (req, res) => {
  res.send('Ad Variation Generator API is running');
});

  
// Generate 3 static image ads - dummy data
app.post('/generate-images', async (req, res) => {
  console.log('Request body:', req.body);
  const { productName, description, targetAudience } = req.body;

  if (!productName || !description || !targetAudience) {
    return res.status(400).json({ error: 'Missing required fields' });
  }

  // Return dummy image URLs pointing to frontend public directory
  const dummyImages = [
    'http://localhost:3000/ad1.png',
    'http://localhost:3000/ad2.png',
    'http://localhost:3000/ad3.png',
  ];

  res.json({ images: dummyImages });
});

// Generate 1 short video ad - dummy data
app.post('/generate-video', async (req, res) => {
  // Return a sample video URL pointing to frontend public directory
  const dummyVideoUrl = 'http://localhost:3000/video.mp4';
  res.json({ videoUrl: dummyVideoUrl });
});

// Read SSL certificate and key files
const options = {
  key: fs.readFileSync(path.join(__dirname, 'certs', 'key.pem')),
  cert: fs.readFileSync(path.join(__dirname, 'certs', 'cert.pem')),
};

// Create HTTPS server
https.createServer(options, app).listen(port, '0.0.0.0', () => {
  console.log('HTTPS Server is running on port ' + port);
});
