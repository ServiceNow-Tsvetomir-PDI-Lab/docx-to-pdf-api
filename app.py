# from flask import Flask, request, send_file
# import os
# import uuid
# import subprocess

# app = Flask(__name__)
# UPLOAD_FOLDER = "uploads"
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# @app.route('/convert/docx/to/pdf', methods=['POST'])
# def convert_docx_to_pdf():
#     if request.content_type != 'application/octet-stream':
#         return {"error": "Invalid Content-Type. Use application/octet-stream"}, 400

#     if not request.data:
#         return {"error": "No file data received"}, 400

#     file_id = str(uuid.uuid4())
#     docx_filename = f"{file_id}.docx"
#     pdf_filename = f"{file_id}.pdf"
#     docx_path = os.path.join(UPLOAD_FOLDER, docx_filename)
#     pdf_path = os.path.join(UPLOAD_FOLDER, pdf_filename)

#     try:
#         # Save DOCX to file
#         with open(docx_path, 'wb') as f:
#             f.write(request.data)

#         # Convert using LibreOffice headless
#         result = subprocess.run([
#             "libreoffice", "--headless", "--convert-to", "pdf", "--outdir", UPLOAD_FOLDER, docx_path
#         ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

#         # Optional: print logs to help with debugging
#         print("STDOUT:", result.stdout.decode())
#         print("STDERR:", result.stderr.decode())

#         if result.returncode != 0:
#             return {"error": result.stderr.decode('utf-8')}, 500

#         # Return PDF Demo Testing
#         if os.path.exists(pdf_path):
#             return send_file(pdf_path, mimetype='application/pdf', as_attachment=True, download_name="converted.pdf")
#         else:
#             return {"error": "PDF not found after conversion"}, 500

#     except Exception as e:
#         return {"error": str(e)}, 500

#     finally:
#         if os.path.exists(docx_path):
#             os.remove(docx_path)
#         if os.path.exists(pdf_path):
#             os.remove(pdf_path)

# if __name__ == '__main__':
#     port = int(os.environ.get("PORT", 5000))
#     app.run(host='0.0.0.0', port=port)



from flask import Flask, request, send_file, jsonify
from flasgger import Swagger, swag_from
import os
import uuid
import subprocess

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
DOWNLOAD_FOLDER = "downloads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# Swagger configuration
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/apispec_1.json',
            "rule_filter": lambda rule: rule.rule.startswith('/convert/docx/to/pdf/swagger'),
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs/"
}

swagger_template = {
    "info": {
        "title": "DOCX to PDF Converter API",
        "description": """Use this endpoint to upload a DOCX file and receive a downloadable PDF link.

⚠️ Copy the download_url from the response and paste it in a new browser tab to download the file.""",
        "version": "1.0.0",
        "contact": {
            "name": "Your Name",
            "email": "your.email@example.com",
            "url": "https://yourcompany.com"
        }
    },
    "host": "localhost:5000",
    "basePath": "/",
    "schemes": ["http"]
}

swagger = Swagger(app, config=swagger_config, template=swagger_template)

@app.route('/convert/docx/to/pdf', methods=['POST'])
def convert_docx_to_pdf_servicenow():
    file_id = str(uuid.uuid4())
    docx_path = os.path.join(UPLOAD_FOLDER, f"{file_id}.docx")
    pdf_path = os.path.join(DOWNLOAD_FOLDER, f"{file_id}.pdf")

    try:
        if not request.data:
            return {"error": "No file data received"}, 400

        with open(docx_path, 'wb') as f:
            f.write(request.data)

        result = subprocess.run([
            "soffice", "--headless", "--convert-to", "pdf", "--outdir", DOWNLOAD_FOLDER, docx_path
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if result.returncode != 0:
            return {"error": result.stderr.decode('utf-8')}, 500

        return send_file(pdf_path, mimetype='application/pdf', as_attachment=True, download_name="converted.pdf")

    finally:
        if os.path.exists(docx_path):
            os.remove(docx_path)
        if os.path.exists(pdf_path):
            os.remove(pdf_path)

@app.route('/convert/docx/to/pdf/swagger', methods=['POST'])
@swag_from({
    'consumes': ['multipart/form-data'],
    'parameters': [
        {
            'name': 'file',
            'in': 'formData',
            'type': 'file',
            'required': True,
            'description': 'Upload a DOCX file to convert to PDF'
        }
    ],
    'responses': {
        200: {
            'description': 'Returns a download URL as JSON.',
            'examples': {
                'application/json': {
                    "message": "PDF generated successfully",
                    "download_url": "http://127.0.0.1:5000/downloads/<uuid>.pdf"
                }
            }
        },
        400: {'description': 'Missing file'},
        500: {'description': 'Conversion failed'}
    }
})
def convert_docx_to_pdf_swagger():
    file_id = str(uuid.uuid4())
    docx_path = os.path.join(UPLOAD_FOLDER, f"{file_id}.docx")
    pdf_filename = f"{file_id}.pdf"
    pdf_path = os.path.join(DOWNLOAD_FOLDER, pdf_filename)

    try:
        if 'file' not in request.files:
            return {"error": "File is required"}, 400

        file = request.files['file']
        file.save(docx_path)

        result = subprocess.run([
            "soffice", "--headless", "--convert-to", "pdf", "--outdir", DOWNLOAD_FOLDER, docx_path
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if result.returncode != 0:
            return {"error": result.stderr.decode('utf-8')}, 500

        if os.path.exists(pdf_path):
            return jsonify({
                "message": "PDF generated successfully",
                "download_url": f"{request.host_url}downloads/{pdf_filename}"
            })
        else:
            return {"error": "PDF file not found after conversion"}, 500
    finally:
        if os.path.exists(docx_path):
            os.remove(docx_path)

@app.route('/downloads/<filename>', methods=['GET'])
def download_file(filename):
    file_path = os.path.join(DOWNLOAD_FOLDER, filename)
    if os.path.exists(file_path):
        return send_file(file_path, mimetype='application/pdf', as_attachment=True)
    else:
        return {"error": "File not found"}, 404

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
