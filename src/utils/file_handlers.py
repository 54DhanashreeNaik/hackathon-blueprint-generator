import shutil
from pathlib import Path
from typing import Optional
from config.settings import UPLOAD_DIR

SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".txt", ".png", ".jpg", ".jpeg"}

def format_file_size(size_bytes: int) -> str:
    """Formats file size into human-readable format."""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.2f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.2f} MB"

def is_supported_file(filename: str) -> bool:
    """Checks if a file extension is supported."""
    suffix = Path(filename).suffix.lower()
    return suffix in SUPPORTED_EXTENSIONS

def save_uploaded_file(file_bytes: bytes, filename: str) -> Optional[Path]:
    """Saves uploaded file bytes to the configure upload folder."""
    if not is_supported_file(filename):
        return None
        
    destination = UPLOAD_DIR / filename
    with open(destination, "wb") as f:
        f.write(file_bytes)
        
    return destination
