from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from werkzeug.utils import secure_filename

load_dotenv()

from .models import TestPlan, ScriptRequest, ScriptResponse
from .utils import save_upload_file
from .ingestion import ingest_docs
from .rag_agent import generate_test_cases, generate_selenium_script

app = Flask(__name__)

# Paths
DOCS_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/docs"))
os.makedirs(DOCS_PATH, exist_ok=True)

@app.route("/upload", methods=["POST"])
def upload_files():
    if 'files' not in request.files:
        return jsonify({"error": "No files part"}), 400
    
    files = request.files.getlist('files')
    saved_files = []
    
    for file in files:
        if file.filename == '':
            continue
        
        # We need to wrap the file object to match what save_upload_file expects or modify save_upload_file
        # save_upload_file expects an object with .filename and .file (like FastAPI UploadFile)
        # Flask FileStorage has .filename and .stream (or can be read directly)
        
        # Let's just save it directly here for simplicity or adapt utils
        filename = secure_filename(file.filename)
        file_path = os.path.join(DOCS_PATH, filename)
        file.save(file_path)
        saved_files.append(filename)
        
    return jsonify({"message": f"Successfully uploaded {len(saved_files)} files.", "files": saved_files})

@app.route("/build-kb", methods=["POST"])
def build_knowledge_base():
    try:
        result = ingest_docs()
        return jsonify({"message": result})
    except Exception as e:
        return jsonify({"detail": str(e)}), 500

@app.route("/generate-tests", methods=["POST"])
def generate_tests_endpoint():
    query = request.args.get('query')
    if not query:
        return jsonify({"error": "Query parameter is required"}), 400
        
    try:
        test_cases = generate_test_cases(query)
        return jsonify(test_cases)
    except Exception as e:
        return jsonify({"detail": str(e)}), 500

@app.route("/generate-script", methods=["POST"])
def generate_script_endpoint():
    data = request.get_json()
    if not data or 'test_case' not in data:
        return jsonify({"error": "Invalid request body"}), 400
        
    try:
        # data['test_case'] is already a dict
        script = generate_selenium_script(data['test_case'])
        return jsonify({"script_code": script})
    except Exception as e:
        return jsonify({"detail": str(e)}), 500

@app.route("/", methods=["GET"])
def root():
    return jsonify({"message": "Autonomous QA Agent API is running (Flask)."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001, debug=True)
