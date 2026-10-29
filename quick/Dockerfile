# 1. 가볍고 안정적인 공식 파이썬 슬림 이미지 사용
FROM python:3.11-slim

# 표준 출력 버퍼링 비활성화 (로그 즉시 확인용)
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

# 작업 디렉토리 설정
WORKDIR /app

# 2. 의존성 파일 복사 및 설치 (캐시 최적화)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. 소스 코드 복사
COPY . .

# 4. Cloud Run 포트 노출
EXPOSE 8080

# 5. Uvicorn 서버 실행 (Cloud Run 주입 PORT 환경변수 사용)
CMD exec uvicorn main:app --host 0.0.0.0 --port ${PORT}

