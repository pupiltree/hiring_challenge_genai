import requests
from typing import List, Dict
import os

class AdGenerator:
    def __init__(self):
        self.hf_api_key = os.getenv('HF_API_KEY')
        if not self.hf_api_key:
            raise ValueError("HF_API_KEY environment variable is not set.")
        self.hf_api_url = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1"

    def generate_image_ads(self, product_info: Dict) -> List[str]:
        """Generate 3 image ad variations using Hugging Face Stable Diffusion."""
        base_prompt = self._create_image_prompt(product_info)
        variations = [
            f"{base_prompt}, professional product photography",
            f"{base_prompt}, vibrant colors, pop art style",
            f"{base_prompt}, minimalist design, white background"
        ]
        image_urls = []
        for idx, prompt in enumerate(variations):
            try:
                response = requests.post(
                    self.hf_api_url,
                    headers={"Authorization": f"Bearer {self.hf_api_key}"},
                    json={"inputs": prompt}
                )
                if response.status_code == 200:
                    # Save image to static folder and return URL
                    img_path = f"static/ad_image_{idx}.png"
                    with open(img_path, "wb") as f:
                        f.write(response.content)
                    image_urls.append(f"/static/ad_image_{idx}.png")
                else:
                    print(f"Hugging Face API error: {response.status_code} {response.text}")
            except Exception as e:
                print(f"Error generating image for prompt '{prompt}': {e}")
        return image_urls

    def generate_video_ad(self, product_info: Dict) -> str:
        # No free video API, return placeholder
        return "https://www.w3schools.com/html/mov_bbb.mp4"

    def _create_image_prompt(self, product_info: Dict) -> str:
        return (f"Create an advertisement for {product_info['productName']}. "
                f"Product details: {product_info['description']}. "
                f"Target audience: {product_info['audience']}. "
                "High quality, 4K resolution.")

    def _create_video_prompt(self, product_info: Dict) -> str:
        return (f"Create a 10-second promotional video for {product_info['productName']}. "
                f"Show the product in use with happy customers. "
                f"Target audience: {product_info['audience']}. "
                "Cinematic quality, smooth transitions.") 