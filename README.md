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

## API Endpoint

### POST `/scan`

Accepts:

- `ingredients_image`
- `nutrition_image`

Returns:

- OCR extracted text
- Ingredients
- Macro nutrients
- Micro nutrients
- Health score
- Positive aspects
- Negative aspects
- Concerning ingredients
- Consumption guidance
- Healthier alternatives
- Balanced diet recommendations

## Workflow

1. Upload ingredient label image.
2. Upload nutrition chart image.
3. Extract text and tables from the images.
4. Analyze nutritional information.
5. Generate health scores and recommendations.
6. Display structured results.

## Future Improvements

- Batch scanning
- Image preprocessing
- Barcode-based product lookup
- Product comparison
- Nutrition history tracking

## Author

**Tanishq Gupta**

- GitHub: https://github.com/tanishq-2004
- LinkedIn: https://www.linkedin.com/in/tanishq-gupta-w/

## License

This project is licensed under the MIT License.