FROM python:3.12-slim

# 환경 변수 설정
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# 종속성 파일 복사 및 설치 (레이어 캐시 최적화)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 소스 코드 전체 복사
COPY . .

# 보안을 위한 비루트 사용자(appuser) 생성 및 작업 디렉터리 권한 부여
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

USER appuser

# Cloud Run 기본 포트(8080) 및 동적 $PORT 바인딩
CMD exec uvicorn main:app --host 0.0.0.0 --port ${PORT:-8080}

