import os
import shutil

def save_upload_file(upload_file, destination_folder):
    try:
        os.makedirs(destination_folder, exist_ok=True)
        file_path = os.path.join(destination_folder, upload_file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
        return file_path
    except Exception as e:
        print(f"Error saving file: {e}")
        return None

def read_file_content(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        return ""
