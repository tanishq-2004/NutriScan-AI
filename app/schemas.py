from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


ConsumptionFrequency = Literal["Daily", "Occasionally"]


class NutrientItem(BaseModel):
    name: str
    amount: str | None = None
    unit: str | None = None
    daily_value_percent: str | None = None
    # Examples:
    # "Per 100 g"
    # "Per serving (50 g)"
    # "Per 100 ml"
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


class ConcerningIngredient(BaseModel):
    ingredient: str
    reason: str
    severity: Literal["Low", "Moderate", "High"]


class BeneficialIngredient(BaseModel):
    ingredient: str
    benefit: str


class ScoreComponent(BaseModel):
    factor: str
    impact: str
    explanation: str


class NutriScanAnalysis(BaseModel):
    model_config = ConfigDict(extra="forbid")

    # Ingredient section
    ingredients: list[str] = Field(default_factory=list)

    # Nutrition section
    macro_nutrients: MacroNutrients = Field(default_factory=MacroNutrients)
    micro_nutrients: list[NutrientItem] = Field(default_factory=list)

    # Overall score
    health_score: int = Field(ge=1, le=10)
    score_breakdown: list[ScoreComponent] = Field(default_factory=list)

    # Positives and negatives
    positive_aspects: list[str] = Field(default_factory=list)
    negative_aspects: list[str] = Field(default_factory=list)

    # Ingredients requiring attention
    concerning_ingredients: list[ConcerningIngredient] = Field(default_factory=list)

    # Beneficial ingredients
    beneficial_ingredients: list[BeneficialIngredient] = Field(default_factory=list)

    # Consumption guidance
    consumption_frequency: ConsumptionFrequency
    recommended_consuming_weight: str | None = None

    # Recommendations
    healthier_alternatives: list[str] = Field(default_factory=list)
    balanced_diet_tips: list[str] = Field(default_factory=list)

    # Short verdict
    summary: str


class ScanResponse(BaseModel):
    raw_ingredients_text: str
    raw_nutrition_text: str
    raw_ocr_text: str
    analysis: NutriScanAnalysis