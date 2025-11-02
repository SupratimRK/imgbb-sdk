"""
Custom exceptions for ImgBB SDK
"""


class ImgBBError(Exception):
    """Base exception for all ImgBB SDK errors."""
    pass


class ImgBBValidationError(ImgBBError):
    """Raised when input validation fails."""
    pass


class ImgBBAPIError(ImgBBError):
    """Raised when the ImgBB API returns an error."""
    
    def __init__(self, message: str, status_code: int = 0, response_text: str = ""):
        super().__init__(message)
        self.status_code = status_code
        self.response_text = response_text


class ImgBBTimeoutError(ImgBBError):
    """Raised when the upload request times out."""
    pass
