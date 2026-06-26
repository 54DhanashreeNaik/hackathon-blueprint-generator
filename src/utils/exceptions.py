class FileProcessingError(Exception):
    """Base exception class for all file processing related errors."""
    pass

class UnsupportedFileTypeError(FileProcessingError):
    """Raised when the uploaded file type is not supported."""
    pass

class ExtractionError(FileProcessingError):
    """Raised when text/metadata extraction fails from a supported file."""
    pass
