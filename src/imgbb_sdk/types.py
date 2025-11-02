"""
Type definitions for ImgBB SDK
"""

import sys
from typing import BinaryIO, Union

if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


class ImgBBUploadOptions(TypedDict, total=False):
    """Options for uploading an image to ImgBB.
    
    Attributes:
        key: Your ImgBB API key (required)
        image: The image to upload - can be a file path, file object, bytes, or URL (required)
        name: Optional custom name for the uploaded image
        expiration: Optional auto-deletion time in seconds (60-15552000)
    """
    key: str
    image: Union[str, bytes, BinaryIO]
    name: str
    expiration: int


class ImgBBImageInfo(TypedDict):
    """Information about an uploaded image variant.
    
    Attributes:
        filename: The filename of the image
        name: The name of the image
        mime: The MIME type of the image
        extension: The file extension
        url: The URL to access the image
    """
    filename: str
    name: str
    mime: str
    extension: str
    url: str


class ImgBBImageData(TypedDict):
    """Complete data for an uploaded image.
    
    Attributes:
        id: The unique ID of the uploaded image
        title: The title of the image
        url_viewer: URL to view the image on ImgBB website
        url: Direct URL to the image
        display_url: Display URL for the image
        width: Width of the image in pixels
        height: Height of the image in pixels
        size: Size of the image in bytes
        time: Upload timestamp
        expiration: Expiration time in seconds (0 if permanent)
        image: Information about the full-size image
        thumb: Information about the thumbnail
        medium: Information about the medium-size variant
        delete_url: URL to delete the image
    """
    id: str
    title: str
    url_viewer: str
    url: str
    display_url: str
    width: str
    height: str
    size: str
    time: str
    expiration: str
    image: ImgBBImageInfo
    thumb: ImgBBImageInfo
    medium: ImgBBImageInfo
    delete_url: str


class ImgBBResponse(TypedDict):
    """Response from ImgBB API.
    
    Attributes:
        data: The uploaded image data
        success: Whether the upload was successful
        status: HTTP status code
    """
    data: ImgBBImageData
    success: bool
    status: int
