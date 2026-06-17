from pathlib import Path
from tempfile import NamedTemporaryFile

from fastapi import UploadFile


ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp", "image/bmp"}


def validate_image_upload(upload: UploadFile) -> None:
    if upload.content_type not in ALLOWED_IMAGE_TYPES:
        allowed = ", ".join(sorted(ALLOWED_IMAGE_TYPES))
        raise ValueError(f"Unsupported file type. Please upload one of: {allowed}")


async def save_upload_to_temp(upload: UploadFile) -> Path:
    suffix = Path(upload.filename or "label.jpg").suffix or ".jpg"
    with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(await upload.read())
        return Path(tmp.name)
