# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app) # GAS 등 외부 도메인에서의 요청을 허용

@app.route('/selection-sort', methods=['POST'])
def selection_sort():
    try:
        # 클라이언트(GAS)로부터 데이터 받기
        data = request.get_json()
        arr = data.get('array', [])
        
        if not arr:
            return jsonify({'error': '배열 데이터가 없습니다.'}), 400

        # 초기 상태 저장
        steps = []
        steps.append(list(arr)) # 얕은 복사로 현재 상태 저장
        
        n = len(arr)
        
        # 단순 선택 정렬 알고리즘 수행
        for i in range(n):
            min_idx = i
            # i번째 이후의 원소들 중 최솟값의 인덱스를 찾음
            for j in range(i + 1, n):
                if arr[j] < arr[min_idx]:
                    min_idx = j
            
            # 찾은 최솟값을 현재 위치(i)와 교환 (자리가 다를 경우에만)
            if min_idx != i:
                arr[i], arr[min_idx] = arr[min_idx], arr[i]
                # 배열에 변화가 생겼으므로 현재 단계를 저장
                steps.append(list(arr))

        # 최종 결과 반환
        return jsonify({
            'status': 'success',
            'original': data.get('array'),
            'sorted': arr,
            'steps': steps,
            'complexity': 'O(n²)',
            'message': '단순 선택 정렬이 완료되었습니다.'
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # 로컬 테스트 시 8080 포트 사용
    app.run(host='0.0.0.0', port=8080)
