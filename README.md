# Ad Variation Generator

## Project Overview
This project is a web application that allows users to generate ad variations based on product information. Users input a product name, description, and target audience, and the app generates 3 static image ad variations and 1 short video ad. Users can view and download the generated content.

## Features
- Input form for product name, description, and target audience.
- Generates 3 static image ads (currently dummy images).
- Generates 1 short video ad (currently a dummy video).
- Displays generated ads with download links.
- Basic error handling and loading states.
- Clean and responsive UI.
- Proxy setup for API requests between frontend and backend.

## Technical Details

### Frontend
- Built with React.
- Components:
  - `InputForm`: Handles user input and API requests.
  - `ResultsPage`: Displays generated ads and video.
- Uses Axios for HTTP requests.
- Proxy middleware configured to forward API requests to backend.

### Backend
- Built with Node.js and Express.
- Provides API endpoints:
  - `POST /generate-images`: Returns URLs of 3 dummy images.
  - `POST /generate-video`: Returns URL of a dummy video.
- Serves HTTPS with self-signed SSL certificates (for development).
- Logs incoming requests for debugging.

### Static Assets
- Dummy images and video are hosted in the frontend `public` directory.

## Setup Instructions

### Backend
1. Navigate to the `backend` directory.
2. Generate SSL certificates as per `backend/README_SSL_SETUP.md` (optional for HTTPS).
3. Install dependencies:
   ```
   npm install
   ```
4. Start the backend server:
   ```
   npm start
   ```

### Frontend
1. Navigate to the `frontend` directory.
2. Install dependencies:
   ```
   npm install
   ```
3. Start the frontend development server:
   ```
   npm start
   ```
4. The app will be available at `http://localhost:3000`.

## Docker Setup

A Dockerfile is included to build and run the application in a containerized environment.

### Build Docker Image
```
docker build -t ad-variation-generator .
```

### Run Docker Container
```
docker run -p 3000:3000 -p 5000:5000 ad-variation-generator
```

## Notes
- Currently, the image and video generation use dummy static files.
- The project is structured to allow easy integration of AI-based generation models or APIs in the future.
- SSL setup is for development only; production should use trusted certificates.

## Future Improvements
- Integrate AI image and video generation models.
- Add customization options for ad generation.
- Implement A/B testing and analytics.
- Optimize performance and cost.

