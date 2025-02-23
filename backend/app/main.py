from fastapi import FastAPI
from fastapi import FastAPI, WebSocket, WebSocketDisconnect,  HTTPException
from fastapi.middleware.cors import CORSMiddleware

from service.login import router as login_router
from service.register import router as register_router
from service.authcheck import router as autocheck_router
from service.returnhist import router as history_router

from models.resnet_model import ResNetModel
from models.yolo_model import YOLODetector
from PIL import Image
import io, json
from jose import jwt, JWTError
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from fastapi import Depends
from data.db import get_db
from data.user import User
from data.history import ObservationHistory
from data.imgdb import upload_image_to_blob
from service.login import get_current_user_id
from dotenv import load_dotenv
import os

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"  # JWT 암호화 알고리즘

# FastAPI 앱 생성
app = FastAPI()

# CORS 정책 설정
allowed_origins = [
        "https://safe13aby.koreacentral.cloudapp.azure.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,  # 모든 도메인 허용 (배포 시 특정 도메인만 허용)
    allow_credentials=True,
    allow_methods=["GET","POST","PUT","DELETE","OPTIONS","HEAD"],  # 모든 HTTP 메서드 허용
    allow_headers=["*"],  # 모든 헤더 허용
)

# 모델 로드 & 카메라 설정
resnet_model = ResNetModel("./models/best_model.pth")
yolo_detector = YOLODetector("./models/best.pt")# 모니터링 상태 변수 초기화
monitoring_state = {"state": "inactive"}

connected_clients = set() # 현재 접속한 클라이언트 리스트 저장
active_alerts = {}  # 활성 알림 저장 (client_id 기준)
print(connected_clients)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()  # WebSocket 연결 수락
   # JWT 토큰을 검증하여 로그인된 사용자의 user_id를 가져옴(key로 사용)
    try:
        # 클라이언트로부터 JWT 토큰을 첫 메시지로 받음
        data = await websocket.receive_text()
        message = json.loads(data)

        if message.get("type") == "auth":
            token = message.get("token")

            if not token:
                await websocket.send_json({"status": "unauthorized"})
                await websocket.close(code=1008)
                return

            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
                user_id = payload.get("user_id")

                if not user_id:
                    await websocket.send_json({"status": "unauthorized"})
                    await websocket.close(code=1008)
                    return

                # ✅ 인증 성공 후 클라이언트 상태 저장
                client_id = id(websocket)
                client_state = {
                    "alert_count": 0,
                    "frame_count": 0,
                    "first_alert_frame": None,
                    "last_blob_url": None,
                    "observed_info": None,
                    "is_alert_active": False,
                    "user_id": user_id
                }

                active_alerts[client_id] = client_state
                connected_clients.add(websocket)

                print(f"✅ WebSocket 인증 성공: user_id={user_id}")
                await websocket.send_json({"status": "authorized"})

            except JWTError:
                await websocket.send_json({"status": "unauthorized"})
                await websocket.close(code=1008)
                return
        while True:
            data = await websocket.receive_bytes()
            client_state["frame_count"] += 1
            image = Image.open(io.BytesIO(data))

            position = resnet_model.predict(image)
            nose_detected, mouth_detected = yolo_detector.detect_nose_mouth(image)

            if position == "Back" or (not nose_detected and not mouth_detected):
                client_state["alert_count"] += 1

                if client_state["alert_count"] == 5:
                    # 5번째 alert 시점에서 이미지 저장
                    time_stamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
                    blob_url = upload_image_to_blob(image, f"monitoring/{time_stamp}.jpg")
                    print('이미지 저장됨!!!')

                    if blob_url:
                        client_state["first_alert_frame"] = client_state["frame_count"]
                        client_state["last_blob_url"] = blob_url
                        client_state["observed_info"] = json.dumps({
                            "position": position,
                            "nose_detected": nose_detected,
                            "mouth_detected": mouth_detected
                        })
                        client_state["is_alert_active"] = True

                await websocket.send_json({"status": "alert"})                

    except WebSocketDisconnect:
        print("클라이언트 연결 해제")
        connected_clients.remove(websocket)
        active_alerts.pop(client_id, None)

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

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.post("/stop_alert")
async def stop_alert(user_id: int = Depends(get_current_user_id), db=Depends(get_db)):
    """사용자가 버튼을 눌러서 강제로 알림을 멈출 때 호출 (user_id 기준으로 찾음)"""

    print(f"stop_alert() 요청됨! 받은 user_id: {user_id}")  # 디버깅

    # user_id를 기반으로 active_alerts에서 해당 사용자의 client_id 찾기
    client_id = next((cid for cid, state in active_alerts.items() if state["user_id"] == user_id), None)

    if client_id is None:
        return {"error": "No active alert for this user"}
    
    client_state = active_alerts[client_id]

    if client_state["is_alert_active"]:
        duration = client_state["frame_count"] - client_state["first_alert_frame"]
        
        if client_state["last_blob_url"] and client_state["observed_info"]:
            history_entry = ObservationHistory(
                user_id=client_state["user_id"],
                image_url=client_state["last_blob_url"],
                timestamp=datetime.now(timezone.utc),
                duration=duration,
                observed_info=client_state["observed_info"]
            )
            db.add(history_entry)
            db.commit()

        client_state["alert_count"] = 0
        client_state["is_alert_active"] = False
        print("Alert stopped and saved to history")
        return {"status": "alert stopped by user"}

    return {"status": "no active alert"}


# API 라우터 추가
app.include_router(login_router, prefix="/auth", tags=["Authentication"]) 
app.include_router(register_router, prefix="/auth", tags=["Authentication"]) # /auth/signup/ → 회원가입 API
app.include_router(autocheck_router, prefix="/auth", tags=["Authentication"]) # /auth/login/ → 로그인 API (JWT 토큰 반환)
app.include_router(history_router, prefix="/api", tags=["History"]) 

# FastAPI 서버 실행 명령어(복붙해서 사용하세요!)
# uvicorn main:app --host 0.0.0.0 --port 8000 --reload
