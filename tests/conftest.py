"""
Shared test fixtures and configuration
"""

import pytest


@pytest.fixture
def sample_image_bytes():
    """Return a sample 1x1 PNG image as bytes."""
    # 1x1 transparent PNG
    return bytes.fromhex(
        "89504e470d0a1a0a0000000d494844520000000100000001"
        "08020000009077535e0000000c49444154789c6364000082"
        "00810000000000ffff03000600054c3c7c440000000049454e44ae426082"
    )


@pytest.fixture
def sample_api_response():
    """Return a sample successful API response."""
    return {
        "data": {
            "id": "2ndCYJK",
            "title": "test-image",
            "url_viewer": "https://ibb.co/2ndCYJK",
            "url": "https://i.ibb.co/w04Prt6/test-image.png",
            "display_url": "https://i.ibb.co/98W13PY/test-image.png",
            "width": "1920",
            "height": "1080",
            "size": "42000",
            "time": "1552042565",
            "expiration": "0",
            "image": {
                "filename": "test-image.png",
                "name": "test-image",
                "mime": "image/png",
                "extension": "png",
                "url": "https://i.ibb.co/w04Prt6/test-image.png",
            },
            "thumb": {
                "filename": "test-image.png",
                "name": "test-image",
                "mime": "image/png",
                "extension": "png",
                "url": "https://i.ibb.co/2ndCYJK/test-image.png",
            },
            "medium": {
                "filename": "test-image.png",
                "name": "test-image",
                "mime": "image/png",
                "extension": "png",
                "url": "https://i.ibb.co/98W13PY/test-image.png",
            },
            "delete_url": "https://ibb.co/2ndCYJK/670a7e48ddcb85ac340c717a41047e5c",
        },
        "success": True,
        "status": 200,
    }
