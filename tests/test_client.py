"""
Unit tests for ImgBB SDK client
"""

import base64
import io

import pytest
import requests

from imgbb_sdk import imgbb_upload
from imgbb_sdk.exceptions import (
    ImgBBAPIError,
    ImgBBTimeoutError,
    ImgBBValidationError,
)

# Sample response from ImgBB API
SAMPLE_RESPONSE = {
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

# Sample 1x1 PNG image (base64)
SAMPLE_PNG_BASE64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
SAMPLE_PNG_BYTES = base64.b64decode(SAMPLE_PNG_BASE64)


class TestValidation:
    """Test input validation."""

    def test_empty_api_key(self):
        """Test that empty API key raises validation error."""
        with pytest.raises(ImgBBValidationError, match="API key is required"):
            imgbb_upload(key="", image=SAMPLE_PNG_BYTES)

    def test_none_api_key(self):
        """Test that None API key raises validation error."""
        with pytest.raises(ImgBBValidationError, match="API key is required"):
            imgbb_upload(key=None, image=SAMPLE_PNG_BYTES)  # type: ignore

    def test_whitespace_api_key(self):
        """Test that whitespace-only API key raises validation error."""
        with pytest.raises(ImgBBValidationError, match="API key is required"):
            imgbb_upload(key="   ", image=SAMPLE_PNG_BYTES)

    def test_invalid_expiration_too_low(self):
        """Test that expiration below minimum raises validation error."""
        with pytest.raises(ImgBBValidationError, match="Expiration must be a number between"):
            imgbb_upload(key="test-key", image=SAMPLE_PNG_BYTES, expiration=30)

    def test_invalid_expiration_too_high(self):
        """Test that expiration above maximum raises validation error."""
        with pytest.raises(ImgBBValidationError, match="Expiration must be a number between"):
            imgbb_upload(key="test-key", image=SAMPLE_PNG_BYTES, expiration=20000000)

    def test_invalid_expiration_type(self):
        """Test that non-integer expiration raises validation error."""
        with pytest.raises(ImgBBValidationError, match="Expiration must be an integer"):
            imgbb_upload(key="test-key", image=SAMPLE_PNG_BYTES, expiration="600")  # type: ignore

    def test_invalid_image_extension(self, tmp_path):
        """Test that invalid file extension raises validation error."""
        # Create a temporary .txt file
        test_file = tmp_path / "test.txt"
        test_file.write_bytes(b"not an image")

        with pytest.raises(ImgBBValidationError, match="Invalid image type"):
            imgbb_upload(key="test-key", image=str(test_file))

    def test_nonexistent_file(self):
        """Test that nonexistent file raises validation error."""
        with pytest.raises(ImgBBValidationError, match="File not found"):
            imgbb_upload(key="test-key", image="/path/to/nonexistent/file.png")

    def test_file_too_large(self, tmp_path):
        """Test that oversized file raises validation error."""
        # Create a temporary file larger than 32MB
        test_file = tmp_path / "large.png"
        test_file.write_bytes(b"x" * (33 * 1024 * 1024))  # 33 MB

        with pytest.raises(ImgBBValidationError, match="exceeds maximum allowed size"):
            imgbb_upload(key="test-key", image=str(test_file))


class TestImagePreparation:
    """Test image data preparation."""

    def test_bytes_upload(self, requests_mock):
        """Test uploading raw bytes."""
        requests_mock.post("https://api.imgbb.com/1/upload", json=SAMPLE_RESPONSE)

        result = imgbb_upload(key="test-key", image=SAMPLE_PNG_BYTES)

        assert result["success"] is True
        assert result["data"]["id"] == "2ndCYJK"

    def test_file_path_upload(self, tmp_path, requests_mock):
        """Test uploading from file path."""
        requests_mock.post("https://api.imgbb.com/1/upload", json=SAMPLE_RESPONSE)

        # Create a temporary PNG file
        test_file = tmp_path / "test.png"
        test_file.write_bytes(SAMPLE_PNG_BYTES)

        result = imgbb_upload(key="test-key", image=str(test_file))

        assert result["success"] is True
        assert result["data"]["id"] == "2ndCYJK"

    def test_file_object_upload(self, requests_mock):
        """Test uploading from file-like object."""
        requests_mock.post("https://api.imgbb.com/1/upload", json=SAMPLE_RESPONSE)

        file_obj = io.BytesIO(SAMPLE_PNG_BYTES)
        result = imgbb_upload(key="test-key", image=file_obj)

        assert result["success"] is True
        assert result["data"]["id"] == "2ndCYJK"

    def test_url_upload(self, requests_mock):
        """Test uploading from URL."""
        requests_mock.post("https://api.imgbb.com/1/upload", json=SAMPLE_RESPONSE)

        result = imgbb_upload(key="test-key", image="https://example.com/image.png")

        assert result["success"] is True
        # Verify the URL was passed directly (URL-encoded in form data)
        assert "https%3A%2F%2Fexample.com%2Fimage.png" in requests_mock.last_request.text


class TestAPIIntegration:
    """Test API integration."""

    def test_successful_upload(self, requests_mock):
        """Test successful upload with all parameters."""
        requests_mock.post("https://api.imgbb.com/1/upload", json=SAMPLE_RESPONSE)

        result = imgbb_upload(
            key="test-key", image=SAMPLE_PNG_BYTES, name="custom-name", expiration=600
        )

        assert result["success"] is True
        assert result["status"] == 200
        assert result["data"]["url"] == "https://i.ibb.co/w04Prt6/test-image.png"

        # Verify request parameters
        request = requests_mock.last_request
        assert "key=test-key" in request.url
        assert "expiration=600" in request.url
        assert "name=custom-name" in request.text

    def test_upload_without_optional_params(self, requests_mock):
        """Test upload without optional parameters."""
        requests_mock.post("https://api.imgbb.com/1/upload", json=SAMPLE_RESPONSE)

        result = imgbb_upload(key="test-key", image=SAMPLE_PNG_BYTES)

        assert result["success"] is True

        # Verify expiration is not in the request
        request = requests_mock.last_request
        assert "expiration" not in request.url

    def test_api_error_response(self, requests_mock):
        """Test handling of API error responses."""
        error_response = {"error": {"message": "Invalid API key", "code": 100}}
        requests_mock.post("https://api.imgbb.com/1/upload", json=error_response, status_code=403)

        with pytest.raises(ImgBBAPIError, match="HTTP 403"):
            imgbb_upload(key="invalid-key", image=SAMPLE_PNG_BYTES)

    def test_network_timeout(self, requests_mock):
        """Test handling of network timeout."""
        requests_mock.post("https://api.imgbb.com/1/upload", exc=requests.exceptions.Timeout)

        with pytest.raises(ImgBBTimeoutError, match="timed out"):
            imgbb_upload(key="test-key", image=SAMPLE_PNG_BYTES)

    def test_network_error(self, requests_mock):
        """Test handling of network errors."""
        requests_mock.post(
            "https://api.imgbb.com/1/upload",
            exc=requests.exceptions.ConnectionError("Connection failed"),
        )

        with pytest.raises(ImgBBAPIError, match="Network error"):
            imgbb_upload(key="test-key", image=SAMPLE_PNG_BYTES)

    def test_unsuccessful_api_response(self, requests_mock):
        """Test handling when API returns success=false."""
        error_response = {"success": False, "error": {"message": "Upload failed"}}
        requests_mock.post("https://api.imgbb.com/1/upload", json=error_response)

        with pytest.raises(ImgBBAPIError, match="Upload failed"):
            imgbb_upload(key="test-key", image=SAMPLE_PNG_BYTES)


class TestResponseStructure:
    """Test response structure."""

    def test_response_contains_all_fields(self, requests_mock):
        """Test that response contains all expected fields."""
        requests_mock.post("https://api.imgbb.com/1/upload", json=SAMPLE_RESPONSE)

        result = imgbb_upload(key="test-key", image=SAMPLE_PNG_BYTES)

        # Check top-level fields
        assert "data" in result
        assert "success" in result
        assert "status" in result

        # Check data fields
        data = result["data"]
        assert "id" in data
        assert "url" in data
        assert "display_url" in data
        assert "delete_url" in data
        assert "image" in data
        assert "thumb" in data
        assert "medium" in data

        # Check nested image info
        image_info = data["image"]
        assert "filename" in image_info
        assert "url" in image_info
        assert "mime" in image_info
        assert "extension" in image_info


class TestEdgeCases:
    """Test edge cases."""

    def test_zero_expiration(self, requests_mock):
        """Test that expiration=0 means permanent storage."""
        requests_mock.post("https://api.imgbb.com/1/upload", json=SAMPLE_RESPONSE)

        result = imgbb_upload(key="test-key", image=SAMPLE_PNG_BYTES, expiration=0)

        assert result["success"] is True
        # Should not include expiration in request
        request = requests_mock.last_request
        assert "expiration" not in request.url

    def test_minimum_valid_expiration(self, requests_mock):
        """Test minimum valid expiration (60 seconds)."""
        requests_mock.post("https://api.imgbb.com/1/upload", json=SAMPLE_RESPONSE)

        result = imgbb_upload(key="test-key", image=SAMPLE_PNG_BYTES, expiration=60)

        assert result["success"] is True
        assert "expiration=60" in requests_mock.last_request.url

    def test_maximum_valid_expiration(self, requests_mock):
        """Test maximum valid expiration (15552000 seconds)."""
        requests_mock.post("https://api.imgbb.com/1/upload", json=SAMPLE_RESPONSE)

        result = imgbb_upload(key="test-key", image=SAMPLE_PNG_BYTES, expiration=15552000)

        assert result["success"] is True
        assert "expiration=15552000" in requests_mock.last_request.url

    def test_file_object_with_name(self, requests_mock):
        """Test file object with name attribute."""
        requests_mock.post("https://api.imgbb.com/1/upload", json=SAMPLE_RESPONSE)

        file_obj = io.BytesIO(SAMPLE_PNG_BYTES)
        file_obj.name = "test.png"

        result = imgbb_upload(key="test-key", image=file_obj)

        assert result["success"] is True

    def test_supported_image_formats(self, tmp_path, requests_mock):
        """Test all supported image formats."""
        requests_mock.post("https://api.imgbb.com/1/upload", json=SAMPLE_RESPONSE)

        formats = [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"]

        for ext in formats:
            test_file = tmp_path / f"test{ext}"
            test_file.write_bytes(SAMPLE_PNG_BYTES)

            result = imgbb_upload(key="test-key", image=str(test_file))
            assert result["success"] is True
