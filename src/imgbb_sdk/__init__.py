"""
imgbb_sdk - Modern, lightweight Python library for uploading images to ImgBB API
"""

from imgbb_sdk.client import imgbb_upload
from imgbb_sdk.exceptions import (
    ImgBBAPIError,
    ImgBBError,
    ImgBBTimeoutError,
    ImgBBValidationError,
)
from imgbb_sdk.types import (
    ImgBBImageData,
    ImgBBImageInfo,
    ImgBBResponse,
    ImgBBUploadOptions,
)

__version__ = "1.0.0"
__all__ = [
    "imgbb_upload",
    "ImgBBError",
    "ImgBBAPIError",
    "ImgBBValidationError",
    "ImgBBTimeoutError",
    "ImgBBUploadOptions",
    "ImgBBResponse",
    "ImgBBImageData",
    "ImgBBImageInfo",
]
