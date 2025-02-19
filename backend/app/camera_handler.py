import cv2
import threading
import time
from fastapi.responses import StreamingResponse

class CameraHandler:
    def __init__(self, video_path=None):
        if video_path:
            self.cap = cv2.VideoCapture(video_path)  # 동영상 파일을 열기
        else:
            self.cap = cv2.VideoCapture(0)  # 웹캠 사용
        self.lock = threading.Lock() # 멀티스레드 환경에서 프레임을 안전하게 읽도록 동기화

    def generate_frames(self):
        fps = self.cap.get(cv2.CAP_PROP_FPS)  # 원본 영상의 FPS 가져오기
        delay = 1 / fps if fps > 0 else 0.033  # 초당 프레임 속도 (기본 30FPS)

        while True:
            with self.lock: #  동기화하여 한 번에 하나의 스레드만 접근 가능
                success, frame = self.cap.read()
                if not success:
                    self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0) # 영상이 끝나면 처음부터 다시 재생
                    continue

                _, buffer = cv2.imencode(".jpg", frame) # 프레임을 특정 포맷(JPEG)으로 인코딩
                frame_bytes = buffer.tobytes() # buffer (NumPy 배열 형태) → .tobytes() 를 통해 순수 바이트 스트림으로 변환

            # HTTP multipart/x-mixed-replace 포맷에 맞게 변환
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + frame_bytes + b"\r\n"
            )
            time.sleep(delay)  # 프레임 속도 조절

    def get_video_stream(self):
        return StreamingResponse(
            self.generate_frames(), media_type="multipart/x-mixed-replace; boundary=frame"
        )
    # StreamingResponse를 통해 실시간으로 영상 프레임을 클라이언트에 전송
    # media_type="multipart/x-mixed-replace; boundary=frame" → 웹 브라우저에서 연속된 이미지로 해석할 수 있도록 설정
    def __del__(self):
        self.cap.release() # 메모리 해제
