import cv2
import pytesseract
import os

# 1. TELL PYTHON WHERE TESSERACT IS
# (Make sure you've installed the Tesseract EXE from the link I gave earlier!)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# 2. FILE LOCATIONS (Same folder as this script)
image_name = "image.jpg"
current_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(current_dir, image_name)
output_path = os.path.join(current_dir, "book_text.txt")

def simple_photo_to_txt():
    # Load the image
    img = cv2.imread(image_path)
    if img is None:
        return print(f"Error: Put '{image_name}' in this folder: {current_dir}")

    # Clean the image (Make it Black & White for better accuracy)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    clean_img = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    # Convert to Text 
    # '-l sqi' = Albanian language, '--psm 3' = Keep the original layout/spacing
    text = pytesseract.image_to_string(clean_img, config='-l sqi --psm 3')

    # Save to .txt
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)

    print(f"Done! Open '{output_path}' to see your text.")

if __name__ == "__main__":
    simple_photo_to_txt()