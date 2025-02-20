<template>
    <div class="alerts-page">
      <h2 class="alerts-title">Alerts & Notifications</h2>
  
      <!-- 알림 설정 토글 -->
      <div class="setting-item">
        <label for="alertsEnabled">Alerts settings</label>
        <!-- 간단히 checkbox로 구현 (iOS 토글 등은 추가 라이브러리 사용 가능) -->
        <input
          id="alertsEnabled"
          type="checkbox"
          v-model="alertsEnabled"
          class="toggle-input"
        />
      </div>
  
      <!-- Alert Trigger Time 슬라이더 -->
      <div class="setting-item">
        <label for="alertTime">Alert Trigger Time (Sec)</label>
        <input
          id="alertTime"
          type="range"
          v-model="alertTime"
          :min="1"
          :max="60"
          :step="1"
          class="slider-input"
        />
        <p>{{ alertTime }} Sec</p>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: "AlertsPage",
    data() {
      return {
        alertsEnabled: true, // 알림 설정 ON/OFF
        alertTime: 30,       // 슬라이더 기본값
      };
    },
    watch: {
      alertsEnabled(newVal) {
        console.log("Alerts settings changed:", newVal);
      },
      alertTime(newVal) {
        console.log("Alert Trigger Time changed:", newVal);
      },
    },
  };
  </script>
  
  <style scoped>
  .alerts-page {
    padding: 20px;
  }
  .alerts-title {
    text-align: center;
    margin-bottom: 20px;
    font-size: 24px;
  }
  .setting-item {
    margin: 20px 0;
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  .toggle-input {
    transform: scale(1.2);
    margin-top: 10px;
  }
  .slider-input {
    width: 60%;
    margin-top: 10px;
  }
  </style>
  