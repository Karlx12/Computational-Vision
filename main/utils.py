import os


path=r"./../resources/static/uploads/"
def check_file_exists(filename):
    
    return os.path.isfile(path+filename)

def generate_new_filename(filename):
    
    base_name, extension = os.path.splitext(filename)
    counter = 1
    new_filename = filename

    while check_file_exists(new_filename):
        new_filename = f"{base_name} ({counter}){extension}"
        counter += 1

    return new_filename