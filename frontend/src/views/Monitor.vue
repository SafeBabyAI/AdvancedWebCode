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
      <button @click="startMonitoring" class="start-button">Start monitoring</button>
      <button @click="stopMonitoring" class="stop-button">Stop monitoring</button>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      monitoringState: "inactive",
      alertDetected: false,
      alertStartTime: null,
      elapsedTime: "00:00",
      timerInterval: null,
      videoStreamUrl: "http://localhost:8000/video_feed",
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
      if (this.monitoringState === "inactive") return " 모니터링 비활성화 상태";
      if (this.monitoringState === "active") return " 실시간 모니터링 중";
      if (this.monitoringState === "alert") return " 위험이 감지되었습니다.";
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
        clearInterval(this.timerInterval); // 이전 타이머를 정리
        this.monitoringLoop(); // 모니터링 상태를 계속 가져오는 함수 실행
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
      } catch (error) {
        console.error("Error stopping monitoring:", error);
      }
    },
    async monitoringLoop() {
  while (this.monitoringState === "active") {
    try {
      // ✅ 아기 상태 분석 요청
      const analyzeResponse = await axios.post("http://localhost:8000/analyze_image", 
        { file: null },  // 파일이 없더라도 요청을 보냄
        { headers: { "Content-Type": "multipart/form-data" } }
      );
      console.log("analyze_image 실행 결과:", analyzeResponse.data);

      // ✅ 최신 상태 가져오기
      const response = await axios.get("http://localhost:8000/get_status");
      const { state, alert, position } = response.data;

      console.log("백엔드 상태 업데이트:", state, alert, position);

      this.alertDetected = alert; // UI 업데이트
      this.monitoringState = alert ? "alert" : "active";

      if (alert && !this.alertStartTime) {  
        this.alertStartTime = new Date();
        this.timerInterval = setInterval(this.updateElapsedTime, 1000);
      }
      await new Promise((resolve) => setTimeout(resolve, 1000)); // 1초 대기 후 다시 실행
    } catch (error) {
      console.error("🚨 분석 중 오류 발생:", error);
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
/* ✅ 전체 컨테이너 스타일 */
.monitoring-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
}

/* ✅ 상태 박스 */
.status-box {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 90%;
  padding: 10px;
  border-radius: 20px;
  font-size: 1.2rem;
  font-weight: bold;
  border: 1px solid #ddd;
  margin-bottom: 15px;
  transition: background-color 0.5s ease-in-out;
}

/* ✅ 상태별 색상 */
.status-inactive {
  background: #f8f8f8;
  color: #666;
}
.status-active {
  background: #eef4ff;
  color: #5b9cf5;
}
.status-alert {
  background: #ffeded;
  color: #d32f2f;
}

/* ✅ 위험 감지 타이머 */
.alert-timer {
  font-size: 1.2rem;
  font-weight: bold;
  color: #d32f2f;
  margin-bottom: 10px;
}

/* ✅ 모니터링 화면 (스트리밍) */
.monitoring-image {
  width: 100%;
  max-width: 500px;
  border-radius: 10px;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
}

/* ✅ 버튼 그룹 */
.button-group {
  display: flex;
  gap: 10px;
  margin-top: 20px;
}

/* ✅ 버튼 스타일 */
button {
  padding: 10px 15px;
  font-size: 1rem;
  font-weight: bold;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
}

.start-button {
  background: #d7eaff;
  color: #1565c0;
}

.stop-button {
  background: #e0e0e0;
  color: #333;
}

button:hover {
  opacity: 0.8;
}
</style>
