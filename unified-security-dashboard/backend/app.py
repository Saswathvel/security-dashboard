from flask import Flask, request, jsonify
from scanners.scan_utils import scan_project
from flask_cors import CORS
import json
import uuid
import os, tempfile, shutil, subprocess, traceback
from scanners.run_codeql import run_codeql_scan
from scanners.run_gitleaks import run_gitleaks_scan
from scanners.run_syft import generate_sbom
from scanners.run_osv import run_osv_scan

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Demo users
users = {
    "admin": "admin123",
    "saswath": "vel123"
}

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Missing credentials"}), 400

    if users.get(username) == password:
        return jsonify({"success": True, "token": "demo-token"})
    else:
        return jsonify({"error": "Invalid username or password"}), 401


@app.route('/api/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    save_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(save_path)

    return jsonify({"status": "uploaded", "filename": file.filename})


@app.route("/api/scan", methods=["POST"])
def scan():
    data = request.get_json()
    input_type = data.get("type")
    repo_url = data.get("value")

    result = scan_project(input_type, repo_url)
    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]

    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True, port=5001)
