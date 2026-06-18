---
title: NutriScan
emoji: 🔥
colorFrom: green
colorTo: gray
sdk: docker
pinned: false
---

# NutriScan AI

NutriScan AI analyzes packaged food labels from images and provides structured nutritional insights, health scores, and consumption recommendations.

## Features

- Extracts text and tables from ingredient labels and nutrition charts
- Identifies macro and micro nutrients
- Generates an explainable health score
- Highlights positive and negative aspects
- Detects concerning ingredients
- Provides consumption guidance and healthier alternatives
- FastAPI backend with Streamlit interface

## Tech Stack

| Component | Technology |
|------------|------------|
| Language | Python |
| Backend | FastAPI |
| Frontend | Streamlit |
| OCR & Document Processing | Docling |
| LLM Inference | Groq API |
| Data Validation | Pydantic |

## Project Structure

```text
NutriScan-AI
│
├── app
│   ├── __init__.py
│   ├── api.py
│   ├── config.py
│   ├── llm.py
│   ├── ocr.py
│   ├── prompts.py
│   ├── schemas.py
│   └── utils.py
│
├── streamlit_app.py
├── requirements.txt
├── Dockerfile
├── .gitignore
└── README.md
```

## Installation

Clone the repository:

```bash
git clone https://github.com/tanishq-2004/NutriScan-AI.git
cd NutriScan-AI
```

Create a virtual environment:

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### Linux / macOS

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_api_key
GROQ_MODEL=llama-3.3-70b-versatile
```

## Running the Streamlit App

```bash
streamlit run streamlit_app.py
```

Open:

```
http://localhost:8501
```

## Running the API

```bash
uvicorn app.api:app --reload
```

API documentation:

```
http://127.0.0.1:8000/docs
```

## Workflow

1. Upload ingredient label and nutrition chart images.
2. Images are preprocessed for improved OCR accuracy.
3. Text and tables are extracted from the images.
4. Nutritional information is analyzed.
5. Health scores and recommendations are generated.
6. Structured results are displayed.

## Future Improvements

- Batch scanning
- Barcode-based product lookup
- Product comparison
- Nutrition history tracking
- Product database integration

## Author

**Tanishq Gupta**

- GitHub: https://github.com/tanishq-2004
- LinkedIn: https://www.linkedin.com/in/tanishq-gupta-w/

## License

This project is licensed under the MIT License.