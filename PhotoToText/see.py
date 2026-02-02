import cv2
import os

# 1. Setup paths
image_filename = "image.jpg"
script_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(script_dir, image_filename)

def segment_and_preview():
    # Load image
    image = cv2.imread(image_path)
    if image is None: return print("Image not found")

    # Convert to grayscale and blur to remove noise
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Thresholding to make text pop (Black and White)
    edged = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                  cv2.THRESH_BINARY_INV, 11, 2)

    # Find "contours" (The boxes around letters)
    contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Sort contours from top to bottom, left to right
    contours = sorted(contours, key=lambda ctr: cv2.boundingRect(ctr)[1])

    print(f"Found {len(contours)} potential characters!")

    # Draw boxes on the original image to see what was found
    for i, ctr in enumerate(contours):
        x, y, w, h = cv2.boundingRect(ctr)
        
        # Filter out tiny dots/noise (keep only shapes big enough to be letters)
        if w > 5 and h > 15:
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            # This is where you would feed the cropped letter to your AI:
            # character_crop = gray[y:y+h, x:x+w]
            # prediction = model.predict(character_crop)

    # Save the preview so you can see the boxes
    preview_path = os.path.join(script_dir, "detected_letters.jpg")
    cv2.imwrite(preview_path, image)
    print(f"Check 'detected_letters.jpg' to see how the AI 'sees' the letters.")

segment_and_preview()