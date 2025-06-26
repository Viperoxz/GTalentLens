FROM python:3.11-slim

WORKDIR /app

# Cài gói hệ thống (nếu dùng fitz hoặc các package cần libmagic...)
RUN apt-get update && apt-get install -y \
    build-essential \
    poppler-utils \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["rq", "worker", "cv_tasks", "--path", "src"]