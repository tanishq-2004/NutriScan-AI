from pathlib import Path
from tempfile import NamedTemporaryFile

import streamlit as st
from PIL import Image

from app.llm import LLMAnalysisError, analyze_nutrition_text
from app.ocr import OCRExtractionError, extract_text_from_image


st.set_page_config(page_title="NutriScan AI", layout="wide")


def save_streamlit_upload(uploaded_file) -> Path:
    suffix = Path(uploaded_file.name).suffix or ".jpg"
    with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(uploaded_file.getbuffer())
        return Path(tmp.name)


def render_list(title: str, items: list[str]) -> None:
    st.subheader(title)
    if not items:
        st.caption("No clear items detected.")
        return
    for item in items:
        st.write(f"- {item}")


def nutrient_to_row(label: str, nutrient) -> dict[str, str] | None:
    if nutrient is None:
        return None

    return {
        "Nutrient": label,
        "Amount": nutrient.amount or "-",
        "Unit": nutrient.unit or "-",
        "% Daily Value": nutrient.daily_value_percent or "-",
        "Notes": nutrient.notes or "-",
    }


def render_macro_table(macros) -> None:
    rows = []

    labels = {
        "energy": "Energy",
        "protein": "Protein",
        "carbohydrates": "Carbohydrates",
        "total_sugar": "Total Sugar",
        "added_sugar": "Added Sugar",
        "total_fat": "Total Fat",
        "saturated_fat": "Saturated Fat",
        "trans_fat": "Trans Fat",
        "fiber": "Fiber",
        "sodium": "Sodium",
    }

    for field_name, label in labels.items():
        row = nutrient_to_row(label, getattr(macros, field_name))
        if row:
            rows.append(row)

    if macros.serving_size:
        st.write(f"Serving size detected: **{macros.serving_size}**")

    if rows:
        st.dataframe(rows, use_container_width=True, hide_index=True)
    else:
        st.caption("No clear macro nutrients detected.")


def render_micro_table(micros) -> None:
    rows = [nutrient_to_row(item.name, item) for item in micros]
    rows = [row for row in rows if row]

    if rows:
        st.dataframe(rows, use_container_width=True, hide_index=True)
    else:
        st.caption("No clear vitamins or minerals detected.")


def render_score_breakdown(score_breakdown) -> None:
    if not score_breakdown:
        st.caption("No score breakdown returned.")
        return

    rows = [
        {
            "Factor": item.factor,
            "Impact": item.impact,
            "Explanation": item.explanation,
        }
        for item in score_breakdown
    ]

    st.dataframe(rows, use_container_width=True, hide_index=True)


def render_concerning_ingredients(items) -> None:
    st.subheader("Ingredients Requiring Attention")

    if not items:
        st.caption("No major concerns detected.")
        return

    rows = [
        {
            "Ingredient": item.ingredient,
            "Severity": item.severity,
            "Reason": item.reason,
        }
        for item in items
    ]

    st.dataframe(rows, use_container_width=True, hide_index=True)


def render_beneficial_ingredients(items) -> None:
    st.subheader("Beneficial Ingredients")

    if not items:
        st.caption("No beneficial ingredients identified.")
        return

    rows = [
        {
            "Ingredient": item.ingredient,
            "Benefit": item.benefit,
        }
        for item in items
    ]

    st.dataframe(rows, use_container_width=True, hide_index=True)


def render_analysis(analysis) -> None:
    st.metric("Health Score", f"{analysis.health_score}/10")
    st.info(analysis.summary)

    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader("Score Breakdown")
        render_score_breakdown(analysis.score_breakdown)
        render_list("Positive Aspects", analysis.positive_aspects)

    with col_b:
        st.subheader("Consumption")
        st.write(f"Frequency: **{analysis.consumption_frequency}**")

        if analysis.recommended_consuming_weight:
            st.write(
                f"Recommended amount: **{analysis.recommended_consuming_weight}**"
            )

        render_list("Negative Aspects", analysis.negative_aspects)

    tab_macros, tab_micros, tab_ingredients, tab_tips = st.tabs(
        ["Macros", "Micros", "Ingredients", "Tips"]
    )

    with tab_macros:
        render_macro_table(analysis.macro_nutrients)

    with tab_micros:
        render_micro_table(analysis.micro_nutrients)

    with tab_ingredients:
        render_list("Ingredients", analysis.ingredients)
        render_concerning_ingredients(analysis.concerning_ingredients)
        render_beneficial_ingredients(analysis.beneficial_ingredients)

    with tab_tips:
        render_list(
            "Healthier Alternatives",
            analysis.healthier_alternatives,
        )

        render_list(
            "Balanced Diet Tips",
            analysis.balanced_diet_tips,
        )


st.title("NutriScan AI")

st.caption(
    "Upload ingredient-list and nutrition-chart images. "
    "Docling extracts structured text and tables before Groq analyzes the food."
)

ingredients_file = st.file_uploader(
    "Ingredient list image",
    type=["jpg", "jpeg", "png", "webp", "bmp"],
    key="ingredients_image",
)

nutrition_file = st.file_uploader(
    "Nutrition chart image",
    type=["jpg", "jpeg", "png", "webp", "bmp"],
    key="nutrition_image",
)

if ingredients_file or nutrition_file:

    preview_left, preview_right = st.columns(2)

    with preview_left:
        if ingredients_file:
            st.image(
                Image.open(ingredients_file),
                caption="Ingredient list",
                use_container_width=True,
            )
        else:
            st.info("Upload the ingredient-list image.")

    with preview_right:
        if nutrition_file:
            st.image(
                Image.open(nutrition_file),
                caption="Nutrition chart",
                use_container_width=True,
            )
        else:
            st.info("Upload the nutrition-chart image.")

    can_scan = ingredients_file is not None and nutrition_file is not None

    if st.button(
        "Scan labels",
        type="primary",
        use_container_width=True,
        disabled=not can_scan,
    ):

        ingredients_path = save_streamlit_upload(ingredients_file)
        nutrition_path = save_streamlit_upload(nutrition_file)

        with st.status("Scanning label...", expanded=True) as status:

            try:
                st.write("Extracting ingredient text with Docling")
                raw_ingredients_text = extract_text_from_image(ingredients_path)

                st.write("Extracting nutrition-chart table with Docling")
                raw_nutrition_text = extract_text_from_image(nutrition_path)

                st.write("Analyzing nutrition profile with Groq")
                analysis = analyze_nutrition_text(
                    raw_ingredients_text,
                    raw_nutrition_text,
                )

            except OCRExtractionError as exc:
                status.update(label="OCR failed", state="error")
                st.error(str(exc))
                st.stop()

            except LLMAnalysisError as exc:
                status.update(label="Analysis failed", state="error")
                st.error(str(exc))
                st.stop()

            status.update(label="Analysis complete", state="complete")

        raw_left, raw_right = st.columns(2)

        with raw_left:
            st.subheader("Ingredient OCR Text")

            st.text_area(
                "Ingredient OCR output",
                raw_ingredients_text,
                height=260,
                label_visibility="collapsed",
            )

        with raw_right:
            st.subheader("Nutrition OCR Text")

            st.text_area(
                "Nutrition OCR output",
                raw_nutrition_text,
                height=260,
                label_visibility="collapsed",
            )

        render_analysis(analysis)

else:
    st.write("Choose both images to begin.")