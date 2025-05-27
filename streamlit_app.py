import streamlit as st

# THIS MUST BE THE FIRST STREAMLIT COMMAND
st.set_page_config(layout="wide")

import vertexai
from vertexai.preview.vision_models import ImageGenerationModel
from google import genai
from google.genai import types
import time
import os
import traceback
from llm import get_image_prompt, get_video_prompt

from dotenv import load_dotenv

load_dotenv()

# ---------- CONFIGURATION (Replace with your details) ----------          
IMAGE_MODEL_NAME = "imagen-4.0-generate-preview-05-20"
VIDEO_MODEL_NAME = "veo-2.0-generate-001"

IMAGE_OUTPUT_DIR = "generated_images"
VIDEO_OUTPUT_DIR = "generated_videos"
# -----------------------------------

# Ensure output directories exist
os.makedirs(IMAGE_OUTPUT_DIR, exist_ok=True)
os.makedirs(VIDEO_OUTPUT_DIR, exist_ok=True)

# Initialize Vertex AI (do this once)
def initialize_vertex_ai():
    try:
        vertexai.init(project=os.getenv("PROJECT_ID"), location=os.getenv("LOCATION"))
        return True, f"Vertex AI initialized"
    except Exception as e:
        return False, f"Error initializing Vertex AI: {e}"

# Cache Vertex AI clients
@st.cache_resource
def get_image_generation_model():
    try:
        return ImageGenerationModel.from_pretrained(IMAGE_MODEL_NAME)
    except Exception as e:
        st.error(f"Error loading image model '{IMAGE_MODEL_NAME}': {e}")
        return None

@st.cache_resource
def get_video_generation_client():
    try:
        return genai.Client(vertexai=True, project=os.getenv("PROJECT_ID"), location=os.getenv("LOCATION"))
    except Exception as e:
        st.error(f"Error creating video client: {e}")
        return None

def generate_advertisement_images(product_name, description, target_audience, tone, style, num_images=3):
    image_model = get_image_generation_model()
    if not image_model:
        st.error("Image model not available.")
        return []

    prompt = get_image_prompt(product_name, description, target_audience, tone, style)  

    st.info(f"🖼️ Generating {num_images} images with prompt:\n---\n{prompt}\n---")
    image_paths = []
    try:
        with st.spinner(f"Generating {num_images} images... (this may take a moment)"):
            images = image_model.generate_images(
                prompt=prompt,
                number_of_images=num_images,
                aspect_ratio="16:9", # Common ad aspect ratio
                add_watermark=False # Per Vertex AI docs, watermark is False by default for imagen 3+ and not recommended for programmatic control
            )

        for i, img in enumerate(images):
            image_filename = os.path.join(IMAGE_OUTPUT_DIR, f"ad_image_{product_name.replace(' ','_')}_{i+1}.png")
            if hasattr(img, '_image_bytes') and img._image_bytes:
                with open(image_filename, "wb") as f:
                    f.write(img._image_bytes)
                image_paths.append(image_filename)
                st.success(f"✅ Image saved: {image_filename}")
            else:
                st.warning(f"⚠️ Could not get image bytes for image {i+1}.")
        
        if image_paths:
             st.success(f"✅ {len(image_paths)} Images generated successfully.")
        else:
            st.error("❌ No images were generated or saved.")

    except Exception as e:
        st.error(f"❌ Error during image generation: {e}")
        traceback.print_exc()
    return image_paths

def generate_advertisement_video(product_name, description, target_audience, tone, style):
    video_client = get_video_generation_client()
    if not video_client:
        st.error("Video client not available.")
        return None

    prompt = get_video_prompt(product_name, description, target_audience, tone, style)  
    st.info(f"🎬 Generating video with prompt:\n---\n{prompt}\n---")
    video_path = None
    try:
        with st.spinner("Generating video... (this may take several minutes)"):
            operation = video_client.models.generate_videos(
                model=VIDEO_MODEL_NAME,
                prompt=prompt,
                config=types.GenerateVideosConfig(
                    aspect_ratio="16:9",
                    number_of_videos=1,
                    duration_seconds=8,
                    person_generation="allow", # As per previous requirement
                    enhance_prompt=True,
                ),
            )

            st.write("⏳ Video generation operation submitted. Waiting for completion...")
            progress_bar = st.progress(0)
            i = 0
            max_checks = 80 # Approx 20 minutes (80 * 15s)
            
            while not operation.done and i < max_checks:
                time.sleep(15) 
                try:
                    operation = video_client.operations.get(operation) # Refresh operation status
                except Exception as op_get_err:
                    st.warning(f"Could not refresh operation status: {op_get_err}")
                    # Potentially break or continue, depending on error type. For now, continue a few times.
                    if i > max_checks -3 : # If near end, break
                        st.error("Failed to get operation status repeatedly.")
                        break
                
                progress_text = "Video generation in progress..."
                if hasattr(operation, 'metadata') and operation.metadata:
                    if hasattr(operation.metadata, 'progress_message'):
                         progress_text = operation.metadata.progress_message
                    elif hasattr(operation.metadata, 'partial_result') and operation.metadata.partial_result:
                         progress_text = f"Partial result: {operation.metadata.partial_result}"

                st.write(f"   {progress_text} (Check {i+1}/{max_checks})")
                progress_bar.progress(min(1.0, (i + 1) / float(max_checks*0.8))) # Adjust progress visualization
                i += 1
            
            if i >= max_checks and not operation.done:
                st.error("Video generation timed out.")
                return None

            progress_bar.progress(1.0)
            st.write("🏁 Video generation operation finished processing.")

            if operation.response and operation.result:
                result = operation.result
                if hasattr(result, 'generated_videos') and result.generated_videos:
                    generated_video_entry = result.generated_videos[0]
                    if generated_video_entry and hasattr(generated_video_entry, 'video'):
                        video_object = generated_video_entry.video
                        if video_object and hasattr(video_object, 'video_bytes') and video_object.video_bytes:
                            video_filename = os.path.join(VIDEO_OUTPUT_DIR, f"ad_video_{product_name.replace(' ','_')}.mp4")
                            with open(video_filename, "wb") as f:
                                f.write(video_object.video_bytes)
                            video_path = video_filename
                            st.success(f"✅ Video generated and saved locally at: {os.path.abspath(video_path)}")
                        else:
                            st.error("❌ Video data (bytes) not found in the response.")
                    else:
                        st.error("❌ Video object or its attributes missing in the response.")
                elif hasattr(result, 'rai_media_filtered_count') and result.rai_media_filtered_count > 0:
                    st.error(f"❌ Video generation was filtered by Responsible AI policies.")
                    if hasattr(result, 'rai_media_filtered_reasons'):
                        st.error(f"Reasons: {result.rai_media_filtered_reasons}")
                else:
                    st.error("❌ No 'generated_videos' found in the result, or it was empty.")
                
                if not video_path: # Print full result for debugging if no video path
                    st.json(str(result))

            elif hasattr(operation, 'error') and operation.error:
                 st.error(f"❌ Video generation failed with error: Code {operation.error.code}, Message: {operation.error.message}")
            else:
                st.error("❌ Video generation failed or operation result/response is empty.")

    except Exception as e:
        st.error(f"❌ An error occurred during video generation: {e}")
        traceback.print_exc()
    return video_path

# --- Streamlit App UI ---
st.title("🚀 AI Advertisement Content Generator")
st.markdown("Generate 3 images and 1 video for your product advertisement using Vertex AI.")

# Initialize Vertex AI and show status
vertex_success, vertex_message = initialize_vertex_ai()
if vertex_success:
    st.sidebar.success(vertex_message)
else:
    st.sidebar.error(vertex_message)
    st.stop()

# Initialize session state for form data
if 'product_name' not in st.session_state:
    st.session_state.product_name = ""
if 'description' not in st.session_state:
    st.session_state.description = ""
if 'target_audience' not in st.session_state:
    st.session_state.target_audience = ""
if 'tone' not in st.session_state:
    st.session_state.tone = ""
if 'style' not in st.session_state:
    st.session_state.style = ""

st.sidebar.header("💡 Sample Data")
if st.sidebar.button("Load Sample Data"):
    st.session_state.product_name = "NovaBloom Smart Garden"
    st.session_state.description = "An AI-powered indoor garden that automatically manages light, water, and nutrients for your herbs and vegetables. Grow fresh produce year-round, effortlessly."
    st.session_state.target_audience = "Urban dwellers, tech enthusiasts, busy professionals, aspiring home gardeners."
    st.session_state.tone = "Innovative, fresh, effortless, vibrant."
    st.session_state.style = "Sleek, modern, organic, tech-integrated."
    st.rerun()

st.header("📝 Input Product Details")
product_name = st.text_input("Product Name", value=st.session_state.product_name, placeholder="e.g., EcoGlow Solar Lamp", key="product_name_input")
description = st.text_area("Product Description", value=st.session_state.description, placeholder="e.g., A stylish, energy-efficient solar lamp that brightens your outdoor spaces.", height=100, key="description_input")
target_audience = st.text_input("Target Audience", value=st.session_state.target_audience, placeholder="e.g., Eco-conscious homeowners, garden enthusiasts", key="target_audience_input")
tone = st.text_input("Desired Tone", value=st.session_state.tone, placeholder="e.g., Inspiring, warm, reliable", key="tone_input")
style = st.text_input("Desired Visual Style", value=st.session_state.style, placeholder="e.g., Minimalist, natural, vibrant, futuristic", key="style_input")

# Update session state when inputs change
st.session_state.product_name = product_name
st.session_state.description = description
st.session_state.target_audience = target_audience
st.session_state.tone = tone
st.session_state.style = style

if st.button("✨ Generate Advertisement Content", type="primary"):
    if not all([st.session_state.product_name, st.session_state.description, st.session_state.target_audience, st.session_state.tone, st.session_state.style]):
        st.warning("Please fill in all product details.")
    else:
        # Check if models are available
        image_model = get_image_generation_model()
        video_client = get_video_generation_client()
        
        if not image_model or not video_client:
            st.error("Models not initialized. Check sidebar for errors.")
        else:
            st.balloons()
            st.subheader("🖼️ Generated Images")
            generated_image_paths = generate_advertisement_images(
                st.session_state.product_name, 
                st.session_state.description, 
                st.session_state.target_audience, 
                st.session_state.tone, 
                st.session_state.style
            )
            if generated_image_paths:
                cols = st.columns(len(generated_image_paths))
                for i, img_path in enumerate(generated_image_paths):
                    with cols[i]:
                        st.image(img_path, caption=f"Ad Image {i+1}", use_container_width=True)
            else:
                st.write("No images were generated.")

            st.subheader("🎬 Generated Video")
            generated_video_path = generate_advertisement_video(
                st.session_state.product_name, 
                st.session_state.description, 
                st.session_state.target_audience, 
                st.session_state.tone, 
                st.session_state.style
            )
            if generated_video_path:
                st.video(generated_video_path)
            else:
                st.write("No video was generated.")
else:
    st.markdown("--- \n Fill in the details and click 'Generate' to create your ad content!")

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Configuration:**")
st.sidebar.markdown(f"Project ID: {os.getenv('PROJECT_ID')}")
st.sidebar.markdown(f"Location: {os.getenv('LOCATION')}")
st.sidebar.markdown(f"Image Model: `{IMAGE_MODEL_NAME}`")
st.sidebar.markdown(f"Video Model: `{VIDEO_MODEL_NAME}`")
st.sidebar.markdown("---")
st.sidebar.info("Note: Video generation can take several minutes. Please be patient.")