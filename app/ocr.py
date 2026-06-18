from functools import lru_cache
from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter, ImageOps


class OCRExtractionError(RuntimeError):
    """Raised when Docling cannot extract text from an uploaded label image."""


@lru_cache(maxsize=1)
def get_docling_converter():
    try:
        from docling.document_converter import DocumentConverter
    except ImportError as exc:
        raise OCRExtractionError(
            "Docling is not installed. Run `pip install -r requirements.txt`."
        ) from exc

    print("Initializing Docling converter...")
    return DocumentConverter()


def preprocess_image(image_path: str | Path) -> Path:
    image_path = Path(image_path)

    image = Image.open(image_path)

    # Fix image orientation
    image = ImageOps.exif_transpose(image)

    # Convert to RGB
    image = image.convert("RGB")

    # Resize large images while preserving aspect ratio
    image.thumbnail((1600, 1600))

    # Slightly improve contrast
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(1.2)

    # Slight sharpening
    image = image.filter(ImageFilter.SHARPEN)

    image.save(image_path, quality=95)

    return image_path


def extract_text_from_image(image_path: str | Path) -> str:
    try:
        image_path = preprocess_image(image_path)

        converter = get_docling_converter()

        conversion = converter.convert(str(image_path))
        document = conversion.document

        parts = []

        # Preserve nutrition tables
        for index, table in enumerate(document.tables, start=1):
            try:
                table_df = table.export_to_dataframe(doc=document)
                parts.append(
                    f"## Table {index}\n{table_df.to_markdown(index=False)}"
                )
            except Exception:
                continue

        # Full extracted markdown
        markdown = document.export_to_markdown().strip()

        if markdown:
            parts.append(
                "## Full extracted text\n" + markdown
            )

        extracted = "\n\n".join(parts).strip()

        if not extracted:
            raise OCRExtractionError(
                "Docling could not extract readable text from this image."
            )

        return extracted

    except Exception as exc:
        raise OCRExtractionError(
            f"Failed to extract text from image: {exc}"
        ) from exc