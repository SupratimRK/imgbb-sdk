"""
Flask example for ImgBB image upload
Install: pip install flask imgbb-sdk
Run: python flask_example.py
"""

import os

from flask import Flask, jsonify, render_template_string, request

from imgbb_sdk import ImgBBError, imgbb_upload

app = Flask(__name__)
IMGBB_API_KEY = os.getenv("IMGBB_API_KEY")

# Simple HTML template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>ImgBB Upload - Flask Example</title>
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
        .error {
            background: #ffe0e0;
            color: #cc0000;
        }
        .success {
            background: #e0ffe0;
            color: #006600;
        }
        img {
            max-width: 100%;
            margin-top: 10px;
        }
    </style>
</head>
<body>
    <h1>🖼️ ImgBB Image Upload</h1>
    <div class="upload-form">
        <form id="uploadForm" enctype="multipart/form-data">
            <input type="file" name="image" accept="image/*" required>
            <br><br>
            <input type="text" name="name" placeholder="Custom name (optional)">
            <br><br>
            <label>
                Auto-delete after:
                <select name="expiration">
                    <option value="0">Never</option>
                    <option value="600">10 minutes</option>
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

                if (data.success) {
                    result.className = 'result success';
                    result.innerHTML = `
                        <h3>✅ Upload Successful!</h3>
                        <p><strong>URL:</strong> <a href="${data.url}" target="_blank">${data.url}</a></p>
                        <p><strong>Size:</strong> ${data.width}x${data.height}</p>
                        <img src="${data.url}" alt="Uploaded image">
                        <p><small>Delete URL: ${data.delete_url}</small></p>
                    `;
                } else {
                    result.className = 'result error';
                    result.innerHTML = `<h3>❌ Upload Failed</h3><p>${data.error}</p>`;
                }
            } catch (error) {
                result.className = 'result error';
                result.innerHTML = `<h3>❌ Error</h3><p>${error.message}</p>`;
            }
        };
    </script>
</body>
</html>
"""


@app.route("/")
def index():
    """Render the upload form."""
    return render_template_string(HTML_TEMPLATE)


@app.route("/upload", methods=["POST"])
def upload():
    """Handle image upload."""
    if not IMGBB_API_KEY:
        return jsonify({"error": "IMGBB_API_KEY not configured"}), 500

    if "image" not in request.files:
        return jsonify({"error": "No image provided"}), 400

    file = request.files["image"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    # Get optional parameters
    name = request.form.get("name", "")
    expiration = int(request.form.get("expiration", 0))

    try:
        # Upload to ImgBB
        response = imgbb_upload(
            key=IMGBB_API_KEY,
            image=file.read(),
            name=name or file.filename or "",
            expiration=expiration,
        )

        return jsonify(
            {
                "success": True,
                "url": response["data"]["url"],
                "display_url": response["data"]["display_url"],
                "delete_url": response["data"]["delete_url"],
                "width": response["data"]["width"],
                "height": response["data"]["height"],
            }
        )

    except ImgBBError as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    if not IMGBB_API_KEY:
        print("⚠️  Warning: IMGBB_API_KEY environment variable not set")
        print("Set it with: export IMGBB_API_KEY='your-key'")

    print("🚀 Starting Flask server...")
    print("📍 Open http://localhost:5000 in your browser")
    app.run(debug=True, port=5000)
