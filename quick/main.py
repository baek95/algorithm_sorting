"""
Google Cloud Run 배포용 정렬 시각화 백엔드 서버 (FastAPI)
- 셸 정렬, 퀵 정렬, 병합 정렬 스냅샷 데이터 API 제공
- CORS 설정으로 GAS(Google Apps Script) 및 브라우저 클라이언트 연동 지원
- 헬스체크 및 상세 에러 핸들링
"""

import os
import random
from typing import List, Optional
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from algorithms import run_all_sorts

# FastAPI 인스턴스 초기화
app = FastAPI(
    title="Sorting Algorithm Snapshot Server",
    description="셸 정렬, 퀵 정렬, 병합 정렬의 매 스텝 스냅샷 히스토리를 반환하는 Cloud Run 백엔드 API",
    version="1.0.0"
)

# CORS 설정: GAS(Google Apps Script) 웹 앱 및 외부 브라우저 호출 허용
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 오리진 허용 (GAS iframe / 웹 브라우저 호환)
    allow_credentials=True,
    allow_methods=["*"],  # GET, POST, OPTIONS 등 전체 허용
    allow_headers=["*"],
)


# 요청 데이터 모델 정의
class SortRequest(BaseModel):
    array: Optional[List[int]] = Field(
        default=None,
        description="정렬할 정수 배열. 제공되지 않으면 size 크기의 무작위 배열을 생성합니다."
    )
    size: Optional[int] = Field(
        default=10,
        ge=2,
        le=50,
        description="랜덤 배열 생성 시 크기 (최소 2, 최대 50 - 시각화 가독성 고려)"
    )


# 루트 엔드포인트
@app.get("/", summary="서버 기본 정보 및 상태 확인")
def root():
    return {
        "status": "online",
        "service": "Sorting Algorithm Snapshot Server",
        "version": "1.0.0",
        "endpoints": {
            "health_check": "GET /health",
            "sort_post": "POST /api/sort",
            "sort_get_sample": "GET /api/sort"
        }
    }


# 헬스체크 엔드포인트 (클라이언트 상태 뱃지 확인용)
@app.get("/health", summary="서버 헬스체크")
def health_check():
    return {
        "status": "healthy",
        "message": "서버가 정상적으로 동작 중입니다."
    }


# 정렬 스냅샷 API (POST)
@app.post("/api/sort", summary="3대 정렬 알고리즘 스냅샷 히스토리 생성 (POST)")
def api_sort_post(request: SortRequest):
    try:
        # 입력 배열 처리
        if request.array is not None:
            input_array = request.array
            # 유효성 검사 1: 빈 배열 검사
            if len(input_array) == 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="입력 배열이 비어 있습니다. 2개 이상의 정수를 입력해주세요."
                )
            # 유효성 검사 2: 너무 큰 배열 크기 제한 (브라우저 시각화 성능 보호)
            if len(input_array) > 50:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"입력 배열 크기({len(input_array)})가 너무 큽니다. 시각화를 위해 50개 이하로 입력해주세요."
                )
        else:
            # 기본 무작위 배열 생성 (1 ~ 100 사이의 중복 없는 정수)
            size = request.size or 10
            input_array = random.sample(range(5, 100), size)

        # 3가지 알고리즘 스냅샷 실행 및 히스토리 추출
        result = run_all_sorts(input_array)
        return {
            "success": True,
            "data": result
        }

    except HTTPException:
        raise
    except Exception as e:
        # 예상치 못한 내부 서버 오류 시 정확한 에러 정보 기술
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"알고리즘 스냅샷 연산 중 내부 오류가 발생했습니다: {str(e)}"
        )


# 정렬 스냅샷 API (GET - 브라우저 URL 직접 테스트용 샘플)
@app.get("/api/sort", summary="샘플 정렬 스냅샷 히스토리 조회 (GET)")
def api_sort_get(size: int = 10):
    if size < 2 or size > 50:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="size는 2 이상 50 이하의 값이어야 합니다."
        )
    sample_array = random.sample(range(5, 100), size)
    result = run_all_sorts(sample_array)
    return {
        "success": True,
        "data": result
    }


if __name__ == "__main__":
    import uvicorn
    # Cloud Run은 환경 변수 PORT를 주입하므로 이를 읽어 바인딩합니다 (기본 8080)
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)

