import io
import logging
import time
from datetime import datetime
from pathlib import Path
from typing import Union, Dict, Any, BinaryIO, Optional

import fitz  # PyMuPDF
import docx
from pydantic import BaseModel, Field

from src.utils.exceptions import UnsupportedFileTypeError, ExtractionError

# Configure logger
logger = logging.getLogger(__name__)

class ProcessedFileResult(BaseModel):
    """
    Official contract representing the unified, structured output of the
    File Processing layer. All downstream AI agents consume this model.
    """
    file_name: str
    file_type: str  # "pdf", "docx", "txt", "png", "jpg", "jpeg"
    pages: int
    raw_text: str
    clean_text: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    # Expected metadata keys:
    # - extension: str
    # - file_size_kb: float
    # - extraction_method: str
    # - processing_time_ms: float
    # - timestamp: datetime
    # - warnings: list[str]


class FileProcessingService:
    """
    Service responsible for converting various uploaded file types into a
    unified ProcessedFileResult object.
    """

    SUPPORTED_EXTENSIONS = {
        ".pdf": "pdf",
        ".docx": "docx",
        ".txt": "txt",
        ".png": "png",
        ".jpg": "jpg",
        ".jpeg": "jpeg"
    }

    def process_file(self, file_source: Union[Path, str, bytes, BinaryIO, Any], file_name: Optional[str] = None) -> ProcessedFileResult:
        """
        Processes the input file source, performs text extraction/processing,
        and returns a standardized ProcessedFileResult.

        Args:
            file_source: A file path, raw bytes, file-like stream, or Streamlit UploadedFile.
            file_name: Optional original file name (highly recommended if passing bytes or stream).

        Returns:
            ProcessedFileResult: Standardized extracted file data.

        Raises:
            UnsupportedFileTypeError: If the file type is unsupported or cannot be detected.
            ExtractionError: If extraction fails due to file corruption or other processing errors.
        """
        start_time = time.perf_counter()
        logger.info("Received file for processing.")

        # 1. Normalize input to bytes, name, and size
        content_bytes, resolved_name, size_kb = self._normalize_input(file_source, file_name)
        
        # 2. Detect file type
        file_type, extension = self._detect_file_type(resolved_name)
        logger.info(f"Detected file type: {file_type} for file: {resolved_name}")

        warnings = []
        raw_text = ""
        pages = 1
        extraction_method = "plain_text"

        try:
            # 3. Dispatch extraction based on type
            if file_type == "pdf":
                extraction_method = "pymupdf"
                raw_text, pages = self._extract_pdf(content_bytes)
            elif file_type == "docx":
                extraction_method = "python-docx"
                raw_text, pages = self._extract_docx(content_bytes)
            elif file_type == "txt":
                extraction_method = "utf-8-reader"
                raw_text, pages = self._extract_txt(content_bytes)
            elif file_type in ["png", "jpg", "jpeg"]:
                extraction_method = "gemini-vision-placeholder"
                # This will raise NotImplementedError as required
                raw_text, pages = self._extract_image(content_bytes)
            else:
                raise UnsupportedFileTypeError(f"Unsupported file type: {file_type}")
        except NotImplementedError as e:
            logger.warning(f"Image processing not implemented: {str(e)}")
            raise e
        except Exception as e:
            logger.error(f"Error during file extraction: {str(e)}")
            raise ExtractionError(f"Failed to extract content from {resolved_name}: {str(e)}") from e

        # 4. Clean extracted text
        clean_text = self._clean_text(raw_text)

        processing_time_ms = (time.perf_counter() - start_time) * 1000
        logger.info(f"Extraction completed in {processing_time_ms:.2f} ms")

        # 5. Build processed result
        metadata = {
            "extension": extension,
            "file_size_kb": round(size_kb, 2),
            "extraction_method": extraction_method,
            "processing_time_ms": round(processing_time_ms, 2),
            "timestamp": datetime.now(),
            "warnings": warnings
        }

        return self._build_processed_result(resolved_name, file_type, pages, raw_text, clean_text, metadata)

    def _normalize_input(self, file_source: Union[Path, str, bytes, BinaryIO, Any], file_name: Optional[str] = None) -> tuple[bytes, str, float]:
        """
        Normalizes the incoming file source into raw bytes, file name, and file size in KB.
        """
        # Case 1: File Path (Path or str)
        if isinstance(file_source, (Path, str)):
            path = Path(file_source)
            if not path.exists():
                raise FileNotFoundError(f"File not found at: {path}")
            resolved_name = file_name or path.name
            try:
                content_bytes = path.read_bytes()
            except Exception as e:
                raise ExtractionError(f"Could not read file from path {path}: {str(e)}") from e
            size_kb = len(content_bytes) / 1024.0
            return content_bytes, resolved_name, size_kb

        # Case 2: Raw bytes
        if isinstance(file_source, bytes):
            resolved_name = file_name or "unknown_file"
            size_kb = len(file_source) / 1024.0
            return file_source, resolved_name, size_kb

        # Case 3: Streamlit UploadedFile or file-like object (BinaryIO)
        if hasattr(file_source, "read"):
            resolved_name = file_name or getattr(file_source, "name", "unknown_file")
            # For Streamlit UploadedFile, we can also check the size attribute if available
            size_bytes = getattr(file_source, "size", None)
            
            try:
                # If seekable, remember position and read
                if hasattr(file_source, "seek"):
                    file_source.seek(0)
                content_bytes = file_source.read()
                # If we need to restore seek position
                if hasattr(file_source, "seek"):
                    file_source.seek(0)
            except Exception as e:
                raise ExtractionError(f"Could not read from file-like stream: {str(e)}") from e
            
            size_kb = (size_bytes if size_bytes is not None else len(content_bytes)) / 1024.0
            return content_bytes, resolved_name, size_kb

        raise UnsupportedFileTypeError(f"Unsupported file source type: {type(file_source)}")

    def _detect_file_type(self, file_name: str) -> tuple[str, str]:
        """
        Detects the file type/format based on the file name extension.
        """
        suffix = Path(file_name).suffix.lower()
        if not suffix or suffix not in self.SUPPORTED_EXTENSIONS:
            raise UnsupportedFileTypeError(f"Extension '{suffix}' is not supported.")
        return self.SUPPORTED_EXTENSIONS[suffix], suffix

    def _extract_pdf(self, content: bytes) -> tuple[str, int]:
        """
        Extracts text from PDF bytes using PyMuPDF.
        """
        text_parts = []
        try:
            with fitz.open(stream=content, filetype="pdf") as doc:
                pages_count = len(doc)
                for page_num in range(pages_count):
                    page = doc.load_page(page_num)
                    text_parts.append(page.get_text())
            raw_text = "\n".join(text_parts)
            return raw_text, pages_count
        except Exception as e:
            raise ExtractionError(f"Error parsing PDF: {str(e)}") from e

    def _extract_docx(self, content: bytes) -> tuple[str, int]:
        """
        Extracts paragraphs text from DOCX bytes using python-docx.
        """
        try:
            doc_file = io.BytesIO(content)
            doc = docx.Document(doc_file)
            paragraphs = [p.text for p in doc.paragraphs]
            raw_text = "\n".join(paragraphs)
            return raw_text, 1
        except Exception as e:
            raise ExtractionError(f"Error parsing DOCX: {str(e)}") from e

    def _extract_txt(self, content: bytes) -> tuple[str, int]:
        """
        Reads plain text UTF-8 content from bytes.
        """
        try:
            raw_text = content.decode("utf-8")
            return raw_text, 1
        except UnicodeDecodeError as e:
            # Fallback to general encoding detection or raise exception
            try:
                raw_text = content.decode("latin-1")
                return raw_text, 1
            except Exception as ex:
                raise ExtractionError(f"Failed to decode text file as UTF-8 or Latin-1: {str(ex)}") from e

    def _extract_image(self, content: bytes) -> tuple[str, int]:
        """
        Placeholder for image extraction. Will be implemented using Gemini Vision in Milestone 4.
        """
        raise NotImplementedError(
            "Image processing will be implemented using Gemini Vision in Milestone 4."
        )

    def _clean_text(self, raw_text: str) -> str:
        """
        Trims whitespace and collapses consecutive blank lines into a single blank line.
        """
        if not raw_text:
            return ""
        
        lines = [line.strip() for line in raw_text.splitlines()]
        cleaned_lines = []
        prev_was_empty = False
        
        for line in lines:
            if line == "":
                if not prev_was_empty:
                    cleaned_lines.append("")
                    prev_was_empty = True
            else:
                cleaned_lines.append(line)
                prev_was_empty = False
                
        return "\n".join(cleaned_lines).strip()

    def _build_processed_result(self, file_name: str, file_type: str, pages: int, raw_text: str, clean_text: str, metadata: Dict[str, Any]) -> ProcessedFileResult:
        """
        Constructs and returns the final ProcessedFileResult Pydantic model.
        """
        return ProcessedFileResult(
            file_name=file_name,
            file_type=file_type,
            pages=pages,
            raw_text=raw_text,
            clean_text=clean_text,
            metadata=metadata
        )
