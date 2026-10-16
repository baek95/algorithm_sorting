import os
from flask import Flask, request, jsonify
from flask_cors import CORS

# Flask 애플리케이션 생성 및 CORS 설정 (GAS와의 통신을 위해 필요)
app = Flask(__name__)
CORS(app)

def get_insertion_sort_steps(arr):
    """
    단순 삽입 정렬을 수행하고, 배열이 변경되는 각 단계를 리스트로 반환합니다.
    """
    # 초기 상태 저장 (값의 복사본을 넣어야 함)
    steps = [list(arr)]
    
    # 두 번째 요소부터 끝까지 반복
    for i in range(1, len(arr)):
        key = arr[i] # 현재 삽입될 숫자를 보관
        j = i - 1
        
        # key보다 큰 값을 만나면 오른쪽으로 한 칸씩 이동
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
            
        # 알맞은 위치에 key를 삽입
        arr[j + 1] = key
        
        # 각 패스(pass)가 끝날 때마다 현재 배열의 상태를 저장
        steps.append(list(arr))
        
    return steps

@app.route('/sort', methods=['POST'])
def sort_array():
    """
    POST 요청을 받아 정렬 단계를 반환하는 API 엔드포인트
    """
    try:
        data = request.get_json()
        if not data or 'array' not in data:
            return jsonify({'error': '유효하지 않은 입력입니다. array 필드가 필요합니다.'}), 400

        # 클라이언트에서 전송한 배열
        input_array = data['array']
        
        # 정렬 수행 및 단계별 결과 획득
        steps = get_insertion_sort_steps(input_array)
        
        # 시간/공간 복잡도 정보
        complexity = {
            'time': '최악 O(n²), 평균 O(n²), 최선 O(n)',
            'space': 'O(1) (제자리 정렬)'
        }
        
        # JSON 형태로 반환
        return jsonify({
            'steps': steps,
            'complexity': complexity,
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Cloud Run에서 제공하는 PORT 환경 변수 사용 (기본값 8080)
    port = int(os.environ.get('PORT', 8080))
    # 0.0.0.0으로 바인딩하여 외부 접속 허용
    app.run(host='0.0.0.0', port=port)
