import cv2
import numpy as np
import tensorflow as tf
import os

# 1. LOAD YOUR AI MODEL
model_path = os.path.join(os.path.dirname(__file__), 'my_first_ai_model.h5')
model = tf.keras.models.load_model(model_path)

# 2. PATHS
image_filename = "image.jpg"
script_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(script_dir, image_filename)

def extract_and_save():
    image = cv2.imread(image_path)
    if image is None: return print("Image not found")

    # PRE-PROCESS
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Binary threshold (Invert so text is white, background is black for the AI)
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)

    # 3. FIND LETTERS (CONTOURS)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Sort contours: First by Y (top to bottom), then by X (left to right)
    # This ensures we read lines in order
    contours = sorted(contours, key=lambda c: (cv2.boundingRect(c)[1] // 10, cv2.boundingRect(c)[0]))

    final_text = ""
    
    print(f"Reading {len(contours)} characters...")

    for ctr in contours:
        x, y, w, h = cv2.boundingRect(ctr)
        
        # Filter noise (ignore tiny specks)
        if w > 5 and h > 10:
            # Crop the character
            roi = gray[y:y+h, x:x+w]
            
            # Prepare for AI (Resize to 28x28 and Normalize)
            roi = cv2.resize(roi, (28, 28))
            roi = roi / 255.0
            roi = np.expand_dims(roi, axis=(0, -1))
            
            # 4. PREDICT
            prediction = model.predict(roi, verbose=0)
            char_index = np.argmax(prediction)
            
            # Map index to character (Assuming MNIST for now)
            # If your model knows letters, you'd change this mapping
            final_text += str(char_index) 

    # 5. SAVE TO TXT
    output_path = os.path.join(script_dir, "book_output.txt")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(final_text)
    
    print(f"Success! Characters saved to {output_path}")

if __name__ == "__main__":
    extract_and_save()