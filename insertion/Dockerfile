베이스 이미지 설정 (가벼운 파이썬 3.10 슬림 버전)

FROM python:3.10-slim

작업 디렉토리 설정

WORKDIR /app

패키지 목록 복사 및 설치

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

애플리케이션 코드 전체 복사

COPY . .

포트 노출 (Cloud Run 기본 포트)

EXPOSE 8080

gunicorn을 사용하여 Flask 애플리케이션 실행 (운영 환경 권장)

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
