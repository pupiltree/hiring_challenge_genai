# Ad Variation Generator

An AI-powered tool that generates image and video advertisements based on product information.

## Features

- Generates 3 image ad variations using Hugging Face's Stable Diffusion (free tier)
- Creates 1 short video ad (using a placeholder video)
- Download generated content
- A/B testing for ad variations
- Basic analytics tracking

## Setup

### 1. Clone the repository
```bash
 git clone <your-repo-url>
 cd ad-generator
```

### 2. Install dependencies
```bash
cd frontend && npm install
cd ../backend && pip install -r requirements.txt
```

### 3. Set up environment variables
Create a `.env` file in the `backend` directory:
```
HF_API_KEY=your_huggingface_api_key_here
```
- Get your free Hugging Face API key from https://huggingface.co/settings/tokens

### 4. Run the application
#### Start the backend (Flask):
```bash
cd backend
python app.py
```
#### Start the frontend (Next.js):
```bash
cd ../frontend
npm run dev
```

- Frontend: http://localhost:3000
- Backend API: http://localhost:5000

## Usage
1. Open the frontend in your browser.
2. Fill out the ad form and submit.
3. Wait for the images and video to be generated.
4. Download or A/B test the results.

## Architecture
- **Frontend:** Next.js (React)
- **Backend:** Python Flask
- **Image Generation:** Hugging Face Inference API (Stable Diffusion)
- **Video Generation:** Placeholder video (no free video API)
- **Analytics:** JSON file storage

## Environment Variables
- `HF_API_KEY`: Your Hugging Face API key (required for image generation)

## Troubleshooting
- **Images not appearing:**
  - Check your Hugging Face API key and quota.
  - Make sure the backend `static/` directory exists.
  - Check backend logs for API errors.
- **Video is a placeholder:**
  - Free video generation is not available; a sample video is used.
- **CORS errors:**
  - Ensure both frontend and backend are running on localhost.

## FAQ
- **Can I use Replicate or OpenAI instead?**
  - Yes, but you must update the backend code and set up billing for those services.
- **Is this free?**
  - Hugging Face offers a limited free tier for image generation. For higher usage, upgrade your Hugging Face plan.
- **How do I deploy this?**
  - You can use Docker or deploy frontend/backend separately. Update environment variables as needed.

## Future Improvements
- Add support for paid image/video APIs (Replicate, OpenAI DALL·E)
- More customization options (color, style, etc.)
- User accounts and saved ads
- Advanced analytics

---

**Enjoy generating creative ad variations!** 