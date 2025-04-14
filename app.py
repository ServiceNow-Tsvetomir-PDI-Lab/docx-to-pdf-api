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







# from flask import Flask, request, make_response
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

#         # 🔥 Връщаме PDF ръчно, без Content-Disposition
#         with open(pdf_path, 'rb') as f:
#             pdf_data = f.read()

#         response = make_response(pdf_data)
#         response.headers['Content-Type'] = 'application/pdf'
#         response.headers['Content-Length'] = str(len(pdf_data))
#         response.headers['Content-Disposition'] = 'inline'  # Това показва PDF-а в браузъра вместо да го тегли

#         # ❌ НЕ задаваме Content-Disposition – така няма теглене

#         return response

#     except Exception as e:
#         return {"error": str(e)}, 500

#     finally:
#         if os.path.exists(docx_path):
#             os.remove(docx_path)
#         if os.path.exists(pdf_path):
#             os.remove(pdf_path)

# if __name__ == '__main__':
#     app.run(port=5000, debug=True)




# from flask import Flask, request, make_response, render_template_string
# from docx2pdf import convert
# import os
# import uuid
# import base64

# app = Flask(__name__)
# UPLOAD_FOLDER = "uploads"
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# @app.route('/convert/docx/to/pdf', methods=['POST'])
# def convert_docx_to_pdf():
#     # Проверяваме дали имаме параметър 'view' в URL
#     view_mode = request.args.get('view', 'false').lower() == 'true'
    
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
        
#         with open(pdf_path, 'rb') as f:
#             pdf_data = f.read()
        
#         # За ServiceNow или когато не е указан режим 'view'
#         if not view_mode:
#             response = make_response(pdf_data)
#             response.headers['Content-Type'] = 'application/pdf'
#             return response
        
#         # За режим 'view' - връщаме HTML страница с вграден PDF
#         else:
#             # Кодираме PDF данните в base64
#             pdf_base64 = base64.b64encode(pdf_data).decode('utf-8')
            
#             # HTML шаблон с вграден PDF
#             html_template = """
#             <!DOCTYPE html>
#             <html>
#             <head>
#                 <title>Конвертиран PDF</title>
#                 <style>
#                     body, html {
#                         margin: 0;
#                         padding: 0;
#                         height: 100%;
#                         font-family: Arial, sans-serif;
#                     }
#                     .container {
#                         display: flex;
#                         flex-direction: column;
#                         height: 100vh;
#                     }
#                     .header {
#                         background-color: #f4f4f4;
#                         padding: 10px;
#                         text-align: center;
#                     }
#                     .viewer {
#                         flex: 1;
#                         border: none;
#                     }
#                 </style>
#             </head>
#             <body>
#                 <div class="container">
#                     <div class="header">
#                         <h2>PDF Визуализация</h2>
#                         <p>Вашият документ е успешно конвертиран в PDF формат.</p>
#                     </div>
#                     <iframe class="viewer" src="data:application/pdf;base64,{{ pdf_data }}"></iframe>
#                 </div>
#             </body>
#             </html>
#             """
            
#             # Връщаме HTML страницата
#             return render_template_string(html_template, pdf_data=pdf_base64)

#     except Exception as e:
#         return {"error": str(e)}, 500

#     finally:
#         if os.path.exists(docx_path):
#             os.remove(docx_path)
#         if os.path.exists(pdf_path):
#             os.remove(pdf_path)

# if __name__ == '__main__':
#     app.run(port=5000, debug=True)




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
    pdf_path = os.path.join(UPLOAD_FOLDER, f"{file_id}.pdf")

    try:
        # Записваме получения DOCX файл
        with open(docx_path, 'wb') as f:
            f.write(request.data)

        # Конвертираме чрез unoconv
        result = subprocess.run(["unoconv", "-f", "pdf", "-o", pdf_path, docx_path],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if result.returncode != 0:
            return {"error": result.stderr.decode('utf-8')}, 500

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
    port = int(os.environ.get('PORT', 5000))  # Взима порта от Render
    print(f"🚀 Flask API is running at http://0.0.0.0:{port}/convert/docx/to/pdf")
    app.run(host='0.0.0.0', port=port)



