<template>
  <div class="alerts-page">
    <!-- 설정 옵션들 -->
    <div class="settings-options">
      <!-- Alerts 설정 토글 -->
      <div class="option">
        <span>Alerts settings</span>
        <label class="switch">
          <input type="checkbox" v-model="alertsEnabled" />
          <span class="slider"></span>
        </label>
      </div>

      <!-- Alert Trigger Time 슬라이더 -->
      <div class="option">
        <span>Alert Trigger Time (Sec)</span>
        <input
          type="range"
          v-model="alertTime"
          :min="1"
          :max="60"
          :step="1"
          class="with-midline"
        />
        <p class="slider-value">{{ alertTime }} Sec</p>
      </div>
    </div>
  </div>
</template>

<script>
// Font Awesome 관련 라이브러리 불러오기
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { faArrowLeft } from '@fortawesome/free-solid-svg-icons'


// 아이콘 등록
library.add(faArrowLeft)

export default {
  name: "AlertsPage",
  components: {
    FontAwesomeIcon
  },
  data() {
    return {
      alertsEnabled: true,
      alertTime: 30
    };
  },
  watch: {
    alertsEnabled(newVal) {
      console.log("Alerts settings changed:", newVal);
    },
    alertTime(newVal) {
      console.log("Alert Trigger Time changed:", newVal);
    }
  }
};
</script>

<style scoped>
/* 전체 컨테이너 */
.alerts-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen,
    Ubuntu, Cantarell, "Open Sans", "Helvetica Neue", sans-serif;
  position: relative;
  padding-bottom: 80px; /* 하단 네비게이션 공간 확보 (필요 시 추가) */
}

/* 헤더 스타일 */
.header {
  position: relative;
  width: 100%;
  padding: 10px 20px;
  border-bottom: 1px solid #eee;
}
.back-button {
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
  position: absolute;
  left: 20px;
  top: 50%;
  transform: translateY(-50%);
}
.header-title {
  margin: 0;
  text-align: center;
  font-size: 20px;
}

/* 설정 옵션 영역 */
.settings-options {
  width: 100%;
  margin-top: 20px;
}
.option {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 16px;
  padding: 15px 0;
  border-bottom: 1px solid #eee;
}
.option:last-of-type {
  border-bottom: none;
}

/* iOS 스타일 토글 스위치 */
.switch {
  position: relative;
  display: inline-block;
  width: 50px;
  height: 28px;
}
.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}
.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  transition: 0.4s;
  border-radius: 28px;
}
.slider:before {
  position: absolute;
  content: "";
  height: 22px;
  width: 22px;
  left: 3px;
  bottom: 3px;
  background-color: #fff;
  transition: 0.4s;
  border-radius: 50%;
}
input:checked + .slider {
  background-color: #6a5acd;
}
input:checked + .slider:before {
  transform: translateX(22px);
}

/* 슬라이더 (Alert Trigger Time) 스타일 */
input[type="range"] {
  -webkit-appearance: none;
  appearance: none;
  width: 60%;
  background: transparent;
  cursor: pointer;
  margin-left: 10px;
  position: relative;
}
input[type="range"]::-webkit-slider-runnable-track {
  height: 5px;
  background: #e0d7ff;
  border-radius: 5px;
}
input[type="range"]::-moz-range-track {
  height: 5px;
  background: #e0d7ff;
  border-radius: 5px;
}
input[type="range"]::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 15px;
  height: 15px;
  background: #6a5acd;
  border-radius: 50%;
  border: 2px solid #fff;
  margin-top: -5px;
}
input[type="range"]::-moz-range-thumb {
  width: 15px;
  height: 15px;
  background: #6a5acd;
  border-radius: 50%;
  border: 2px solid #fff;
}

/* 슬라이더 중앙선 */
input[type="range"].with-midline::before {
  content: "";
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 2px;
  height: 16px;
  background: #6a5acd;
}

/* 슬라이더 값 표시 */
.slider-value {
  margin-top: 10px;
  font-size: 16px;
}
</style>
