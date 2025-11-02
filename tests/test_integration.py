"""
Integration tests for ImgBB SDK
These tests make actual API calls and should be run with a valid API key.
"""

import os

import pytest

from imgbb_sdk import imgbb_upload

# Skip integration tests if no API key is provided
IMGBB_API_KEY = os.getenv("IMGBB_API_KEY")
pytestmark = pytest.mark.skipif(
    not IMGBB_API_KEY, reason="IMGBB_API_KEY environment variable not set"
)


@pytest.mark.integration
class TestIntegration:
    """Integration tests with real API."""

    def test_real_upload_from_bytes(self):
        """Test real upload from bytes."""
        # Sample 1x1 PNG
        png_bytes = bytes.fromhex(
            "89504e470d0a1a0a0000000d494844520000000100000001"
            "08020000009077535e0000000c49444154789c6364000082"
            "00810000000000ffff03000600054c3c7c440000000049454e44ae426082"
        )

        result = imgbb_upload(
            key=IMGBB_API_KEY, image=png_bytes, name="test-integration"  # type: ignore
        )

        assert result["success"] is True
        assert result["data"]["url"]
        assert result["data"]["delete_url"]
        print(f"Uploaded image: {result['data']['url']}")

    def test_real_upload_with_expiration(self):
        """Test real upload with expiration."""
        png_bytes = bytes.fromhex(
            "89504e470d0a1a0a0000000d494844520000000100000001"
            "08020000009077535e0000000c49444154789c6364000082"
            "00810000000000ffff03000600054c3c7c440000000049454e44ae426082"
        )

        result = imgbb_upload(
            key=IMGBB_API_KEY, image=png_bytes, expiration=3600  # type: ignore  # 1 hour
        )

        assert result["success"] is True
        assert result["data"]["expiration"] == "3600"
        print(f"Image will expire in 1 hour: {result['data']['url']}")
