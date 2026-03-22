import os
from PIL import Image

# REMOVE THE SIZE LIMIT
Image.MAX_IMAGE_PIXELS = None 

# --- CONFIGURATION ---
INPUT_FOLDER = "slices"
OUTPUT_NAME = "restored_image.png"
# ---------------------

def rebuild_image(folder_path, output_name):
    if not os.path.exists(folder_path):
        print(f"Error: Folder '{folder_path}' not found.")
        return

    try:
        first_slice_path = os.path.join(folder_path, "slice_0_0.png")
        with Image.open(first_slice_path) as first_slice:
            slice_w, slice_h = first_slice.size
    except Exception as e:
        print(f"Error opening slice: {e}")
        return

    full_width = slice_w * 3
    full_height = slice_h * 3
    
    # Create the large canvas
    print(f"Creating canvas ({full_width}x{full_height})...")
    canvas = Image.new("RGB", (full_width, full_height))

    for row in range(3):
        for col in range(3):
            file_path = os.path.join(folder_path, f"slice_{row}_{col}.png")
            if os.path.exists(file_path):
                with Image.open(file_path) as slice_img:
                    canvas.paste(slice_img, (col * slice_w, row * slice_h))
                    print(f"Pasted slice_{row}_{col}.png")
            else:
                print(f"Warning: Missing {file_path}")

    print("Saving massive image... this may take a moment.")
    canvas.save(output_name)
    print(f"Done! Image restored as '{output_name}'.")

if __name__ == "__main__":
    rebuild_image(INPUT_FOLDER, OUTPUT_NAME)