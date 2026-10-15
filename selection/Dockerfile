# Python 3.11 경량화 이미지 사용
FROM python:3.11-slim

# 작업 디렉토리 설정
WORKDIR /app

# 라이브러리 설치 파일 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사 (app.py 기준)
COPY app.py .

# 컨테이너 포트 8080 노출 설정
ENV PORT 8080

# Gunicorn을 사용하여 Flask 앱 실행 (app.py의 app 객체)
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
