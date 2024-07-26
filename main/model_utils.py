
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np
import os

# Cargar el modelo


class_indices = { 'Pulgones (Aphids)': 0, 'Gusanos (Army worm)': 1, 'Plaga Bacteriana (Bacterial Blight)': 2, 'Sana': 3, 'Hongos (Powdery Mildew)': 4, 'Manchas (Target spot)': 5 }
labels = {v: k for k, v in class_indices.items()}

# Función para preprocesar la imagen
def preprocess_image(image_path, target_size=(224, 224)):
    img = load_img(image_path, target_size=target_size)
    img_array = img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0
    return img_array

# Función para hacer la predicción
def predict_image(model_path,image_path):
    print("Cargando Predicción............")
    img_array = preprocess_image(image_path)
    
    print(model_path)
    model = load_model(model_path)
    
    predictions = model.predict(img_array)
    predicted_class = np.argmax(predictions, axis=1)
    confidence = float (predictions[0][predicted_class])

    predicted_label = labels[predicted_class[0]] 
    
    
    if predicted_class[0]!=3:
        predicted_label="enferma con la enfermedad: "+predicted_label        
    return predicted_label, str.format("{:.2%}", confidence)
