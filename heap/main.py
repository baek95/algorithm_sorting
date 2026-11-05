import random
import time
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(
    title="Dual Sort Visualizer API",
    description="Heap Sort & Counting Sort Step-by-Step Simulation Engine",
    version="1.0.0"
)

# Enable CORS for Google Apps Script, local frontend, and browser testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class SortCompareRequest(BaseModel):
    size: int = Field(default=30, ge=5, le=200, description="배열 원소 개수 (N)")
    max_val: int = Field(default=100, ge=10, le=500, description="원소 최대값 범위 (K)")
    custom_array: Optional[List[int]] = Field(default=None, description="직접 전달할 배열 (선택사항)")


def generate_heap_sort_steps(initial_arr: List[int]) -> Dict[str, Any]:
    arr = list(initial_arr)
    n = len(arr)
    steps: List[Dict[str, Any]] = []
    comparisons = 0
    swaps = 0
    start_time = time.perf_counter()

    # Step 0: Initial state
    steps.append({
        "step": len(steps),
        "array": list(arr),
        "active": [],
        "sorted": [],
        "action": "init",
        "description": f"초기 원시 배열 로드 (N={n})",
        "comparisons": comparisons,
        "swaps": swaps,
        "progress_pct": 0.0,
        "time_ms": round((time.perf_counter() - start_time) * 1000, 3)
    })

    def sift_down(a: List[int], heap_size: int, root: int, sorted_set: List[int]):
        nonlocal comparisons, swaps
        largest = root
        left = 2 * root + 1
        right = 2 * root + 2

        if left < heap_size:
            comparisons += 1
            if a[left] > a[largest]:
                largest = left

        if right < heap_size:
            comparisons += 1
            if a[right] > a[largest]:
                largest = right

        if largest != root:
            a[root], a[largest] = a[largest], a[root]
            swaps += 1
            steps.append({
                "step": len(steps),
                "array": list(a),
                "active": [root, largest],
                "sorted": list(sorted_set),
                "action": "sift_down",
                "description": f"최대 힙 조정: 노드[{root}] ↔ 자식[{largest}] 값 교환 ({a[root]} ↔ {a[largest]})",
                "comparisons": comparisons,
                "swaps": swaps,
                "progress_pct": round(min(99.0, (len(sorted_set) / n) * 80 + 10), 1),
                "time_ms": round((time.perf_counter() - start_time) * 1000, 3)
            })
            sift_down(a, heap_size, largest, sorted_set)

    # 1. Build Max-Heap
    for i in range(n // 2 - 1, -1, -1):
        sift_down(arr, n, i, [])

    steps.append({
        "step": len(steps),
        "array": list(arr),
        "active": [0],
        "sorted": [],
        "action": "heap_built",
        "description": "최대 힙(Max-Heap) 트리 구조 생성 완료 (루트 = 최대값)",
        "comparisons": comparisons,
        "swaps": swaps,
        "progress_pct": 20.0,
        "time_ms": round((time.perf_counter() - start_time) * 1000, 3)
    })

    # 2. Extract Max Elements
    sorted_indices: List[int] = []
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        swaps += 1
        sorted_indices.append(i)
        
        pct = round(20.0 + (len(sorted_indices) / n) * 79.0, 1)
        steps.append({
            "step": len(steps),
            "array": list(arr),
            "active": [0, i],
            "sorted": list(sorted_indices),
            "action": "extract_root",
            "description": f"루트 최댓값({arr[i]})을 끝 인덱스[{i}]로 교환 후 힙 크기 축소",
            "comparisons": comparisons,
            "swaps": swaps,
            "progress_pct": pct,
            "time_ms": round((time.perf_counter() - start_time) * 1000, 3)
        })
        sift_down(arr, i, 0, sorted_indices)

    sorted_indices.append(0)
    total_time_ms = round((time.perf_counter() - start_time) * 1000, 3)

    steps.append({
        "step": len(steps),
        "array": list(arr),
        "active": [],
        "sorted": list(range(n)),
        "action": "done",
        "description": "힙 정렬(Heap Sort) 완료: 시간복잡도 O(N log N)",
        "comparisons": comparisons,
        "swaps": swaps,
        "progress_pct": 100.0,
        "time_ms": total_time_ms
    })

    return {
        "metadata": {
            "algorithm": "Heap Sort",
            "time_complexity": "O(N log N)",
            "space_complexity": "O(1)",
            "total_comparisons": comparisons,
            "total_swaps": swaps,
            "total_steps": len(steps),
            "total_time_ms": total_time_ms,
            "n": n
        },
        "steps": steps
    }


def generate_counting_sort_steps(initial_arr: List[int], max_val: int) -> Dict[str, Any]:
    arr = list(initial_arr)
    n = len(arr)
    k = max(max(arr), max_val)
    steps: List[Dict[str, Any]] = []
    operations = 0
    start_time = time.perf_counter()

    count = [0] * (k + 1)
    output = [0] * n
    sorted_indices: List[int] = []

    # Step 0: Initial state
    steps.append({
        "step": len(steps),
        "array": list(arr),
        "output_array": list(output),
        "count_matrix": count[:min(k + 1, 30)],
        "active": [],
        "sorted": [],
        "phase": "init",
        "action": "init",
        "description": f"도수 정렬 초기화 (N={n}, 값 범위 K={k})",
        "operations": operations,
        "progress_pct": 0.0,
        "time_ms": round((time.perf_counter() - start_time) * 1000, 3)
    })

    # Phase 1: Frequency count
    for i, val in enumerate(arr):
        count[val] += 1
        operations += 1
        pct = round((i + 1) / n * 30.0, 1)
        steps.append({
            "step": len(steps),
            "array": list(arr),
            "output_array": list(output),
            "count_matrix": count[:min(k + 1, 30)],
            "active": [i],
            "sorted": [],
            "phase": "count",
            "action": "count",
            "description": f"빈도 계산: arr[{i}]={val} 발견 ➔ Count[{val}] = {count[val]}",
            "operations": operations,
            "progress_pct": pct,
            "time_ms": round((time.perf_counter() - start_time) * 1000, 3)
        })

    # Phase 2: Cumulative Sum
    for i in range(1, k + 1):
        count[i] += count[i - 1]
        operations += 1

    steps.append({
        "step": len(steps),
        "array": list(arr),
        "output_array": list(output),
        "count_matrix": count[:min(k + 1, 30)],
        "active": [],
        "sorted": [],
        "phase": "accumulate",
        "action": "accumulate",
        "description": f"도수 누적 합 계산 완료: 각 원소가 배치될 마지막 인덱스 결정 (0~{k})",
        "operations": operations,
        "progress_pct": 50.0,
        "time_ms": round((time.perf_counter() - start_time) * 1000, 3)
    })

    # Phase 3: Placement into output array (stable backwards loop)
    for i in range(n - 1, -1, -1):
        val = arr[i]
        count[val] -= 1
        pos = count[val]
        output[pos] = val
        sorted_indices.append(pos)
        operations += 1
        
        placed_ratio = len(sorted_indices) / n
        pct = round(50.0 + placed_ratio * 49.0, 1)
        steps.append({
            "step": len(steps),
            "array": list(arr),
            "output_array": list(output),
            "count_matrix": count[:min(k + 1, 30)],
            "active": [pos],
            "sorted": list(sorted_indices),
            "phase": "place",
            "action": "place",
            "description": f"안정 정렬 배치: arr[{i}]={val} ➔ Output[{pos}] 기입 (Count[{val}] 차감)",
            "operations": operations,
            "progress_pct": pct,
            "time_ms": round((time.perf_counter() - start_time) * 1000, 3)
        })

    total_time_ms = round((time.perf_counter() - start_time) * 1000, 3)
    steps.append({
        "step": len(steps),
        "array": list(output),
        "output_array": list(output),
        "count_matrix": count[:min(k + 1, 30)],
        "active": [],
        "sorted": list(range(n)),
        "phase": "done",
        "action": "done",
        "description": f"도수 정렬(Counting Sort) 완료: 시간복잡도 O(N + K) (비교 연산 0회)",
        "operations": operations,
        "progress_pct": 100.0,
        "time_ms": total_time_ms
    })

    return {
        "metadata": {
            "algorithm": "Counting Sort",
            "time_complexity": "O(N + K)",
            "space_complexity": "O(K)",
            "total_operations": operations,
            "total_steps": len(steps),
            "total_time_ms": total_time_ms,
            "n": n,
            "k": k
        },
        "steps": steps
    }


@app.get("/health")
def health_check():
    return {
        "status": "online",
        "service": "Dual Sort Visualizer (FastAPI Engine)",
        "timestamp": time.time(),
        "algorithms": ["Heap Sort", "Counting Sort"]
    }


@app.post("/api/sort/compare")
def compare_sorting_algorithms(req: SortCompareRequest):
    if req.custom_array and len(req.custom_array) > 0:
        base_array = req.custom_array
    else:
        # Generate uniform random array
        base_array = [random.randint(5, req.max_val) for _ in range(req.size)]

    heap_res = generate_heap_sort_steps(base_array)
    counting_res = generate_counting_sort_steps(base_array, req.max_val)

    return {
        "success": True,
        "size": len(base_array),
        "max_val": req.max_val,
        "initial_array": base_array,
        "heap_sort": heap_res,
        "counting_sort": counting_res
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

