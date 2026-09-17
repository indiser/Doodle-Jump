from rembg import remove, new_session
from PIL import Image
import sys

input_path = 'Game_Assests/resume.png'
output_path = 'Game_Assests/resume_transparent.png'

try:
    print("Initializing lightweight model...")
    # Force the engine to use the small model to prevent 'bad allocation' OOM crashes
    session = new_session("u2netp")
    
    input_image = Image.open(input_path)
    
    # Pass the custom session into the remove function
    output_image = remove(input_image, session=session)
    
    output_image.save(output_path, "PNG")
    print(f"Success. Transparent asset saved to {output_path}")
    
except Exception as e:
    print(f"Fatal error: {e}")
    sys.exit(1)