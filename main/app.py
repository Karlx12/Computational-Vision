from flask import Flask, render_template, request, redirect, url_for
import os
from utils import generate_new_filename, list_models
from model_utils import predict_image

app = Flask(__name__, static_folder='../resources/static', template_folder='../resources/templates')
app.config['UPLOAD_FOLDER'] = os.path.join(app.static_folder, 'uploads')
app.config['MODEL_FOLDER'] = os.path.join(app.static_folder, 'models')
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/', methods=['GET', 'POST'])
def index():
    models = list_models(app.config['MODEL_FOLDER'])
    
    if not models:
        return render_template('index.html', models=models, message="No hay modelos cargados.")
    
    selected_model = models[0] if models else None  # Valor predeterminado
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            new_filename = generate_new_filename(app.config['UPLOAD_FOLDER'], file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
            file.save(file_path)
            
            # Obtener el valor del modelo seleccionado
            selected_model = request.form.get('model', selected_model)  # valor predeterminado
            
            return redirect(url_for('uploaded_file', filename=new_filename, model=selected_model))

    # Listar archivos en la carpeta de uploads
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    files = [f for f in files if allowed_file(f)]
    return render_template('index.html', files=files, models=models, selected_model=selected_model)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    # Obtener el modelo desde los parámetros de consulta de la URL
    model = request.args.get('model', 'modelo1')  # Valor predeterminado
    model = os.path.join(app.config['MODEL_FOLDER'],model)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    
    # Realiza la predicción utilizando el modelo y el archivo
    predictions, confidence = predict_image(model, file_path)
    print("Predicciones............")
    
    # Renderiza la plantilla con los resultados de la predicción
    return render_template('show_image.html', filename=filename, predictions=predictions, confidence=confidence)

if __name__ == '__main__':
    app.run(debug=False)
