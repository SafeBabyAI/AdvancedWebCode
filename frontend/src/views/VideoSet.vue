<template>
  <div class="video-settings-container">
    <!-- 비디오 미리보기 (위/아래 구분선 있음) -->
    <div class="video-preview">
      <img
        src="../assets/cam.png"
        alt="Video Preview"
      />
    </div>

    <!-- 설정 옵션들 -->
    <div class="settings-options">
      <!-- Night Mode (구분선 제거) -->
      <div class="option">
        <span>Night Mode</span>
        <label class="switch">
          <input type="checkbox" v-model="nightMode" />
          <span class="slider"></span>
        </label>
      </div>

      <!-- Voice Detection (구분선 제거) -->
      <div class="option">
        <span>Voice Detection</span>
        <label class="switch">
          <input type="checkbox" v-model="voiceDetection" />
          <span class="slider"></span>
        </label>
      </div>

      <!-- Zoom In/Out Slider (중앙선 포함) -->
      <div class="option">
        <span>Zoom In/Out</span>
        <input
          type="range"
          class="with-midline"
          v-model="zoomLevel"
          min="1"
          max="10"
          step="0.1"
        />
      </div>

      <!-- Brightness Slider (중앙선 포함) -->
      <div class="option">
        <span>Brightness</span>
        <input
          type="range"
          class="with-midline"
          v-model="brightness"
          min="0"
          max="100"
          step="1"
        />
      </div>
    </div>

    <!-- 하단 네비게이션 바 (카메라 버튼 제거: 홈, 설정 아이콘만 표시) -->
    <nav class="bottom-nav">
      <button class="nav-icon">
        <font-awesome-icon :icon="['fas', 'home']" />
      </button>
      <button class="nav-icon">
        <font-awesome-icon :icon="['fas', 'cog']" />
      </button>
    </nav>
  </div>
</template>

<script>
// Font Awesome 관련 라이브러리 불러오기
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { faArrowLeft, faHome, faCog } from '@fortawesome/free-solid-svg-icons'

// 아이콘 등록
library.add(faArrowLeft, faHome, faCog)

export default {
  name: 'VideoSettings',
  components: {
    FontAwesomeIcon
  },
  data() {
    return {
      nightMode: true,
      voiceDetection: true,
      zoomLevel: 5,
      brightness: 50
    }
  },
  methods: {
    goBack() {
      alert("뒤로가기 클릭");
    }
  }
}
</script>

<style scoped>
/* 전체 컨테이너 */
.video-settings-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen,
    Ubuntu, Cantarell, "Open Sans", "Helvetica Neue", sans-serif;
  position: relative;
  padding-bottom: 80px; /* 하단 네비게이션 공간 확보 */
}

/* 상단 헤더 */
.header {
  position: relative;
  width: 100%;
  padding: 10px 20px;
}
.back-button {
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
}
.header-title {
  position: absolute;
  top: 0;
  left: 50%;
  transform: translateX(-50%);
  margin: 0;
  font-size: 20px;
  text-align: center;
}

/* 비디오 미리보기: 위/아래 구분선 추가 */
.video-preview {
  width: 100%;
  border-top: 1px solid #eee;
  border-bottom: 1px solid #eee;
  padding: 10px 0;
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
}
.video-preview img {
  width: 100%;
  border-radius: 10px;
  object-fit: cover;
}

/* 설정 옵션들 */
.settings-options {
  width: 100%;
  display: flex;
  flex-direction: column;
}
.option {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 16px;
  padding: 15px 0;
  border-bottom: 1px solid #eee;
}
/* Night Mode와 Voice Detection 옵션은 구분선 제거 */
.settings-options .option:nth-child(1),
.settings-options .option:nth-child(2) {
  border-bottom: none;
}
.option:last-of-type {
  border-bottom: none;
}

/* 토글 스위치 (굵게) */
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

/* 슬라이더 (Zoom, Brightness) */
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

/* 하단 네비게이션 바 */
.bottom-nav {
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 60px;
  background-color: #fff;
  border-top: 1px solid #eee;
  display: flex;
  justify-content: space-around;
  align-items: center;
}
.nav-icon {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 24px;
}
</style>
