from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import cv2
import numpy as np
import torch
import torchvision.models as models
from torchvision import transforms
from io import BytesIO
from PIL import Image

app = FastAPI()

### CORS 설정 (Vue.js 프론트엔드에서 API 호출 허용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 배포 시 특정 도메인으로 제한해야 함
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

### 모델 로드
device = "cuda" if torch.cuda.is_available() else "cpu"

model = models.resnet50(weights=None)  # 사전 학습 없이 ResNet50 로드
num_ftrs = model.fc.in_features
model.fc = torch.nn.Linear(num_ftrs, 3)  # 2개 클래스 분류
model.load_state_dict(torch.load("./models/best_model.pth", map_location=device))  # 가중치 로드

model.to(device)
model.eval()

"""이미지 처리 함수"""
def detect_risk(image: Image.Image):
    img = np.array(image)
    img_resized = cv2.resize(img, (224, 224))  # 모델 입력 크기에 맞게 변환
    img_tensor = transforms.ToTensor()(img_resized).unsqueeze(0).to(device)  # (1, C, H, W)

    with torch.no_grad():
        output = model(img_tensor)
        probabilities = torch.softmax(output, dim=1)  # softmax 적용
        risk_prob = probabilities[0, 0].item()  # 위험 확률 추출

    alert_text = "Dangerous!" if risk_prob > 0.5 else "Safe :)"
    return {"alert": alert_text, "risk_prob": risk_prob}


class DataModel(BaseModel):
    data: str  # 문자열 데이터를 받을 필드


@app.get("/")
def home():
    return {"message": "Hello from FastAPI!"}

@app.post("/data")
def receive_data(payload: DataModel):
    return {"message": f"서버가 받은 데이터: {payload.data}"}

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(BytesIO(contents)).convert("RGB")  # 이미지 로드
    result = detect_risk(image)
    return result

# 실행 명령어: uvicorn main:app --host 0.0.0.0 --port 8000 --reload
