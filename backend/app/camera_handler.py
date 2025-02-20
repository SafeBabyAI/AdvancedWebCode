import cv2
import threading
import time
from fastapi.responses import StreamingResponse

# OpenCV 멀티스레딩 비활성화 (필요한 경우 추가)
cv2.setNumThreads(0)

class CameraHandler:
    def __init__(self, video_path=None):
        if video_path:
            self.cap = cv2.VideoCapture(video_path)  # 동영상 파일을 열기
        else:
            self.cap = cv2.VideoCapture(0)  # 웹캠 사용

        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # 최신 프레임을 유지하도록 버퍼 크기 설정
        self.lock = threading.Lock()  # 멀티스레드 환경에서 프레임 동기화

    def generate_frames(self):
        fps = self.cap.get(cv2.CAP_PROP_FPS)  #  원본 영상의 FPS 가져오기
        delay = 1 / fps if fps > 0 else 0.033  # 초당 프레임 속도 (기본 30FPS)

        while self.cap.isOpened():  # 비디오 캡처가 열려 있을 때만 실행
            with self.lock:
                success, frame = self.cap.read()
                if not success:
                    print("프레임을 가져올 수 없습니다. 비디오 리셋 중...")
                    self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # ✅ 영상이 끝나면 처음부터 다시 재생
                    continue

                _, buffer = cv2.imencode(".jpg", frame)  
                frame_bytes = buffer.tobytes()  # 바이트 스트림 변환

            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + frame_bytes + b"\r\n"
            )
            time.sleep(delay)  # 프레임 속도 조절

    def get_video_stream(self):
        return StreamingResponse(
            self.generate_frames(), media_type="multipart/x-mixed-replace; boundary=frame"
        )

    def close(self):
        if self.cap.isOpened():
            print("비디오 스트림 종료 중...")
            self.cap.release()

    def __del__(self):
        self.close()
