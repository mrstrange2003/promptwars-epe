# CivicSmart EPE Assistant 🗳️

**CivicSmart** is a highly lightweight, interactive Election Process Education (EPE) assistant crafted specifically for the Indian democratic context. It combines an automated dynamic visualizer with a modern AI guide to help users seamlessly understand the intricacies of voting, timelines, and guidelines like the Model Code of Conduct.

Specifically built to remain under a 2MB repository size restriction, it natively limits framework bloat by pairing a lean Python FastAPI backend directly to a CDN-rendered Vanilla JS frontend.

### ✨ Key Features
- **Split-Screen Dynamic Layout**: A responsive visualizer that natively tracks the conversational context of the AI and actively highlights standard Indian election phases (from Voter Registration to EVM Polling and Results).
- **AI-Powered Guide**: Powered by Google's highly scalable `gemini-2.5-flash-lite` model natively running through the `google-genai` SDK. The AI is specifically trained via system prompts to act as a deeply unbiased mentor focused on the Election Commission of India (ECI) framework.
- **Glassmorphism Aesthetic**: Built entirely with Vanilla Tailwind CSS utility classes and modern web aesthetics. Zero external image assets or heavy SVG bundles needed.
- **Cloud Run Ready**: Packaged natively with a multi-stage `Dockerfile` optimizing build size down. 

### 🚀 Tech Stack
- **Backend**: Python 3.11+ / FastAPI / Uvicorn
- **Frontend**: Vanilla HTML5, JavaScript, Tailwind CSS (via CDN)
- **AI Integration**: Google GenAI SDK (`google-genai`)

---

### ⚙️ Local Setup Guide

1. **Clone the repository:**
   ```bash
   git clone https://github.com/mrstrange2003/promptwars-epe.git
   cd promptwars-epe
   ```

2. **Set up a Virtual Environment & Install Dependencies:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: .\venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables:**
   You must export your Google GenAI key so the backend can authenticate your LLM requests.
   ```bash
   export GOOGLE_API_KEY="your-api-key-here"
   # On Windows PowerShell use: $env:GOOGLE_API_KEY="your-api-key-here"
   ```

4. **Run the Application:**
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8080 --reload
   ```
   *Navigate your browser to `http://localhost:8080` to access the interface!*

---

### 🐳 Docker & Google Cloud Run

To containerize or deploy directly to Google Cloud Run, leverage the provided efficient `Dockerfile`! 

**Build Locally:**
```bash
docker build -t civicsmart-app .
docker run -p 8080:8080 -e GOOGLE_API_KEY="your-api-key-here" civicsmart-app
```
