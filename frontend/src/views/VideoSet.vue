<template>
    <div class="video-settings-container">
      <!-- 상단 제목 -->
      <div class="header">
        <button @click="$router.go(-1)" class="back-button">
          <font-awesome-icon :icon="['fas', 'arrow-left']" />
        </button>
        <h2>Video Settings</h2>
      </div>
  
      <!-- 상단 비디오 (이미지로 대체 가능) -->
      <div class="video-preview">
        <img src="@/assets/test.png" alt="Video Preview" />
      </div>
  
      <!-- 설정 옵션 -->
      <div class="settings-options">
        <!-- Night Mode Toggle -->
        <div class="option">
          <span>Night Mode</span>
          <label class="switch">
            <input type="checkbox" v-model="nightMode" />
            <span class="slider"></span>
          </label>
        </div>
  
        <!-- Voice Detection Toggle -->
        <div class="option">
          <span>Voice Detection</span>
          <label class="switch">
            <input type="checkbox" v-model="voiceDetection" />
            <span class="slider"></span>
          </label>
        </div>
  
        <!-- Zoom In/Out Slider -->
        <div class="option">
          <span>Zoom In/Out</span>
          <input type="range" v-model="zoomLevel" min="1" max="10" step="0.1" />
        </div>
  
        <!-- Brightness Slider -->
        <div class="option">
          <span>Brightness</span>
          <input type="range" v-model="brightness" min="0" max="100" step="1" />
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        nightMode: false, // 🌙 Night Mode 상태
        voiceDetection: true, // 🎙️ Voice Detection 상태
        zoomLevel: 5, // 🔍 Zoom Level (1~10)
        brightness: 50, // 💡 Brightness (0~100)
      };
    },
    watch: {
      nightMode(newValue) {
        console.log("Night Mode:", newValue ? "ON" : "OFF");
      },
      voiceDetection(newValue) {
        console.log("Voice Detection:", newValue ? "ON" : "OFF");
      },
      zoomLevel(newValue) {
        console.log("Zoom Level:", newValue);
      },
      brightness(newValue) {
        console.log("Brightness:", newValue);
      },
    },
  };
  </script>
  
  <style scoped>
  /* ✅ 전체 컨테이너 스타일 */
  .video-settings-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20px;
    font-family: Arial, sans-serif;
  }
  
  /* ✅ 헤더 스타일 */
  .header {
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 10px 0;
    font-size: 20px;
    text-align: center;
  }
  
  .back-button {
    background: none;
    border: none;
    font-size: 20px;
    cursor: pointer;
  }
  
  /* ✅ 비디오 (또는 이미지) 미리보기 */
  .video-preview img {
    width: 90%;
    max-width: 350px;
    border-radius: 10px;
    margin-bottom: 20px;
  }
  
  /* ✅ 설정 옵션 */
  .settings-options {
    width: 90%;
    max-width: 400px;
    display: flex;
    flex-direction: column;
    gap: 20px;
  }
  
  /* ✅ 개별 옵션 스타일 */
  .option {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 16px;
  }
  
  /* ✅ 토글 스위치 스타일 */
  .switch {
    position: relative;
    display: inline-block;
    width: 40px;
    height: 22px;
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
    border-radius: 22px;
  }
  
  .slider:before {
    position: absolute;
    content: "";
    height: 16px;
    width: 16px;
    left: 4px;
    bottom: 3px;
    background-color: white;
    transition: 0.4s;
    border-radius: 50%;
  }
  
  input:checked + .slider {
    background-color: #6a5acd;
  }
  
  input:checked + .slider:before {
    transform: translateX(18px);
  }
  
  /* ✅ 슬라이더 스타일 */
  input[type="range"] {
    width: 70%;
    appearance: none;
    background: #e0d7ff;
    height: 5px;
    border-radius: 5px;
    outline: none;
  }
  
  input[type="range"]::-webkit-slider-thumb {
    appearance: none;
    width: 15px;
    height: 15px;
    background: #6a5acd;
    border-radius: 50%;
    cursor: pointer;
  }
  </style>
  