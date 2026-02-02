import tensorflow as tf
from tensorflow.keras import layers, models
import os

# 1. SETUP DATASET
# Instead of manual labeling, we use the MNIST dataset 
# (the "ABC's" of AI training)
print("Loading dataset...")
mnist = tf.keras.datasets.mnist
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# Normalize: AI learns better when pixel values are between 0 and 1
x_train, x_test = x_train / 255.0, x_test / 255.0

# 2. DESIGN THE ARCHITECTURE (The "Brain" Structure)
model = models.Sequential([
    # This layer looks for edges and shapes
    layers.Flatten(input_shape=(28, 28)),
    
    # Hidden layers where the "thinking" happens
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.2), # Randomly shuts off neurons to make the AI more robust
    
    # Output layer: 10 nodes for digits 0-9
    layers.Dense(10, activation='softmax')
])

# 3. COMPILE
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# 4. TRAINING (The AI starts learning)
print("Training the AI...")
model.fit(x_train, y_train, epochs=3)

# 5. TEST IT
print("\nTesting the AI's intelligence:")
model.evaluate(x_test, y_test)

# 6. SAVE YOUR AI
model.save('my_first_ai_model.h5')
print("\nSuccess! Your AI is saved as 'my_first_ai_model.h5'")