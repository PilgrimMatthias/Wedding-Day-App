FROM python:3.12-slim

# Prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Flask app entry
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

EXPOSE 5000

# Production WSGI server
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "app:app"]
