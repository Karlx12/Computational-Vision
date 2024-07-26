import os

def check_file_exists(path,filename):
    return os.path.isfile(os.path.join(path, filename))

def generate_new_filename(path, filename):
    base_name, extension = os.path.splitext(filename)
    counter = 1
    new_filename = filename

    while check_file_exists(path,new_filename):
        new_filename = f"{base_name} ({counter}){extension}"
        counter += 1

    return new_filename

def list_models(path):
    models = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and f.endswith('.h5')]
    return models
