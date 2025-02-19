<template>
    <div class="settings-container">
      <h2>설정</h2>
  
      <div class="setting-item">
        <label>알림 설정</label>
        <input type="checkbox" v-model="notificationsEnabled" />
      </div>
  
      <div class="setting-item">
        <label>위험 감지 임계값</label>
        <input type="range" v-model="riskThreshold" min="0.1" max="1.0" step="0.1" />
        <p>현재 임계값: {{ riskThreshold.toFixed(1) }}</p>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        notificationsEnabled: true,
        riskThreshold: 0.5,
      };
    },
    watch: {
      riskThreshold(newVal) {
        console.log("위험 감지 임계값 변경:", newVal);
      },
    },
  };
  </script>
  
  <style scoped>
  .settings-container {
    text-align: center;
    padding: 20px;
  }
  .setting-item {
    margin: 15px 0;
  }
  </style>
  