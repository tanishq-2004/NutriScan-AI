import json

from groq import Groq
from pydantic import ValidationError

from app.config import get_settings
from app.prompts import ANALYSIS_SYSTEM_PROMPT, analysis_user_prompt
from app.schemas import NutriScanAnalysis


class LLMAnalysisError(RuntimeError):
    """Raised when the LLM response cannot be parsed or validated."""


def _extract_json(content: str) -> dict:
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        start = content.find("{")
        end = content.rfind("}")
        if start == -1 or end == -1 or end <= start:
            raise LLMAnalysisError("Groq response did not contain JSON.") from None
        try:
            return json.loads(content[start : end + 1])
        except json.JSONDecodeError as exc:
            raise LLMAnalysisError(f"Groq response contained invalid JSON: {exc}") from exc


def analyze_nutrition_text(raw_ingredients_text: str, raw_nutrition_text: str) -> NutriScanAnalysis:
    settings = get_settings()
    if not settings.groq_api_key:
        raise LLMAnalysisError("Missing GROQ_API_KEY. Add it to your .env file.")

    client = Groq(api_key=settings.groq_api_key)
    completion = client.chat.completions.create(
        model=settings.groq_model,
        messages=[
            {"role": "system", "content": ANALYSIS_SYSTEM_PROMPT},
            {"role": "user", "content": analysis_user_prompt(raw_ingredients_text, raw_nutrition_text)},
        ],
        temperature=0.1,
        response_format={"type": "json_object"},
    )

    content = completion.choices[0].message.content or "{}"
    parsed = _extract_json(content)
    try:
        return NutriScanAnalysis.model_validate(parsed)
    except ValidationError as exc:
        raise LLMAnalysisError(f"Groq JSON did not match the expected schema: {exc}") from exc
