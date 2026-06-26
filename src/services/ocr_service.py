from pathlib import Path

class OCRService:
    """Wrapper class for OCR and Document text parsing."""

    def extract_text_from_file(self, file_path: Path) -> str:
        """Parses txt, docx, pdf, or images to extract text contents."""
        suffix = file_path.suffix.lower()
        if suffix == ".txt":
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        else:
            return f"[Placeholder: Extracted plain text content from file: {file_path.name}]"
