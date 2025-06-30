from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import requests
from dotenv import load_dotenv
import base64

load_dotenv()

app = FastAPI()

# CORS setup for local frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

STABILITY_API_KEY = os.getenv("STABILITY_API_KEY")

class AdRequest(BaseModel):
    product_name: str
    description: str
    target_audience: str

@app.get("/")
def read_root():
    return {"message": "FastAPI backend is running!"}

@app.post("/generate-images")
def generate_images(ad_request: AdRequest):
    if not STABILITY_API_KEY:
        raise HTTPException(status_code=500, detail="Stability AI API key not set.")

    prompt = f"Ad for {ad_request.product_name}: {ad_request.description} Target audience: {ad_request.target_audience}. Professional, eye-catching, high quality."
    headers = {
        "Authorization": f"Bearer {STABILITY_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "text_prompts": [{"text": prompt}],
        "cfg_scale": 7,
        "clip_guidance_preset": "FAST_BLUE",
        "height": 1024,
        "width": 1024,
        "samples": 1,
        "steps": 30
    }
    image_urls = []
    for _ in range(3):
        response = requests.post(
            "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image",
            headers=headers,
            json=data
        )
        if response.status_code == 200:
            result = response.json()
            image_base64 = result["artifacts"][0]["base64"]
            image_urls.append(f"data:image/png;base64,{image_base64}")
        else:
            print("Stability AI error:", response.status_code, response.text)
            image_urls.append("https://placehold.co/512x512/FF6B6B/FFF?text=Image+Generation+Failed")
    return {"images": image_urls} 