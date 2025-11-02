"""
Example CLI script for uploading images to ImgBB
Usage: python upload_cli.py /path/to/image.jpg
"""

import os
import sys
from pathlib import Path

# Add the src directory to the path for local development
sys.path.insert(0, str(Path(__file__).parent / "src"))

from imgbb_sdk import ImgBBError, imgbb_upload


def main():
    """Main CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: python upload_cli.py <image_path> [name] [expiration]")
        print("\nArguments:")
        print("  image_path   : Path to the image file (required)")
        print("  name         : Custom name for the image (optional)")
        print("  expiration   : Auto-deletion time in seconds (optional, 60-15552000)")
        print("\nExample:")
        print("  python upload_cli.py image.jpg my-image 3600")
        sys.exit(1)

    # Get arguments
    image_path = sys.argv[1]
    name = sys.argv[2] if len(sys.argv) > 2 else ""
    expiration = int(sys.argv[3]) if len(sys.argv) > 3 else 0

    # Get API key from environment
    api_key = os.getenv("IMGBB_API_KEY")
    if not api_key:
        print("❌ Error: IMGBB_API_KEY environment variable not set")
        print("\nTo set it:")
        print("  Linux/Mac: export IMGBB_API_KEY='your-key'")
        print("  Windows:   set IMGBB_API_KEY=your-key")
        sys.exit(1)

    # Validate file exists
    if not Path(image_path).exists():
        print(f"❌ Error: File not found: {image_path}")
        sys.exit(1)

    try:
        print(f"📤 Uploading {image_path}...")
        if name:
            print(f"   Name: {name}")
        if expiration:
            print(f"   Expiration: {expiration} seconds")

        # Upload the image
        response = imgbb_upload(key=api_key, image=image_path, name=name, expiration=expiration)

        # Print success information
        print("\n✅ Upload successful!")
        print(f"📷 Image ID: {response['data']['id']}")
        print(f"📐 Size: {response['data']['width']}x{response['data']['height']}")
        print(f"💾 File size: {int(response['data']['size']) / 1024:.2f} KB")
        print("\n🔗 URLs:")
        print(f"   Viewer:  {response['data']['url_viewer']}")
        print(f"   Direct:  {response['data']['url']}")
        print(f"   Display: {response['data']['display_url']}")
        print(f"\n🗑️  Delete URL: {response['data']['delete_url']}")

        if response["data"]["expiration"] != "0":
            exp_hours = int(response["data"]["expiration"]) / 3600
            print(f"⏰ Will expire in: {exp_hours:.1f} hours")
        else:
            print("♾️  Permanent storage")

    except ImgBBError as e:
        print(f"\n❌ Upload failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
