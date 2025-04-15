# Use a lightweight official Python image
FROM python:3.10-slim

# Install LibreOffice and other necessary tools
RUN apt-get update && apt-get install -y libreoffice curl && apt-get clean

# Set the working directory inside the container
WORKDIR /app

# Copy Python dependencies and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the main application file
COPY app.py .

# Create a directory for temporary uploads
RUN mkdir -p uploads

# Expose the port (Render will use the PORT environment variable automatically)
ENV PORT 10000

# Start the Flask application
CMD ["python", "app.py"]
