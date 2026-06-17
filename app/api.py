from fastapi import FastAPI, File, HTTPException, UploadFile

from app.llm import LLMAnalysisError, analyze_nutrition_text
from app.ocr import OCRExtractionError, extract_text_from_image
from app.schemas import ScanResponse
from app.utils import save_upload_to_temp, validate_image_upload


app = FastAPI(
    title="NutriScan AI",
    description="OCR + Groq nutrition-label extraction and explainable packaged-food analysis.",
    version="0.1.0",
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/scan", response_model=ScanResponse)
async def scan_label(
    ingredients_image: UploadFile = File(...),
    nutrition_image: UploadFile = File(...),
) -> ScanResponse:
    try:
        validate_image_upload(ingredients_image)
        validate_image_upload(nutrition_image)

        ingredients_path = await save_upload_to_temp(ingredients_image)
        nutrition_path = await save_upload_to_temp(nutrition_image)
        raw_ingredients_text = extract_text_from_image(ingredients_path)
        raw_nutrition_text = extract_text_from_image(nutrition_path)
        raw_ocr_text = (
            "Ingredients label:\n"
            f"{raw_ingredients_text}\n\n"
            "Nutrition chart:\n"
            f"{raw_nutrition_text}"
        )
        if not raw_ingredients_text.strip() and not raw_nutrition_text.strip():
            raise HTTPException(status_code=422, detail="No readable label text found in the uploaded images.")

        analysis = analyze_nutrition_text(raw_ingredients_text, raw_nutrition_text)
        return ScanResponse(
            raw_ingredients_text=raw_ingredients_text,
            raw_nutrition_text=raw_nutrition_text,
            raw_ocr_text=raw_ocr_text,
            analysis=analysis,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except OCRExtractionError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except LLMAnalysisError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
