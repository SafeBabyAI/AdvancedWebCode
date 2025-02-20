from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from models.resnet_model import ResNetModel
from models.yolo_model import YOLODetector
from camera_handler import CameraHandler
from PIL import Image
import cv2
from fastapi.middleware.cors import CORSMiddleware

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

video_path="./temp/test_video.mp4" # 테스트용 비디오 파일 경로(.mp4)
#video_path =None # 실제 환경

# 모델 로드 & 카메라 설정
resnet_model = ResNetModel("./models/best_model.pth")
yolo_detector = YOLODetector("./models/yolov8n.pt")
camera_handler = CameraHandler(video_path)

monitoring_state = {"state": "inactive"}  # 모니터링 상태 변수

#
@app.get("/video_feed")
async def video_feed():
    return camera_handler.get_video_stream()

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

# 이미지 업로드 & 분석 API
@app.post("/analyze_image")
async def analyze_image():  
    global monitoring_state

    #  카메라 프레임을 캡처
    success, frame = camera_handler.cap.read()
    if not success:
        return {"error": "카메라 프레임을 읽을 수 없음"}
    
    # OpenCV 프레임을 PIL 이미지로 변환해서 바로 넣기 (BGR → RGB 변환 후 PIL 이미지로 변환)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  
    pil_image = Image.fromarray(frame_rgb)
        
    # ResNet 모델로 앞면/뒷면/옆면 판별
    position = resnet_model.predict(pil_image)

    # YOLO 모델로 코 & 입 감지
    nose_detected, mouth_detected = yolo_detector.detect_nose_mouth(pil_image)

    print("현상태: ",monitoring_state)
    return {
        "position": position,
        "nose_detected": nose_detected,
        "mouth_detected": mouth_detected,
    }

# FastAPI 서버 실행 명령어(복붙해서 사용하세요!)
# uvicorn main:app --host 0.0.0.0 --port 8000 --reload
