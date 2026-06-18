from functools import lru_cache
from pathlib import Path


class OCRExtractionError(RuntimeError):
    """Raised when Docling cannot extract text from an uploaded label image."""


@lru_cache
def get_docling_converter():
    try:
        from docling.document_converter import DocumentConverter
    except ImportError as exc:
        raise OCRExtractionError(
            "Docling is not installed. Run `python -m pip install -r requirements.txt`."
        ) from exc

    return DocumentConverter()


def extract_text_from_image(image_path: str | Path) -> str:
    converter = get_docling_converter()
    conversion = converter.convert(str(image_path))
    document = conversion.document
    parts: list[str] = []

    for index, table in enumerate(document.tables, start=1):
        table_df = table.export_to_dataframe(doc=document)
        parts.append(f"## Table {index}\n{table_df.to_markdown(index=False)}")

    markdown = document.export_to_markdown().strip()
    if markdown:
        parts.append("## Full extracted text\n" + markdown)

    extracted = "\n\n".join(parts).strip()
    if not extracted:
        raise OCRExtractionError("Docling could not extract readable text from this image.")

    return extracted