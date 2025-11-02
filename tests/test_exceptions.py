"""
Tests for exception classes
"""

import pytest

from imgbb_sdk.exceptions import (
    ImgBBAPIError,
    ImgBBError,
    ImgBBTimeoutError,
    ImgBBValidationError,
)


def test_base_exception():
    """Test base ImgBBError exception."""
    error = ImgBBError("Test error")
    assert str(error) == "Test error"
    assert isinstance(error, Exception)


def test_validation_error():
    """Test ImgBBValidationError exception."""
    error = ImgBBValidationError("Validation failed")
    assert str(error) == "Validation failed"
    assert isinstance(error, ImgBBError)


def test_api_error():
    """Test ImgBBAPIError exception with all attributes."""
    error = ImgBBAPIError(
        "API error occurred",
        status_code=403,
        response_text="Forbidden"
    )
    assert str(error) == "API error occurred"
    assert error.status_code == 403
    assert error.response_text == "Forbidden"
    assert isinstance(error, ImgBBError)


def test_api_error_defaults():
    """Test ImgBBAPIError with default values."""
    error = ImgBBAPIError("API error")
    assert str(error) == "API error"
    assert error.status_code == 0
    assert error.response_text == ""


def test_timeout_error():
    """Test ImgBBTimeoutError exception."""
    error = ImgBBTimeoutError("Request timed out")
    assert str(error) == "Request timed out"
    assert isinstance(error, ImgBBError)
