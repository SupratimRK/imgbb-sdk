# imgbb-sdk Examples

This directory contains example implementations of the imgbb-sdk library.

## Examples

### 1. CLI Upload Tool (`upload_cli.py`)

A command-line tool for uploading images.

**Usage:**
```bash
export IMGBB_API_KEY="your-api-key"
python upload_cli.py /path/to/image.jpg
python upload_cli.py image.jpg my-image 3600
```

### 2. Flask Web Application (`flask_example.py`)

A simple web application with an upload form.

**Installation:**
```bash
pip install flask imgbb-sdk
```

**Run:**
```bash
export IMGBB_API_KEY="your-api-key"
python flask_example.py
```

Then open http://localhost:5000

### 3. FastAPI Application (`fastapi_example.py`)

A modern async API with automatic documentation.

**Installation:**
```bash
pip install fastapi uvicorn imgbb-sdk python-multipart
```

**Run:**
```bash
export IMGBB_API_KEY="your-api-key"
python fastapi_example.py
```

Then open:
- http://localhost:8000 - Upload form
- http://localhost:8000/docs - API documentation

## Environment Setup

All examples require the `IMGBB_API_KEY` environment variable:

**Linux/Mac:**
```bash
export IMGBB_API_KEY="your-api-key"
```

**Windows (Command Prompt):**
```cmd
set IMGBB_API_KEY=your-api-key
```

**Windows (PowerShell):**
```powershell
$env:IMGBB_API_KEY="your-api-key"
```

## Features Demonstrated

- ✅ File upload handling
- ✅ Custom image names
- ✅ Expiration settings
- ✅ Error handling
- ✅ Response processing
- ✅ Web forms
- ✅ REST APIs
- ✅ Async operations (FastAPI)
