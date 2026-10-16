FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# app.py의 app 객체를 실행하도록 설정
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
