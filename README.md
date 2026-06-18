# NutriScan AI

NutriScan AI analyzes packaged food labels from images and provides structured nutritional insights, health scores, and consumption recommendations.

## Live Demo

🚀 https://huggingface.co/spaces/Skywalker67/NutriScan-AI

## Features

- Extracts text and tables from ingredient labels and nutrition charts
- Identifies macro and micro nutrients
- Generates an explainable health score
- Highlights positive and negative aspects
- Detects concerning ingredients with severity and reasons
- Identifies beneficial ingredients
- Provides consumption guidance and healthier alternatives
- Generates balanced diet recommendations
- FastAPI backend with Streamlit interface

## Screenshots

### Home Page

![Home Page](https://raw.githubusercontent.com/tanishq-2004/NutriScan-AI/main/assets/home_page.png)

### Upload Images

![Upload Images](https://raw.githubusercontent.com/tanishq-2004/NutriScan-AI/main/assets/upload_images.jpg)

### Analysis Result (Part 1)

![Analysis Result 1](https://raw.githubusercontent.com/tanishq-2004/NutriScan-AI/main/assets/analysis_result1.png)

### Analysis Result (Part 2)

![Analysis Result 2](https://raw.githubusercontent.com/tanishq-2004/NutriScan-AI/main/assets/analysis_result2.png)

### Analysis Result (Part 3)

![Analysis Result 3](https://raw.githubusercontent.com/tanishq-2004/NutriScan-AI/main/assets/analysis_result3.png)

## Tech Stack

| Component | Technology |
|------------|------------|
| Language | Python |
| Backend | FastAPI |
| Frontend | Streamlit |
| OCR & Document Processing | Docling |
| LLM Inference | Groq API |
| Data Validation | Pydantic |
| Deployment | Hugging Face Spaces (Docker) |

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

```text
http://localhost:8501
```

## Running the API

```bash
uvicorn app.api:app --reload
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

## Workflow

1. Upload ingredient-list and nutrition-chart images.
2. Images are processed using Docling.
3. Text and nutrition tables are extracted.
4. Groq analyzes ingredients and nutritional information.
5. Macro and micro nutrients are identified.
6. Health score and score breakdown are generated.
7. Concerning and beneficial ingredients are highlighted.
8. Healthier alternatives and balanced diet tips are provided.

## Deployment

The application is deployed on Hugging Face Spaces using Docker.

**Live Demo**

https://huggingface.co/spaces/Skywalker67/NutriScan-AI

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