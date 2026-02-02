import cv2
import numpy as np
import tensorflow as tf
import os

# 1. LOAD MODEL
# Ensure this file is in the same folder as your script!
model_path = os.path.join(os.path.dirname(__file__), 'my_first_ai_model.h5')
model = tf.keras.models.load_model(model_path)

def predict_digit(image_name):
    # 2. AUTOMATIC PATH LOCATOR
    # This finds the folder where THIS script is saved
    script_dir = os.path.dirname(os.path.abspath(__file__))
    full_image_path = os.path.join(script_dir, image_name)

    print(f"Looking for image at: {full_image_path}")

    # 3. LOAD IMAGE
    img = cv2.imread(full_image_path, cv2.IMREAD_GRAYSCALE)
    
    if img is None:
        print(f"❌ Error: Could not find '{image_name}' in that folder!")
        print("Check if the filename is spelled exactly right (including .jpg or .png)")
        return

    # 4. PRE-PROCESS
    img_resized = cv2.resize(img, (28, 28))
    img_resized = cv2.bitwise_not(img_resized) 
    img_final = img_resized / 255.0
    img_final = np.expand_dims(img_final, axis=(0, -1)) # Reshape to (1, 28, 28, 1)

    # 5. PREDICT
    prediction = model.predict(img_final)
    predicted_digit = np.argmax(prediction)
    print(f"✅ Prediction: {predicted_digit}")

# --- RUN IT ---
# Change '20260131_162857.jpg' to the name of your file
predict_digit('image.jpg')