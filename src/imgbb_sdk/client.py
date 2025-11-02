"""
Main client module for ImgBB SDK
"""

import base64
import os
from io import BytesIO
from pathlib import Path
from typing import BinaryIO, Union
from urllib.parse import urlparse

import requests

from imgbb_sdk.exceptions import (
    ImgBBAPIError,
    ImgBBTimeoutError,
    ImgBBValidationError,
)
from imgbb_sdk.types import ImgBBResponse

# Constants
IMGBB_API_URL = "https://api.imgbb.com/1/upload"
UPLOAD_TIMEOUT = 30  # seconds
MAX_FILE_SIZE = 32 * 1024 * 1024  # 32 MB
MIN_EXPIRATION = 60
MAX_EXPIRATION = 15552000

SUPPORTED_MIME_TYPES = {
    "image/jpeg",
    "image/jpg",
    "image/png",
    "image/gif",
    "image/bmp",
    "image/webp",
}

SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"}


def _validate_api_key(key: str) -> None:
    """Validate the API key."""
    if not key or not isinstance(key, str) or not key.strip():
        raise ImgBBValidationError(
            "ImgBB API key is required and must be a non-empty string"
        )


def _validate_expiration(expiration: int) -> None:
    """Validate the expiration parameter."""
    if not isinstance(expiration, int):
        raise ImgBBValidationError("Expiration must be an integer")
    
    if expiration < MIN_EXPIRATION or expiration > MAX_EXPIRATION:
        raise ImgBBValidationError(
            f"Expiration must be a number between {MIN_EXPIRATION} and {MAX_EXPIRATION} seconds"
        )


def _is_url(path: str) -> bool:
    """Check if the given string is a URL."""
    try:
        result = urlparse(path)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def _get_file_extension(filename: str) -> str:
    """Get the file extension from a filename."""
    return Path(filename).suffix.lower()


def _validate_image_type(image_data: Union[str, bytes, BinaryIO], filename: str = "") -> None:
    """Validate the image type based on filename or content."""
    # If we have a filename, check the extension
    if filename:
        ext = _get_file_extension(filename)
        if ext and ext not in SUPPORTED_EXTENSIONS:
            raise ImgBBValidationError(
                f"Invalid image type. Supported formats: JPEG, PNG, GIF, BMP, WEBP. Got: {ext}"
            )


def _read_image_file(file_path: str) -> bytes:
    """Read an image file from disk."""
    path = Path(file_path)
    
    if not path.exists():
        raise ImgBBValidationError(f"File not found: {file_path}")
    
    if not path.is_file():
        raise ImgBBValidationError(f"Path is not a file: {file_path}")
    
    file_size = path.stat().st_size
    if file_size > MAX_FILE_SIZE:
        raise ImgBBValidationError(
            f"File size ({file_size} bytes) exceeds maximum allowed size ({MAX_FILE_SIZE} bytes)"
        )
    
    _validate_image_type(b"", str(path))
    
    with open(path, "rb") as f:
        return f.read()


def _prepare_image_data(image: Union[str, bytes, BinaryIO]) -> str:
    """Prepare image data for upload (convert to base64)."""
    image_bytes: bytes
    filename = ""
    
    # Handle different input types
    if isinstance(image, str):
        if _is_url(image):
            # It's a URL, return as-is
            return image
        else:
            # It's a file path
            filename = image
            image_bytes = _read_image_file(image)
    elif isinstance(image, bytes):
        # Raw bytes
        image_bytes = image
    elif hasattr(image, "read"):
        # File-like object
        if hasattr(image, "name"):
            filename = str(getattr(image, "name", ""))
        image_bytes = image.read()  # type: ignore
        if hasattr(image, "seek"):
            image.seek(0)  # type: ignore  # Reset file pointer
    else:
        raise ImgBBValidationError(
            "Image must be a file path (str), URL (str), bytes, or file-like object"
        )
    
    # Validate image type
    _validate_image_type(image_bytes, filename)
    
    # Convert to base64
    return base64.b64encode(image_bytes).decode("utf-8")


def imgbb_upload(
    key: str,
    image: Union[str, bytes, BinaryIO],
    name: str = "",
    expiration: int = 0,
) -> ImgBBResponse:
    """Upload an image to ImgBB.
    
    Args:
        key: Your ImgBB API key
        image: The image to upload. Can be:
            - File path (str): "/path/to/image.jpg"
            - Image URL (str): "https://example.com/image.jpg"
            - Raw bytes: b"\\x89PNG..."
            - File-like object: open("image.jpg", "rb")
        name: Optional custom name for the uploaded image
        expiration: Optional auto-deletion time in seconds (60-15552000).
                   Set to 0 or omit for permanent storage.
    
    Returns:
        ImgBBResponse: Response from the ImgBB API containing upload information
    
    Raises:
        ImgBBValidationError: If input validation fails
        ImgBBAPIError: If the API returns an error
        ImgBBTimeoutError: If the upload times out
    
    Example:
        >>> from imgbb_sdk import imgbb_upload
        >>> 
        >>> # Upload from file path
        >>> response = imgbb_upload(
        ...     key="your-api-key",
        ...     image="/path/to/image.jpg",
        ...     name="my-image",
        ...     expiration=3600
        ... )
        >>> print(response["data"]["url"])
        
        >>> # Upload from file object
        >>> with open("image.jpg", "rb") as f:
        ...     response = imgbb_upload(key="your-api-key", image=f)
        
        >>> # Upload from URL
        >>> response = imgbb_upload(
        ...     key="your-api-key",
        ...     image="https://example.com/image.jpg"
        ... )
    """
    # Validate inputs
    _validate_api_key(key)
    
    if expiration and expiration != 0:
        _validate_expiration(expiration)
    
    # Prepare the image data
    try:
        image_data = _prepare_image_data(image)
    except ImgBBValidationError:
        raise
    except Exception as e:
        raise ImgBBValidationError(f"Failed to prepare image data: {str(e)}")
    
    # Prepare the request
    params = {"key": key}
    if expiration and expiration != 0:
        params["expiration"] = str(expiration)
    
    data = {"image": image_data}
    if name:
        data["name"] = name
    
    # Make the API request
    try:
        response = requests.post(
            IMGBB_API_URL,
            params=params,
            data=data,
            timeout=UPLOAD_TIMEOUT,
        )
        
        # Check for HTTP errors
        if response.status_code != 200:
            error_message = f"ImgBB API error: HTTP {response.status_code}"
            try:
                error_data = response.json()
                if "error" in error_data:
                    error_message += f": {error_data['error'].get('message', 'Unknown error')}"
            except Exception:
                error_message += f": {response.text}"
            
            raise ImgBBAPIError(
                error_message,
                status_code=response.status_code,
                response_text=response.text,
            )
        
        # Parse the response
        result = response.json()
        
        # Validate the response structure
        if not result.get("success"):
            raise ImgBBAPIError(
                f"Upload failed: {result.get('error', {}).get('message', 'Unknown error')}",
                status_code=response.status_code,
                response_text=response.text,
            )
        
        return result
        
    except requests.exceptions.Timeout:
        raise ImgBBTimeoutError(f"Upload timed out after {UPLOAD_TIMEOUT} seconds")
    except requests.exceptions.RequestException as e:
        raise ImgBBAPIError(f"Network error: {str(e)}")
    except ImgBBAPIError:
        raise
    except ImgBBTimeoutError:
        raise
    except Exception as e:
        raise ImgBBAPIError(f"Unexpected error during upload: {str(e)}")
