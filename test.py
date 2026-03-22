import os
from PIL import Image

def slice_image(image_path, output_folder="slices"):
    # 1. Create the output directory if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Created folder: {output_folder}")

    # 2. Open the image
    try:
        img = Image.open(image_path)
        img_width, img_height = img.size
    except Exception as e:
        print(f"Error opening image: {e}")
        return

    # 3. Calculate dimensions for a 3x3 grid
    # We use integer division to avoid float pixel issues
    slice_width = img_width // 3
    slice_height = img_height // 3

    # 4. Loop through coordinates and crop
    count = 0
    for row in range(3):
        for col in range(3):
            # Define the box: (left, upper, right, lower)
            left = col * slice_width
            upper = row * slice_height
            
            # For the last column/row, we go to the full width/height 
            # to avoid losing pixels due to rounding
            right = (col + 1) * slice_width if col < 2 else img_width
            lower = (row + 1) * slice_height if row < 2 else img_height

            # Crop and save
            box = (left, upper, right, lower)
            working_slice = img.crop(box)
            
            file_name = f"slice_{row}_{col}.png"
            working_slice.save(os.path.join(output_folder, file_name))
            count += 1

    print(f"Success! {count} slices saved to '{output_folder}'.")

# Run the function
if __name__ == "__main__":
    # Replace 'your_image.jpg' with your actual filename
    slice_image("29890.png")