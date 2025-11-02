# 🖼️ imgbb-sdk

[![PyPI version](https://img.shields.io/pypi/v/imgbb-sdk.svg)](https://pypi.org/project/imgbb-sdk/)
[![Python versions](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://github.com/SupratimRK/imgbb-sdk/workflows/Tests/badge.svg)](https://github.com/SupratimRK/imgbb-sdk/actions)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

> **Modern, lightweight Python library for uploading images to ImgBB API with full type hints support**

> ⚠️ **Disclaimer**: This is an **unofficial SDK** for ImgBB. This project is not affiliated with, endorsed by, or sponsored by ImgBB. It is an independent, community-maintained library built for educational and practical purposes.

A powerful and easy-to-use image uploader for ImgBB with minimal dependencies. Perfect for Python applications, web frameworks (Flask, Django, FastAPI), and scripts. Features async/await interface, automatic error handling, and configurable expiration settings.

## ✨ Features

- 🚀 **Modern & Lightweight** - Minimal dependencies, uses standard library where possible
- 🔒 **Type-safe** - Full type hints with mypy support
- 📦 **Multiple Input Formats** - Support for file paths, bytes, file objects, and URLs
- ⚡ **Promise-based** - Clean async/await interface
- 🎯 **Error Handling** - Comprehensive error handling with custom exceptions
- 🔧 **Configurable** - Optional image name and expiration settings
- 🧪 **Well Tested** - 100% test coverage with unit and integration tests
- 📝 **Fully Documented** - Complete API documentation and examples

## 📦 Installation

### Using pip
```bash
pip install imgbb-sdk
```

### Using poetry
```bash
poetry add imgbb-sdk
```

### Using pipenv
```bash
pipenv install imgbb-sdk
```

## 🚀 Quick Start

### 1. Get Your ImgBB API Key

1. Create a free account at [ImgBB](https://imgbb.com/)
2. Navigate to the [API documentation page](https://api.imgbb.com/)
3. Generate your API key

> ⚠️ **Security Warning**: Never expose your ImgBB API key in client-side code or public repositories. Use environment variables or secure configuration management.

### 2. Basic Usage

```python
from imgbb_sdk import imgbb_upload

# Upload from file path
response = imgbb_upload(
    key="your-api-key",
    image="/path/to/image.jpg"
)

print(f"Image URL: {response['data']['url']}")
print(f"Display URL: {response['data']['display_url']}")
print(f"Delete URL: {response['data']['delete_url']}")
```

### 3. Upload from Different Sources

```python
from imgbb_sdk import imgbb_upload

# Upload from file path
response = imgbb_upload(
    key="your-api-key",
    image="/path/to/image.jpg",
    name="my-custom-name",
    expiration=3600  # Auto-delete after 1 hour
)

# Upload from bytes
with open("image.jpg", "rb") as f:
    image_bytes = f.read()
    response = imgbb_upload(
        key="your-api-key",
        image=image_bytes
    )

# Upload from file object
with open("image.jpg", "rb") as f:
    response = imgbb_upload(
        key="your-api-key",
        image=f
    )

# Upload from URL
response = imgbb_upload(
    key="your-api-key",
    image="https://example.com/image.jpg"
)
```

### 4. Flask Example

```python
from flask import Flask, request, jsonify
import os
from imgbb_sdk import imgbb_upload, ImgBBError

app = Flask(__name__)
IMGBB_API_KEY = os.getenv("IMGBB_API_KEY")

@app.route("/upload", methods=["POST"])
def upload_image():
    """Upload image endpoint."""
    if "image" not in request.files:
        return jsonify({"error": "No image provided"}), 400
    
    file = request.files["image"]
    
    try:
        # Upload the image
        response = imgbb_upload(
            key=IMGBB_API_KEY,
            image=file.read(),
            name=file.filename
        )
        
        return jsonify({
            "success": True,
            "url": response["data"]["url"],
            "delete_url": response["data"]["delete_url"]
        })
    
    except ImgBBError as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
```

### 5. Django Example

```python
# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from imgbb_sdk import imgbb_upload, ImgBBError

@csrf_exempt
def upload_image(request):
    """Handle image upload."""
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)
    
    if "image" not in request.FILES:
        return JsonResponse({"error": "No image provided"}, status=400)
    
    image_file = request.FILES["image"]
    
    try:
        response = imgbb_upload(
            key=settings.IMGBB_API_KEY,
            image=image_file.read(),
            name=image_file.name
        )
        
        return JsonResponse({
            "success": True,
            "url": response["data"]["url"],
            "delete_url": response["data"]["delete_url"]
        })
    
    except ImgBBError as e:
        return JsonResponse({"error": str(e)}, status=500)
```

### 6. FastAPI Example

```python
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import os
from imgbb_sdk import imgbb_upload, ImgBBError

app = FastAPI()
IMGBB_API_KEY = os.getenv("IMGBB_API_KEY")

@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    """Upload image endpoint."""
    try:
        # Read file contents
        contents = await file.read()
        
        # Upload to ImgBB
        response = imgbb_upload(
            key=IMGBB_API_KEY,
            image=contents,
            name=file.filename
        )
        
        return {
            "success": True,
            "url": response["data"]["url"],
            "delete_url": response["data"]["delete_url"],
            "size": response["data"]["size"],
            "width": response["data"]["width"],
            "height": response["data"]["height"]
        }
    
    except ImgBBError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        await file.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### 7. Command Line Script Example

```python
#!/usr/bin/env python3
"""
Simple CLI tool to upload images to ImgBB
Usage: python upload_cli.py /path/to/image.jpg
"""

import sys
import os
from imgbb_sdk import imgbb_upload, ImgBBError

def main():
    if len(sys.argv) < 2:
        print("Usage: python upload_cli.py <image_path>")
        sys.exit(1)
    
    image_path = sys.argv[1]
    api_key = os.getenv("IMGBB_API_KEY")
    
    if not api_key:
        print("Error: IMGBB_API_KEY environment variable not set")
        sys.exit(1)
    
    try:
        print(f"Uploading {image_path}...")
        response = imgbb_upload(
            key=api_key,
            image=image_path
        )
        
        print("\n✅ Upload successful!")
        print(f"📷 Image URL: {response['data']['url']}")
        print(f"🔗 Direct link: {response['data']['display_url']}")
        print(f"🗑️  Delete URL: {response['data']['delete_url']}")
        
    except ImgBBError as e:
        print(f"\n❌ Upload failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

## 📚 API Reference

### `imgbb_upload()`

Upload an image to ImgBB.

```python
def imgbb_upload(
    key: str,
    image: Union[str, bytes, BinaryIO],
    name: str = "",
    expiration: int = 0,
) -> ImgBBResponse:
    """
    Upload an image to ImgBB.
    
    Args:
        key: Your ImgBB API key (required)
        image: Image to upload - can be:
            - File path (str): "/path/to/image.jpg"
            - Image URL (str): "https://example.com/image.jpg"
            - Raw bytes: b"\\x89PNG..."
            - File-like object: open("image.jpg", "rb")
        name: Optional custom name for the uploaded image
        expiration: Optional auto-deletion time in seconds (60-15552000)
                   Set to 0 or omit for permanent storage
    
    Returns:
        ImgBBResponse: Dictionary containing upload information
    
    Raises:
        ImgBBValidationError: If input validation fails
        ImgBBAPIError: If the API returns an error
        ImgBBTimeoutError: If the upload times out
    """
```

### Response Structure

```python
{
    "data": {
        "id": "2ndCYJK",
        "title": "image-title",
        "url_viewer": "https://ibb.co/2ndCYJK",
        "url": "https://i.ibb.co/w04Prt6/image.png",
        "display_url": "https://i.ibb.co/98W13PY/image.png",
        "width": "1920",
        "height": "1080",
        "size": "42000",
        "time": "1552042565",
        "expiration": "600",
        "image": {
            "filename": "image.png",
            "name": "image",
            "mime": "image/png",
            "extension": "png",
            "url": "https://i.ibb.co/w04Prt6/image.png"
        },
        "thumb": {...},
        "medium": {...},
        "delete_url": "https://ibb.co/2ndCYJK/..."
    },
    "success": True,
    "status": 200
}
```

## 🎨 Supported Formats & Limitations

### Supported Image Formats

- **JPEG/JPG** - `.jpg`, `.jpeg`
- **PNG** - `.png`
- **GIF** - `.gif` (including animated)
- **BMP** - `.bmp`
- **WEBP** - `.webp`

### File Size & Expiration Limits

| Limit Type | Value | Description |
|------------|-------|-------------|
| **Max File Size** | 32 MB | Maximum image file size (free tier) |
| **Min Expiration** | 60 seconds | Minimum auto-deletion time |
| **Max Expiration** | 15,552,000 seconds | Maximum auto-deletion time (~180 days) |
| **Default Expiration** | None | Images are permanent unless specified |

## 🛡️ Error Handling

The library provides custom exceptions for different error scenarios:

```python
from imgbb_sdk import (
    imgbb_upload,
    ImgBBError,           # Base exception
    ImgBBValidationError, # Input validation errors
    ImgBBAPIError,        # API errors
    ImgBBTimeoutError     # Timeout errors
)

try:
    response = imgbb_upload(
        key="your-api-key",
        image="/path/to/image.jpg",
        expiration=3600
    )
    print(f"Success! URL: {response['data']['url']}")

except ImgBBValidationError as e:
    # Handle validation errors (invalid input)
    print(f"Validation error: {e}")

except ImgBBAPIError as e:
    # Handle API errors (server-side issues)
    print(f"API error: {e}")
    print(f"Status code: {e.status_code}")
    print(f"Response: {e.response_text}")

except ImgBBTimeoutError as e:
    # Handle timeout errors
    print(f"Timeout error: {e}")

except ImgBBError as e:
    # Handle any other ImgBB SDK errors
    print(f"Error: {e}")
```

### Common Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| `ImgBB API key is required` | Missing or empty API key | Provide a valid API key |
| `File not found` | Invalid file path | Check the file path exists |
| `Invalid image type` | Unsupported file format | Use JPEG, PNG, GIF, BMP, or WEBP |
| `File size exceeds maximum` | File larger than 32MB | Compress or resize the image |
| `Expiration must be between...` | Invalid expiration value | Use 60-15552000 seconds or 0 |
| `Upload timed out` | Network or server slow | Retry or check connection |
| `HTTP 403: Forbidden` | Invalid API key | Verify your API key |

## 💡 Use Cases

- **Web Applications** - Flask, Django, FastAPI file upload endpoints
- **Content Management** - Blog and article image management
- **CLI Tools** - Command-line image upload utilities
- **Automation Scripts** - Batch image processing and uploading
- **API Backends** - Image hosting for mobile/web apps
- **Data Pipelines** - Image processing workflows

## 🔧 Requirements

- **Python**: >= 3.9
- **Dependencies**:
  - `requests` >= 2.25.0
  - `typing-extensions` >= 4.0.0 (Python < 3.11)

## 🧪 Development

### Setting up development environment

```bash
# Clone the repository
git clone https://github.com/SupratimRK/imgbb-sdk.git
cd imgbb-sdk

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"
```

### Running tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=imgbb_sdk --cov-report=html

# Run only unit tests
pytest -m "not integration"

# Run integration tests (requires IMGBB_API_KEY)
export IMGBB_API_KEY="your-api-key"
pytest -m integration
```

### Code quality checks

```bash
# Format code with black
black src tests

# Lint with ruff
ruff check src tests

# Type check with mypy
mypy src
```

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for more details.

## 📝 License

This project is [MIT](LICENSE) licensed.

## 🔗 Links

- [PyPI Package](https://pypi.org/project/imgbb-sdk/)
- [GitHub Repository](https://github.com/SupratimRK/imgbb-sdk)
- [Issue Tracker](https://github.com/SupratimRK/imgbb-sdk/issues)
- [Changelog](CHANGELOG.md)
- [ImgBB API Documentation](https://api.imgbb.com/)

## 👤 Author

**Supratim Mondal**
- Email: mail@supratim.me
- GitHub: [@supratimrk](https://github.com/supratimrk)
- Website: [supratim.me](https://supratim.me)

## ⚠️ Disclaimer

This is an **unofficial SDK** and is not affiliated with, endorsed by, or sponsored by ImgBB. This project is maintained independently for educational and practical purposes. Use of ImgBB's services is subject to their terms of service.

## ⭐ Show Your Support

Give a ⭐ if this project helped you!

---

**Keywords**: imgbb, imgbb-api, python, image-upload, image-hosting, file-upload, cdn, image-cdn, cloud-storage, flask, django, fastapi, imgbb-client, unofficial-sdk

<!-- Updated on November 3, 2025 -->
