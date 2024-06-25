import cv2
from tensorflow.keras.models import load_model
import numpy as np

IMG_WIDTH = 30
IMG_HEIGHT = 30

model = load_model("traffic_sign_classifier.h5")

image = cv2.imread("stop.png")
image = cv2.resize(image, (IMG_WIDTH, IMG_HEIGHT))
image = image.astype("float") / 255.0 

image = np.expand_dims(image, axis=0)
predictions = model.predict(image)
predicted_label = np.argmax(predictions[0])  

print(f"Predicted label: {predicted_label}")
