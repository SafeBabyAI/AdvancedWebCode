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

    <!-- video_feed 엔드포인트를 통해 전달된 영상을 표시 -->
    <img :src="videoStreamUrl" alt="Monitoring View" class="monitoring-image" />

    <!-- 버튼 그룹(@click 디렉티브를 사용하여 버튼 클릭 시 특정 메서드 실행) -->
    <div class="button-group">
      <button @click="startMonitoring" class="start-button" :class="{ active: isMonitoring }">Start monitoring</button>
      <button @click="stopMonitoring" class="stop-button" :class="{ active: !isMonitoring }">Stop monitoring</button>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      monitoringState: "inactive", // 상태 (inactive, active, alert)
      isMonitoring: false, // 루프 실행 여부 추가 (true, false)
      alertDetected: false,
      alertStartTime: null,
      elapsedTime: "00:00",
      timerInterval: null,
      videoStreamUrl: "http://localhost:8000/video_feed", //FastAPI 백엔드 서버에서 제공하는 비디오 스트림 엔드포인트를 가리키는 URL이다.
      // 즉, 웹 브라우저에서 이 URL을 img 태그에 설정하면 스트리밍 영상이 실시간으로 갱신됨.
    };
  },
  computed: {
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
        await axios.post("http://localhost:8000/start_monitoring");
        this.monitoringState = "active";
        this.alertDetected = false;
        this.elapsedTime = "00:00";
        clearInterval(this.timerInterval);
        this.isMonitoring = true; // 모니터링 루프 실행 플래그 ON
        this.monitoringLoop(); // 루프 돌리기 
      } catch (error) {
        console.error("Error starting monitoring:", error);
      }
    },
    async stopMonitoring() {
      try {
        await axios.post("http://localhost:8000/stop_monitoring");
        this.monitoringState = "inactive";
        this.alertDetected = false;
        this.elapsedTime = "00:00";
        clearInterval(this.timerInterval);
        this.isMonitoring = false; //모니터링 루프 중단
      } catch (error) {
        console.error("Error stopping monitoring:", error);
      }
    },
    async monitoringLoop() {
      let alertCount = 0;
      let safeCount = 0;

      while (this.isMonitoring) { // 모니터링 상태에 따라 계속 실행됨
        try {
          const analyzeResponse = await axios.post("http://localhost:8000/analyze_image", 
            { file: null },  
            { headers: { "Content-Type": "multipart/form-data" } }
          );

          const { position, nose_detected, mouth_detected } = analyzeResponse.data;

          console.log(`Position: ${position}, Nose: ${nose_detected}, Mouth: ${mouth_detected}`);

          if (position === "Back" && (!nose_detected || !mouth_detected)) {
            alertCount++;
            safeCount = 0;
          } else {
            safeCount++;
            alertCount = 0;
          }

          console.log(`위험 감지 횟수: ${alertCount}, 안전 감지 횟수: ${safeCount}`);

          if (alertCount >= 1) {
            this.alertDetected = true;
            this.monitoringState = "alert";
            if (!this.alertStartTime) {
              this.alertStartTime = new Date();
              this.timerInterval = setInterval(this.updateElapsedTime, 1000);
            }
          }

          // `alert` 상태에서도 분석 계속 수행
          if (safeCount >= 3 && this.monitoringState === "alert") {
            this.alertDetected = false;
            this.monitoringState = "active";
            this.alertStartTime = null;
            clearInterval(this.timerInterval);
            this.elapsedTime = "00:00";
            console.log("안전 상태로 복귀");
          }

          await new Promise((resolve) => setTimeout(resolve, 1000)); // 서버 과부화 방지지
        } catch (error) {
          console.error("분석 중 오류 발생:", error);
          break;
        }
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
