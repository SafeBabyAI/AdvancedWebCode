<template>
  <div class="monitoring-container">
    <!--  상태 표시 UI(:class - 현재 상태에 따라 동적으로 클래스가 변경) -->
    <div class="status-box" :class="statusClass">
      <font-awesome-icon :icon="statusIcon" class="status-icon" />
      <span>{{ statusText }}</span>
    </div>
    <!--  위험 감지 시 경과 시간 표시(alertDetected가 true일 때만 이 <div>가 렌더링됨) -->
    <div v-if="alertDetected" class="alert-timer">
      뒤집기 관측 경과시간 {{ elapsedTime }}
    </div>
    <!--  웹캠 영상 표시 -->
    <video ref="videoElement" autoplay playsinline class="monitoring-image"></video>
    <!-- 버튼 그룹(@click 디렉티브를 사용하여 버튼 클릭 시 특정 메서드 실행) -->
    <div class="button-group">
      <button @click="startMonitoring" class="start-button" :class="{ active: isMonitoring }">Start monitoring</button>
      <button @click="stopMonitoring" class="stop-button" :class="{ active: !isMonitoring }">Stop monitoring</button>
    </div>
  </div>
</template>
<script>
export default {
  data() {
    return {
      monitoringState: "inactive",
      isMonitoring: false,
      alertStartTime: null,
      elapsedTime: "00:00",
      timerInterval: null,

      websocket: null, // WebSocket 객체
      videoStream: null, // 웹캠 스트림
      canvas: null, // 프레임을 캡처할 캔버스
      ctx: null, // 캔버스 컨텍스트

      alertCount: 0,  
      safeCount: 0,  
    };
  },
  computed: {
    ALERT_THRESHOLD() {
      return 100;  // 위험 감지 기준
    },
    SAFE_THRESHOLD() {
      return 3;  // 안전 감지 기준
    },
    statusClass() {
      return {
        "status-inactive": this.monitoringState === "inactive",
        "status-active": this.monitoringState === "active",
        "status-alert": this.monitoringState === "alert",
      };
    },
    statusText() {
      if (this.monitoringState === "inactive") return "모니터링 비활성화 상태";
      if (this.monitoringState === "active") return "실시간 모니터링 중";
      if (this.monitoringState === "alert") return "위험이 감지되었습니다.";
      return "";
    },
    statusIcon() {
      if (this.monitoringState === "inactive") return ["fas", "video-slash"];
      if (this.monitoringState === "active") return ["fas", "video"];
      if (this.monitoringState === "alert") return ["fas", "bell"];
      return ["fas", "info-circle"];
    },
  },
  methods: {
    async startMonitoring() {
      try {
        this.isMonitoring = true;
        this.monitoringState = "active";
        this.elapsedTime = "00:00";
        clearInterval(this.timerInterval);
        this.alertCount = 0; // 위험 감지 카운트 초기화
        this.safeCount = 0; // 안전 감지 카운트 초기화

        // 웹캠 시작
        await this.startWebcam();

        // WebSocket 연결 (배포 시 바꿔야)
        this.websocket = new WebSocket("ws://127.0.0.1:8000/ws");

        this.websocket.onopen = () => {
          console.log("WebSocket 연결됨");
          this.sendFrames(); // 웹캠 프레임을 서버로 전송 시작
        };
        this.websocket.onmessage = (event) => { // 서버에서 메세지를 받을 때만 실행 
          this.handleServerResponse(event.data); // 서버의 응답을 처리하는 함수
        };

        this.websocket.onerror = (error) => console.error("WebSocket 오류:", error);
        this.websocket.onclose = () => console.log("WebSocket 연결 종료됨");

      } catch (error) {
        console.error("Error starting monitoring:", error);
      }
    },

    stopMonitoring() {
      this.isMonitoring = false;
      this.monitoringState = "inactive";
      this.elapsedTime = "00:00";
      clearInterval(this.timerInterval);

      // 웹캠 종료
      if (this.videoStream) {
        this.videoStream.getTracks().forEach((track) => track.stop());
      }
      // WebSocket 종료
      if (this.websocket) {
        this.websocket.close();
      }
    },

    async startWebcam() {
      try {
        const videoElement = this.$refs.videoElement; 
        // ref="videoElement"로 지정된 <video> 태그를 가져옴
        this.videoStream = await navigator.mediaDevices.getUserMedia({ video: true });
        // 사용자의 카메라 접근 권한을 요청하고, 비디오 스트림을 가져옴
        videoElement.srcObject = this.videoStream;
        //videoElement.srcObject에 웹캠 스트림을 직접 연결하여 <video>에서 재생되도록 함
        
        this.canvas = document.createElement("canvas"); // 캔버스 생성 (프레임 캡처 용도)
        this.ctx = this.canvas.getContext("2d");
      } catch (error) {
        console.error("웹캠을 사용할 수 없습니다:", error);
      }
    },

    sendFrames() {
      // WebSocket이 존재하지 않거나(!this.websocket) 아직 연결이 안 된 상태(this.websocket.readyState !== WebSocket.OPEN)
      if (!this.isMonitoring || !this.websocket || this.websocket.readyState !== WebSocket.OPEN) {
        return;
      }

      const videoElement = this.$refs.videoElement;
      this.canvas.width = videoElement.videoWidth;
      this.canvas.height = videoElement.videoHeight; // 웹캠의 실제 해상도에 맞게 캔버스를 동적으로 조정
      this.ctx.drawImage(videoElement, 0, 0, this.canvas.width, this.canvas.height); // <canvas> 요소의 2D 컨텍스트(this.ctx)를 사용해 웹캠에서 현재 프레임을 캡처

      this.canvas.toBlob((blob) => { // 이미지 데이터를 압축된 JPEG 포맷으로 변환
        if (blob) {
          this.websocket.send(blob); // blob 객체를 WebSocket을 통해 서버로 전송
        }
      }, "image/jpeg");

      setTimeout(() => this.sendFrames(), 100); // 100ms(0.1초) 후에 sendFrames() 함수를 다시 호출
    },

    handleServerResponse(data) {
      const response = JSON.parse(data);
      console.log("서버 응답:", response);

      // 위험 감지 조건 (Back이고 코 or 입 감지 안 됨)
      if (response.position === "Back" && (!response.nose_detected || !response.mouth_detected)) {
        this.alertCount++;  
        this.safeCount = 0;  
      }  // 안전 감지 조건 (Front or Slide 이고 코 or 입 감지 안 됨)
      else if (["Front", "Side"].includes(response.position) && response.nose_detected && response.mouth_detected) { // (Front 또는 Side이고, 코/입 감지됨)
        this.safeCount++;  
        this.alertCount = 0;  
      }

      if (this.alertCount >= this.ALERT_THRESHOLD) {
        if (this.monitoringState !== "alert") {
          this.monitoringState = "alert";
          this.alertStartTime = new Date();
          
          this.timerInterval = setInterval(this.updateElapsedTime, 1000);
        }
      }
      if (this.safeCount >= SAFE_THRESHOLD && this.monitoringState === "alert") {
        this.monitoringState = "active";
        this.alertStartTime = null;

        clearInterval(this.timerInterval);
        this.elapsedTime = "00:00";
      }

    },
    updateElapsedTime() {
      if (!this.alertStartTime) return;
      const now = new Date();
      const diff = Math.floor((now - this.alertStartTime) / 1000);
      const minutes = String(Math.floor(diff / 60)).padStart(2, "0");
      const seconds = String(diff % 60).padStart(2, "0");
      this.elapsedTime = `${minutes}:${seconds}`;
    },
  },
};
</script>


<style scoped>
.monitoring-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 2vh;
}

/* 상태 박스 */
.status-box {
  width: 60vw;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2vh;
  border-radius: 3vh;
  font-size: 1rem;
  border: 0.1rem solid #ddd;
  margin-bottom: 2vh;
  transition: color 0.5s ease-in-out;
}

/* 상태별 색상 */
.status-inactive {
  color: #666;
}
.status-active {
  color: #5b9cf5;
}
.status-alert {
  color: #d32f2f;
}

/* 위험 감지 타이머 */
.alert-timer {
  font-size: 1.2rem;
  font-weight: bold;
  color: #d32f2f;
  margin-bottom: 1vh;
}

/* 스트리밍 화면 */
.monitoring-image {
  width: 90vw;
  max-width: 50rem;
  border-radius: 1vh;
  box-shadow: 0 0.5vh 1vh rgba(0, 0, 0, 0.1);
}

/* 버튼 그룹 */
.button-group {
  display: flex;
  gap: 10vw;
  margin-top: 2vh;
}

/* 버튼 스타일 */
button {
  padding: 1.5vh 2vw;
  font-size: 1rem;
  font-weight: bold;
  border: none;
  border-radius: 2vh;
  cursor: pointer;
  box-shadow: 0.2vh 0.2vh 1vh rgba(0, 0, 0, 0.1);
  background: #e0e0e0;
  color: #333;
  transition: background-color 0.3s ease;
}
.start-button.active, .stop-button.active  {
  background-color: #77C3F2;
}

</style>
