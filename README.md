```markdown
# 📄 DOCX to PDF Conversion API

This is a lightweight Python REST API built with **Flask**, designed to convert `.docx` files to PDF using **LibreOffice in headless mode**.  
The service is containerized with **Docker** and deployed for free via **Render.com**.

---

## 🌐 Live Deployment (Render)

The API is fully deployed using a **Dockerized container** on [Render.com](https://render.com/) using the following configuration:

```yaml
# render.yaml
services:
  - type: web
    name: docx-to-pdf-api
    env: docker
    plan: free
```

No build or start commands are needed — Render will automatically detect and build the Docker container.

---

## 🚀 Features

- Convert `.docx` files to `.pdf` using LibreOffice
- RESTful interface (simple POST request)
- Stateless & ephemeral
- Automatically deletes files after conversion
- Works with Postman, ServiceNow, and any REST client
- No external libraries like Microsoft Word required

---

## 📁 Project Structure

```
docx-to-pdf-api/
├── app.py             # Flask application
├── Dockerfile         # Docker container setup
├── requirements.txt   # Python dependencies
├── render.yaml        # Render.com deployment config
└── uploads/           # Temporary storage (automatically cleaned up)
```

---

## ⚙️ API Endpoint

### `POST /convert/docx/to/pdf`

- **Content-Type**: `application/octet-stream`
- **Body**: Raw binary of a `.docx` file
- **Returns**: PDF as a stream (`application/pdf`)

---

## 🧪 Example Usage (Postman)

### Headers:
```http
Content-Type: application/octet-stream
```

### Body:
Upload your `.docx` file in "binary" mode.

### Sample Response:
Returns the PDF as a downloadable file.

---

## 🧰 Deployment Instructions (Render + Docker)

### 1. 🐙 Push to GitHub

Ensure your repo (like https://github.com/ServiceNow-Tsvetomir-PDI-Lab/docx-to-pdf-api) contains:

- `app.py`
- `Dockerfile`
- `render.yaml`
- `requirements.txt`

### 2. 🌐 Connect to Render

1. Go to [Render.com](https://render.com/)
2. Click **"New Web Service"**
3. Choose **"From a GitHub repo"**
4. Select your repo
5. Render will auto-detect the `Dockerfile` and build the image
6. After deployment, you’ll receive a public HTTPS URL like:
   ```
   https://docx-to-pdf-api.onrender.com/convert/docx/to/pdf
   ```

---

## 🐳 Dockerfile Overview

```Dockerfile
FROM python:3.10-slim

RUN apt-get update && \
    apt-get install -y libreoffice && \
    apt-get clean

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]
```

> 📦 Installs LibreOffice in headless mode and runs the Flask server.

---

## 🧠 Python App Summary (`app.py`)

- Accepts raw `.docx` files via POST
- Saves them to disk temporarily
- Converts using LibreOffice:
  ```bash
  libreoffice --headless --convert-to pdf ...
  ```
- Deletes temporary files after conversion
- Returns the PDF stream to the client

---

## 🔐 Security & Data Privacy
```markdown

This API is designed with privacy and security in mind. By default:

- ✅ All uploaded `.docx` files are processed **in-memory** and stored **only temporarily** in a private `/uploads` directory within the container.
- ✅ The converted `.pdf` file is immediately returned in the HTTP response and **never stored permanently** on the server.
- ✅ After processing, both the input and output files are securely deleted using Python’s `os.remove()` function.
- ✅ No file names, content, or metadata are logged or retained beyond the request lifecycle.

This behavior ensures full confidentiality of any sensitive documents processed via the API.

```

---
