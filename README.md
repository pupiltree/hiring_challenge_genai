# GenAI Ad Variation Generator

This project is my submission for the Powersmy.biz GenAI Engineer (Image/Video) Intern Challenge. It is a web application that generates ad variations (images, and soon video) based on product information using generative AI models.

---

## Features Implemented
- **Input Form:** Enter product name, description, and target audience
- **Image Generation:** Generates 3 ad image variations using real AI (Stability AI SDXL engine)
- **Results Page:** Displays all generated images with download buttons
- **Download Option:** Download any generated image
- **A/B Preference Testing:** Select your favorite ad variation (bonus feature)
- **Responsive UI:** Clean, modern, and mobile-friendly
- **Error Handling & Loading States:** User-friendly feedback during generation
- **Improved Code Structure:** Main logic is in `Body.jsx`, keeping `App.jsx` clean and readable

---

## Not Yet Completed
- **Video Generation:** Not yet implemented (will add a video endpoint and UI soon)
- **Other Bonus Features:** (customization, analytics) not yet implemented

---

## Architecture
- **Frontend:** React (Vite) — `/client`
  - `App.jsx`: Page structure and header
  - `Body.jsx`: Main form, image results, and A/B preference logic
- **Backend:** FastAPI (Python) — `/server`
- **Communication:** REST API calls from frontend to backend
- **Image Generation:**
  - **Stability AI SDXL engine** for real, high-quality ad images
  - Modular and ready for further improvements

---

## 🛠️ Setup Instructions

### Prerequisites
- Node.js & npm
- Python 3.8+

### Backend (FastAPI)
```bash
cd hiring_challenge_genai/server
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
# Add your Stability AI API key to .env
# STABILITY_API_KEY=your_key_here
uvicorn main:app --reload
```

### Frontend (React + Vite)
```bash
cd hiring_challenge_genai/client
npm install
npm run dev
```

---

## 🤖 Model/API Choices & Justification
- **Stability AI SDXL:** Used for real image generation (reliable, high-quality, free tier available).
- **Mock Images:** Used for development and UI testing if needed.
- **Hugging Face/Replicate/Bria:** Explored but faced billing or access issues.

---

## 📝 Future Improvements
- Add video ad generation (using RunwayML, Stability AI, or mock video)
- Add customization options (aspect ratio, tone, style)
- Add analytics to track ad performance
- Polish UI/UX further
- Add Dockerfile for easy deployment

---

## 📋 Assignment Coverage
-  Product info input
-  3 image ad variations (real AI)
-  Download option
-  Responsive UI
-  Error handling/loading
-  Results page
-  A/B preference testing (bonus)
---

## 🙋 Notes
- All core web app/image requirements are met with real AI image generation.
- Video generation and some bonus features are planned but not yet implemented.
- Code is modular, clean, and easy to maintain.

---

**Thank you for reviewing my submission!**
