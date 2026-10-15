import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
# GAS 등 다른 도메인에서의 요청을 허용하기 위해 CORS 설정
CORS(app)

@app.route('/sort', methods=['POST'])
def bubble_sort():
    """
    POST 요청을 받아 버블 정렬을 수행하고 각 단계별 배열 상태를 반환합니다.
    요청 형식: {"array": [5, 2, 9, 1, 5, 6]}
    """
    try:
        data = request.get_json()
        if not data or 'array' not in data:
            return jsonify({"error": "배열 데이터가 없습니다."}), 400
        
        arr = data['array']
        
        # 입력이 리스트인지 확인
        if not isinstance(arr, list):
            return jsonify({"error": "배열 형태가 아닙니다."}), 400

        # 초기 상태 저장
        steps = [list(arr)]
        n = len(arr)
        
        # 버블 정렬 알고리즘 수행
        for i in range(n):
            swapped = False
            for j in range(0, n - i - 1):
                # 앞의 원소가 뒤의 원소보다 크면 스왑
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    # 스왑이 발생할 때마다 현재 배열의 상태를 복사하여 steps에 추가
                    steps.append(list(arr))
                    swapped = True
            
            # 한 번도 스왑이 발생하지 않았다면 이미 정렬된 상태이므로 조기 종료
            if not swapped:
                break
                
        # 최종 결과 반환
        return jsonify({
            "status": "success",
            "original": data['array'],
            "sorted": arr,
            "steps": steps,
            "complexity": {
                "time": "O(n²)",
                "space": "O(1)"
            },
            "message": "정렬이 완료되었습니다."
        }), 200

    except Exception as e:
        return jsonify({"error": str(e), "status": "fail"}), 500

if __name__ == "__main__":
    # Cloud Run 환경에서는 PORT 환경변수를 사용합니다. (기본값 8080)
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=True)
