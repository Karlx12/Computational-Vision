import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np
import os

# Cargar el modelo
model_path = os.path.join(os.path.dirname(__file__), 'models', 'cotton_vgg16.h5')
model = load_model(model_path)

# Función para preprocesar la imagen
def preprocess_image(image_path, target_size=(224, 224)):
    img = load_img(image_path, target_size=target_size)
    img_array = img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0
    return img_array

# Función para hacer la predicción
def predict_image(image_path):
    img_array = preprocess_image(image_path)
    predictions = model.predict(img_array)
    predicted_class = np.argmax(predictions, axis=1)
    return 'Sana' if predicted_class[0] == 3 else 'Enferma'
