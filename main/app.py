from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import json
from utils import generate_new_filename, list_models
from model_utils import predict_image

app = Flask(__name__, static_folder='../resources/static', template_folder='../resources/templates')
app.config['UPLOAD_FOLDER'] = os.path.join(app.static_folder, 'uploads')
app.config['MODEL_FOLDER'] = os.path.join(app.static_folder, 'models')
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

if not os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], 'metadata.json')):
    with open(os.path.join(app.config['UPLOAD_FOLDER'], 'metadata.json'), 'w') as f:
        json.dump({}, f)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def save_metadata(filename, model_name):
    with open(os.path.join(app.config['UPLOAD_FOLDER'], 'metadata.json'), 'r') as f:
        metadata = json.load(f)
    metadata[filename] = model_name
    with open(os.path.join(app.config['UPLOAD_FOLDER'], 'metadata.json'), 'w') as f:
        json.dump(metadata, f)

def get_metadata(filename):
    with open(os.path.join(app.config['UPLOAD_FOLDER'], 'metadata.json'), 'r') as f:
        metadata = json.load(f)
    return metadata.get(filename, 'modelo1')  # Default model

@app.route('/', methods=['GET', 'POST'])
def index():
    models = list_models(app.config['MODEL_FOLDER'])
    
    if not models:
        return render_template('index.html', models=models, message="No hay modelos cargados.")
    
    selected_model = models[0] if models else None  # Valor predeterminado
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        if file and allowed_file(file.filename):
            new_filename = generate_new_filename(app.config['UPLOAD_FOLDER'], file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
            file.save(file_path)
            
            # Obtener el valor del modelo seleccionado
            selected_model = request.form.get('model', selected_model)  # valor predeterminado
            
            # Guardar metadata
            save_metadata(new_filename, selected_model)
            
            redirect_url = url_for('uploaded_file', filename=new_filename, model=selected_model)
            return jsonify({'redirect_url': redirect_url})

    # Listar archivos en la carpeta de uploads
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    files = [f for f in files if allowed_file(f)]
    return render_template('index.html', files=files, models=models, selected_model=selected_model)


# Mostrar imagen y resultados de la predicción
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    # Obtener el modelo desde los metadatos almacenados
    model_name = get_metadata(filename)
    model_path = os.path.join(app.config['MODEL_FOLDER'], model_name)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    # Realiza la predicción utilizando el modelo y el archivo
    predictions, confidence = predict_image(model_path, file_path)
    
    # Renderiza la plantilla con los resultados de la predicción
    return render_template('show_image.html', filename=filename, predictions=predictions, confidence=confidence, model_name=model_name)

# Eliminar imagen y su metadata
@app.route('/delete_image', methods=['POST'])
def delete_image():
    data = request.get_json()
    filename = data.get('filename')
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    metadata_path = os.path.join(app.config['UPLOAD_FOLDER'], 'metadata.json')

    # Eliminar archivo de imagen
    if os.path.exists(file_path):
        os.remove(file_path)

    # Eliminar metadata
    if os.path.exists(metadata_path):
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
        if filename in metadata:
            del metadata[filename]
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f)

    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=False)
