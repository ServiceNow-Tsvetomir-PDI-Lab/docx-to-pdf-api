# Working - This is a simple Flask application that converts DOCX files to PDF format.
# from flask import Flask, request, send_file
# from docx2pdf import convert
# import os
# import uuid
# from werkzeug.datastructures import FileStorage
# import io

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
#     docx_path = os.path.join(UPLOAD_FOLDER, f"{file_id}.docx")
#     pdf_path = os.path.join(UPLOAD_FOLDER, f"{file_id}.pdf")

#     with open(docx_path, 'wb') as f:
#         f.write(request.data)

#     try:
#         convert(docx_path, pdf_path)
#         return send_file(pdf_path, mimetype='application/pdf')
#     except Exception as e:
#         return {"error": str(e)}, 500
#     finally:
#         if os.path.exists(docx_path):
#             os.remove(docx_path)
#         if os.path.exists(pdf_path):
#             os.remove(pdf_path)

# if __name__ == '__main__':
#     app.run(port=5000, debug=True)





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
#     docx_path = os.path.join(UPLOAD_FOLDER, f"{file_id}.docx")
#     pdf_path = os.path.join(UPLOAD_FOLDER, f"{file_id}.pdf")

#     try:
#         # Записваме получения DOCX файл
#         with open(docx_path, 'wb') as f:
#             f.write(request.data)

#         # Конвертираме чрез unoconv
#         result = subprocess.run(["unoconv", "-f", "pdf", "-o", pdf_path, docx_path],
#                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE)

#         if result.returncode != 0:
#             return {"error": result.stderr.decode('utf-8')}, 500

#         return send_file(pdf_path, mimetype='application/pdf', as_attachment=True, download_name="converted.pdf")

#     except Exception as e:
#         return {"error": str(e)}, 500

#     finally:
#         if os.path.exists(docx_path):
#             os.remove(docx_path)
#         if os.path.exists(pdf_path):
#             os.remove(pdf_path)



# if __name__ == '__main__':
#     port = int(os.environ.get('PORT', 5000))
#     print(f"🚀 Flask API is running at http://0.0.0.0:{port}/convert/docx/to/pdf")
#     app.run(host='0.0.0.0', port=port)



from flask import Flask, request, send_file
import os
import uuid
import subprocess

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/convert/docx/to/pdf', methods=['POST'])
def convert_docx_to_pdf():
    if request.content_type != 'application/octet-stream':
        return {"error": "Invalid Content-Type. Use application/octet-stream"}, 400

    if not request.data:
        return {"error": "No file data received"}, 400

    file_id = str(uuid.uuid4())
    docx_path = os.path.join(UPLOAD_FOLDER, f"{file_id}.docx")
    output_dir = os.path.abspath(UPLOAD_FOLDER)

    try:
        # Save the uploaded DOCX
        with open(docx_path, 'wb') as f:
            f.write(request.data)

        # Use LibreOffice in headless mode to convert
        result = subprocess.run([
            "soffice", "--headless", "--convert-to", "pdf", "--outdir", output_dir, docx_path
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if result.returncode != 0:
            return {"error": result.stderr.decode('utf-8')}, 500

        pdf_path = docx_path.replace('.docx', '.pdf')
        return send_file(pdf_path, mimetype='application/pdf', as_attachment=True, download_name="converted.pdf")

    except Exception as e:
        return {"error": str(e)}, 500

    finally:
        if os.path.exists(docx_path):
            os.remove(docx_path)
        if os.path.exists(pdf_path):
            os.remove(pdf_path)

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 Running on http://0.0.0.0:{port}")
    app.run(host="0.0.0.0", port=port)
