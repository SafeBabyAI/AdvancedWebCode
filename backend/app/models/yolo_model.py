from ultralytics import YOLO
import cv2

class YOLODetector:
    def __init__(self, model_path):
        self.model = YOLO(model_path)

    def detect_nose_mouth(self, image):
        results = self.model.predict(image, conf=0.5)  # 🔹 신뢰도 50% 이상 객체 탐지
        detected_classes = []

        for box in results[0].boxes:
            class_id = int(box.cls)
            label = self.model.names[class_id]
            if label in ["mouth", "nose"]:
                detected_classes.append(label)

        nose_detected = "nose" in detected_classes
        mouth_detected = "mouth" in detected_classes

        return nose_detected, mouth_detected  # 🔹 코 & 입 감지 결과 반환
