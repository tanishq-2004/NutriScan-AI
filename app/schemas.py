from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


ConsumptionFrequency = Literal["Daily", "Occasionally"]


class NutrientItem(BaseModel):
    name: str
    amount: str | None = None
    unit: str | None = None
    daily_value_percent: str | None = None
    notes: str | None = None


class MacroNutrients(BaseModel):
    energy: NutrientItem | None = None
    protein: NutrientItem | None = None
    carbohydrates: NutrientItem | None = None
    total_sugar: NutrientItem | None = None
    added_sugar: NutrientItem | None = None
    total_fat: NutrientItem | None = None
    saturated_fat: NutrientItem | None = None
    trans_fat: NutrientItem | None = None
    fiber: NutrientItem | None = None
    sodium: NutrientItem | None = None
    serving_size: str | None = None


class NutriScanAnalysis(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ingredients: list[str] = Field(default_factory=list)
    macro_nutrients: MacroNutrients = Field(default_factory=MacroNutrients)
    micro_nutrients: list[NutrientItem] = Field(default_factory=list)
    health_score: int = Field(ge=1, le=10)
    score_breakdown: dict[str, str] = Field(default_factory=dict)
    positive_aspects: list[str] = Field(default_factory=list)
    negative_aspects: list[str] = Field(default_factory=list)
    concerning_ingredients: list[str] = Field(default_factory=list)
    consumption_frequency: ConsumptionFrequency
    recommended_consuming_weight: str | None = None
    healthier_alternatives: list[str] = Field(default_factory=list)
    balanced_diet_tips: list[str] = Field(default_factory=list)
    summary: str


class ScanResponse(BaseModel):
    raw_ingredients_text: str
    raw_nutrition_text: str
    raw_ocr_text: str
    analysis: NutriScanAnalysis
