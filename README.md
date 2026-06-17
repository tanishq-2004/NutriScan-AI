---
title: NutriScan
emoji: 🔥
colorFrom: green
colorTo: gray
sdk: docker
pinned: false
---

# NutriScan AI

Resume-worthy hackathon project that scans packaged food nutrition labels and ingredient lists, extracts structured text and tables with Docling, and asks a Groq-hosted LLM to return strict structured JSON with explainable nutrition analysis.

## Features

- Upload separate ingredient-list and nutrition-chart images through Streamlit.
- Extract structured text and nutrition tables from both images with Docling.
- Use one LLM call for both extraction and reasoning.
- Return strict JSON with nutrients, ingredients, health score, breakdown, consumption frequency, recommended consuming weight, recommendations, and diet tips.
- Optional FastAPI backend for API-first demos.

## Tech Stack

- Python
- FastAPI
- Streamlit
- Docling
- Groq API

## Project Structure

```text
nutriscan-ai/
  app/
    api.py              # FastAPI endpoints
    config.py           # Environment-based settings
    llm.py              # Groq JSON analysis client
    ocr.py              # Docling image/table extraction
    prompts.py          # LLM prompt for extraction + analysis
    schemas.py          # Pydantic response models
    utils.py            # Image/file helpers
  streamlit_app.py      # Streamlit UI
  requirements.txt
  .env.example
```

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

Add your Groq API key to `.env`:

```text
GROQ_API_KEY=your_groq_api_key_here
```

## Run Streamlit

```bash
streamlit run streamlit_app.py
```

## Run FastAPI

```bash
uvicorn app.api:app --reload
```

Then open:

```text
http://127.0.0.1:8000/docs
```

## Notes

NutriScan AI is educational and should not replace medical advice. Nutrition-label formats vary widely, so the app preserves extracted text from both uploads and lets the LLM perform robust extraction and reasoning without regex-heavy parsing or hardcoded ingredient lists. Product names are intentionally excluded because they are not required for nutrition analysis.

Both ingredients and nutrition charts are extracted with Docling. This keeps table structure available for nutrition charts instead of flattening rows and columns into noisy OCR text.
