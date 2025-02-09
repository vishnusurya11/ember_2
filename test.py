import os
from PIL import Image

def resize_and_compress_images(input_folder, output_folder, target_size=(1280, 720), max_file_size=2 * 1024 * 1024):
    """
    Reads images from input_folder, resizes them to a 16:9 format for YouTube thumbnails,
    compresses them to be strictly under 2MB, and saves them in output_folder.

    :param input_folder: Path to the folder containing images.
    :param output_folder: Path where resized images will be saved.
    :param target_size: Desired resolution (default: 1280x720, HD).
    :param max_file_size: Maximum allowed file size in bytes (strictly under 2MB).
    """

    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Supported image formats
    valid_extensions = (".jpg", ".jpeg", ".png", ".webp")

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(valid_extensions):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)

            try:
                # Open image
                with Image.open(input_path) as img:
                    # Convert to RGB (to avoid transparency issues)
                    if img.mode in ("RGBA", "P"):
                        img = img.convert("RGB")

                    # Resize while maintaining aspect ratio
                    img.thumbnail(target_size)

                    # Initialize compression
                    quality = 95  # Start with high quality
                    while True:
                        # Save with compression
                        img.save(output_path, "JPEG", quality=quality, optimize=True)
                        file_size = os.path.getsize(output_path)

                        # Ensure file is STRICTLY under 2MB
                        if file_size <= max_file_size or quality <= 20:
                            break
                        quality -= 5  # Reduce quality incrementally

                    # Double-check final file size
                    final_size = os.path.getsize(output_path)
                    if final_size > max_file_size:
                        print(f"❌ {filename} could not be reduced below 2MB!")
                        os.remove(output_path)  # Remove oversized file
                    else:
                        print(f"✅ Processed: {filename} -> {output_path} ({final_size / 1024:.2f} KB)")

            except Exception as e:
                print(f"❌ Error processing {filename}: {e}")

# Example Usage
input_folder = r"E:\ComfyUI_windows_portable\ComfyUI\output\api\20250207225733\thumbnail"
output_folder = r"E:\Ember_V2\ember_2.0\playground"

# Default HD resolution (1280x720)
# resize_and_compress_images(input_folder, output_folder, target_size=(1280, 720))

# Full HD (1920x1080)
# resize_and_compress_images(input_folder, output_folder, target_size=(1920, 1080))

# 2K (2560x1440)
# resize_and_compress_images(input_folder, output_folder, target_size=(2560, 1440))

# 4K (3840x2160)  # May be harder to keep under 2MB
resize_and_compress_images(input_folder, output_folder, target_size=(3840, 2160))

