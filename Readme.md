# 🚀 AI Advertisement Content Generator using Vertex AI

This project is a Streamlit-based web app that generates **advertisement images and videos** for a product using **Google Cloud Vertex AI's Imagen and Veo models**.
## SAMPLE GENERATED AD:
* **Product Name**: NovaBloom Smart Garden
* **Description**: An AI-powered indoor garden that automatically manages light, water, and nutrients for your herbs and vegetables. Grow fresh produce year-round, effortlessly.
* **Target Audience**: Urban dwellers, tech enthusiasts, busy professionals, aspiring home gardeners.
* **Tone**: Innovative, fresh, effortless, vibrant.
* **Style**: Sleek, modern, organic, tech-integrated.

## GENERATED AD
https://github.com/user-attachments/assets/e39f0725-f518-45b1-a4a5-a7e96265495c

## DEMO VIDEO:
https://github.com/user-attachments/assets/7c7075f3-e1f4-44ac-ac54-b4bca98e8912


## 🌐 Prerequisites

- Google Cloud Project with **Vertex AI** enabled.
- Python ≥ 3.10.
- Conda or `virtualenv` for creating an isolated environment.
- Google Cloud SDK (gcloud CLI).

## 🔧 Setup Instructions

### 1. Install Google Cloud SDK

Follow instructions to install the gcloud CLI from the official docs:  
👉 https://cloud.google.com/sdk/docs/install

Once installed, authenticate and set your project:
```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
````

### 2. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/ai-ad-generator.git
cd ai-ad-generator
```

### 3. Create Conda Environment & Install Dependencies

```bash
conda create -n adgen python=3.10 -y
conda activate adgen
pip install -r requirements.txt
```

### 4. Create `.env` File

Create a `.env` file in the project root with your configuration:

```env
PROJECT_ID=YOUR_PROJECT_ID
LOCATION=us-central1
IMAGE_MODEL_VERSION=imagen-3.0-generate-002
VIDEO_MODEL_VERSION=veo-2.0-generate-001
GOOGLE_API_KEY=YOUR_API_KEY
```

### 5. Run the App

```bash
streamlit run streamlit_app.py
```

The app will open in your default web browser.

---
## 📂 Project Structure

```
.
├── generated_images/
├── generated_videos/
├── llm.py
├── streamlit_app.py
├── requirements.txt
└── .env  # Your config file (not included in repo)
```

---

## 📌 Notes

* Ensure your **Google Cloud Vertex AI APIs** are enabled.
* Image/video generation may take **several minutes** — please be patient.
* The app supports loading **sample data** for demo purposes.

---

## 🧠 Credits

Built with ❤️ using [Streamlit](https://streamlit.io) and [Google Vertex AI](https://cloud.google.com/vertex-ai/docs/generative-ai/overview).

