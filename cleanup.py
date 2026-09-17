from PIL import Image
import os

def clean_png_metadata(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".png"):
            filepath = os.path.join(directory, filename)
            try:
                # Opening and re-saving with Pillow strips the bad iCCP chunk
                with Image.open(filepath) as img:
                    img.save(filepath, format="PNG", icc_profile=None)
                print(f"Cleaned: {filename}")
            except Exception as e:
                print(f"Failed to clean {filename}: {e}")

# Point this at your asset folders
clean_png_metadata("Game_Assests/monsters")