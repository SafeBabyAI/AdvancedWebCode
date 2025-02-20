from fastapi import FastAPI
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from models.resnet_model import ResNetModel
from models.yolo_model import YOLODetector
from PIL import Image
import cv2
from fastapi.middleware.cors import CORSMiddleware
import io

# FastAPI 앱 생성
app = FastAPI()

# CORS 정책 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인 허용 (배포 시 특정 도메인만 허용)
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드 허용
    allow_headers=["*"],  # 모든 헤더 허용
)

#video_path="./temp/test_video.mp4" # 테스트용 비디오 파일 경로(.mp4)

# 모델 로드 & 카메라 설정
resnet_model = ResNetModel("./models/best_model.pth")
yolo_detector = YOLODetector("./models/yolov8n.pt")# 모니터링 상태 변수 초기화
monitoring_state = {"state": "inactive"}

# 현재 접속한 클라이언트 리스트 저장
connected_clients = set()

print(connected_clients)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """클라이언트와 WebSocket 연결을 설정하고, 웹캠 프레임을 받아 분석 후 응답하는 함수"""
    print("WebSocket 요청 받음")  # 웹소켓 요청 로그 추가
    await websocket.accept()
    connected_clients.add(websocket)
    print(f"연결된 클라이언트 수: {len(connected_clients)}")
    try:
        while True:
            # 클라이언트에서 프레임을 바이너리 데이터로 받음
            data = await websocket.receive_bytes()
            
            # 수신된 데이터를 PIL 이미지로 변환
            image = Image.open(io.BytesIO(data))

            # ResNet 모델로 앞면/뒷면/옆면 판별
            position = resnet_model.predict(image)
            # YOLO 모델로 코 & 입 감지
            nose_detected, mouth_detected = yolo_detector.detect_nose_mouth(image)
            
            # 분석 결과 JSON으로 클라이언트에 전송
            await websocket.send_json({
                "position": position,
                "nose_detected": nose_detected,
                "mouth_detected": mouth_detected
            })

    except WebSocketDisconnect:
        print("클라이언트 연결 해제")
        connected_clients.remove(websocket)


# 모니터링 시작 API
@app.post("/start_monitoring")
async def start_monitoring():
    monitoring_state["state"] = "active"
    return {"status": "monitoring started"}

# 모니터링 중지 API
@app.post("/stop_monitoring")
async def stop_monitoring():
    monitoring_state["state"] = "inactive"
    return {"status": "monitoring stopped"}

# 현재 모니터링 상태 조회 API
@app.get("/get_status")
async def get_status():
    return monitoring_state

# FastAPI 서버 실행 명령어(복붙해서 사용하세요!)
# uvicorn main:app --host 0.0.0.0 --port 8000 --reload
