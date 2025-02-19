import torch
import torchvision.transforms as transforms
from torchvision import models
from PIL import Image
import cv2

class ResNetModel:
    def __init__(self, model_path):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        # ✅ ResNet50 모델 불러오기
        self.model = models.resnet50(weights=None)
        num_ftrs = self.model.fc.in_features
        self.model.fc = torch.nn.Linear(num_ftrs, 3)  # 🔹 3개 클래스 (Back, Front, Side)

        # ✅ 저장된 가중치 로드
        self.model.load_state_dict(torch.load(model_path, map_location=self.device))
        self.model.to(self.device)
        self.model.eval()  # 🔥 모델을 평가 모드로 전환

        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
        self.class_names = ["Back", "Front", "Side"]  # 클래스 이름

    def predict(self, image_path):
        image = Image.open(image_path).convert("RGB")
        image_tensor = self.transform(image).unsqueeze(0).to(self.device)

        with torch.no_grad():
            output = self.model(image_tensor)
            predicted_class = torch.argmax(output, dim=1).item()

        return self.class_names[predicted_class]  # 🔹 예측된 클래스 반환