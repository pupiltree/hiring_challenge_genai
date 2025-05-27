from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

def get_image_prompt(product_name, description, target_audience, tone, style):
    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

    prompt = (
        f"Generate a detailed visual description for an advertisement image.\n\n"
        f"Product Name: {product_name}\n"
        f"Description: {description}\n"
        f"Target Audience: {target_audience}\n"
        f"Tone: {tone} \n"
        f"Style: {style} \n\n"
        f"The image should visually appeal to the audience and reflect the tone and style."
    )

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
    )

    return response.text


def get_video_prompt(product_name, description, target_audience, tone, style, length=8):
    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

    prompt = (
        f"Generate a script and visual storyboard description for a short advertisement video.\n\n"
        f"Product Name: {product_name}\n"
        f"Description: {description}\n"
        f"Target Audience: {target_audience}\n"
        f"Tone: {tone} \n"
        f"Style: {style} \n\n"
        f"Video length: {length} seconds\n\n"
        f"The video should be engaging and convey the product's key value proposition effectively."
    )

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
    )

    return response.text
