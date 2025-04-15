# Използваме лек Python образ
FROM python:3.10-slim

# Инсталираме LibreOffice
RUN apt-get update && apt-get install -y libreoffice curl && apt-get clean

# Създаваме работна директория в контейнера
WORKDIR /app

# Копираме dependencies и ги инсталираме
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копираме самото приложение
COPY app.py .

# Създаваме папка за uploads
RUN mkdir -p uploads

# Експортираме порт (Render ще използва $PORT автоматично)
ENV PORT 10000

# Стартираме Flask приложението
CMD ["python", "app.py"]
