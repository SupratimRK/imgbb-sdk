"""
FastAPI example for ImgBB image upload
Install: pip install fastapi uvicorn imgbb-sdk python-multipart
Run: python fastapi_example.py
"""

import os

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import HTMLResponse

from imgbb_sdk import ImgBBError, imgbb_upload

app = FastAPI(title="ImgBB Upload API", version="1.0.0")
IMGBB_API_KEY = os.getenv("IMGBB_API_KEY")

# HTML template for the upload form
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>ImgBB Upload - FastAPI Example</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 600px;
            margin: 50px auto;
            padding: 20px;
        }
        .upload-form {
            border: 2px dashed #ccc;
            padding: 20px;
            text-align: center;
        }
        .result {
            margin-top: 20px;
            padding: 15px;
            background: #f0f0f0;
            border-radius: 5px;
        }
        img { max-width: 100%; margin-top: 10px; }
    </style>
</head>
<body>
    <h1>🖼️ ImgBB Image Upload (FastAPI)</h1>
    <div class="upload-form">
        <form id="uploadForm" enctype="multipart/form-data">
            <input type="file" name="file" accept="image/*" required>
            <br><br>
            <input type="text" name="name" placeholder="Custom name (optional)">
            <br><br>
            <label>
                Auto-delete:
                <select name="expiration">
                    <option value="0">Never</option>
                    <option value="3600">1 hour</option>
                    <option value="86400">1 day</option>
                </select>
            </label>
            <br><br>
            <button type="submit">Upload</button>
        </form>
    </div>
    <div id="result"></div>

    <script>
        document.getElementById('uploadForm').onsubmit = async (e) => {
            e.preventDefault();
            const formData = new FormData(e.target);
            const result = document.getElementById('result');
            result.innerHTML = '<p>Uploading...</p>';

            try {
                const response = await fetch('/upload', {
                    method: 'POST',
                    body: formData
                });
                const data = await response.json();

                result.className = 'result';
                result.innerHTML = `
                    <h3>✅ Success!</h3>
                    <p><strong>URL:</strong> <a href="${data.url}">${data.url}</a></p>
                    <p><strong>Size:</strong> ${data.width}x${data.height}</p>
                    <img src="${data.url}">
                `;
            } catch (error) {
                result.innerHTML = `<h3>❌ Error: ${error.message}</h3>`;
            }
        };
    </script>
</body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
async def index():
    """Render the upload form."""
    return HTML_TEMPLATE


@app.post("/upload")
async def upload_image(
    file: UploadFile = File(...), name: str = Form(""), expiration: int = Form(0)
):
    """
    Upload an image to ImgBB.

    - **file**: Image file to upload
    - **name**: Optional custom name
    - **expiration**: Auto-deletion time in seconds (0 for permanent)
    """
    if not IMGBB_API_KEY:
        raise HTTPException(status_code=500, detail="IMGBB_API_KEY not configured")

    try:
        # Read file contents
        contents = await file.read()

        # Upload to ImgBB
        response = imgbb_upload(
            key=IMGBB_API_KEY,
            image=contents,
            name=name or file.filename or "",
            expiration=expiration,
        )

        return {
            "success": True,
            "url": response["data"]["url"],
            "display_url": response["data"]["display_url"],
            "delete_url": response["data"]["delete_url"],
            "width": response["data"]["width"],
            "height": response["data"]["height"],
            "size": response["data"]["size"],
        }

    except ImgBBError as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

    finally:
        await file.close()


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "api_key_configured": bool(IMGBB_API_KEY)}


if __name__ == "__main__":
    import uvicorn

    if not IMGBB_API_KEY:
        print("⚠️  Warning: IMGBB_API_KEY environment variable not set")
        print("Set it with: export IMGBB_API_KEY='your-key'")

    print("🚀 Starting FastAPI server...")
    print("📍 Open http://localhost:8000 in your browser")
    print("📚 API docs: http://localhost:8000/docs")

    uvicorn.run(app, host="0.0.0.0", port=8000)
