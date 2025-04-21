from flask import Flask, request, send_file
from flasgger import Swagger, swag_from
import os
import uuid
import subprocess

app = Flask(__name__)
swagger = Swagger(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route('/convert/docx/to/pdf', methods=['POST'])
@swag_from({
    'tags': ['Conversion'],
    'summary': 'Convert DOCX to PDF',
    'description': 'Accepts a DOCX file and returns a converted PDF file.',
    'consumes': ['application/octet-stream'],
    'produces': ['application/pdf'],
    'parameters': [
        {
            'name': 'file',
            'in': 'body',
            'required': True,
            'description': 'The .docx file to convert',
            'schema': {
                'type': 'string',
                'format': 'binary'
            }
        }
    ],
    'responses': {
        200: {
            'description': 'PDF file generated successfully'
        },
        400: {
            'description': 'Invalid input or missing file'
        },
        500: {
            'description': 'Internal error or conversion failed'
        }
    }
})
def convert_docx_to_pdf():
    if request.content_type != 'application/octet-stream':
        return {"error": "Invalid Content-Type. Use application/octet-stream"}, 400

    if not request.data:
        return {"error": "No file data received"}, 400

    file_id = str(uuid.uuid4())
    docx_filename = f"{file_id}.docx"
    pdf_filename = f"{file_id}.pdf"
    docx_path = os.path.join(UPLOAD_FOLDER, docx_filename)
    pdf_path = os.path.join(UPLOAD_FOLDER, pdf_filename)

    try:
        with open(docx_path, 'wb') as f:
            f.write(request.data)

        result = subprocess.run([
            "libreoffice", "--headless", "--convert-to", "pdf", "--outdir", UPLOAD_FOLDER, docx_path
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if result.returncode != 0:
            return {"error": result.stderr.decode('utf-8')}, 500

        if os.path.exists(pdf_path):
            return send_file(pdf_path, mimetype='application/pdf', as_attachment=True, download_name="converted.pdf")
        else:
            return {"error": "PDF not found after conversion"}, 500

    except Exception as e:
        return {"error": str(e)}, 500

    finally:
        if os.path.exists(docx_path):
            os.remove(docx_path)
        if os.path.exists(pdf_path):
            os.remove(pdf_path)


@app.route('/')
def index():
    return "✅ DOCX to PDF Conversion API is running. Visit /docs for Swagger UI."


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

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

