<template>
    <div class="calendar-container">
      <h2>아기 위험 감지 기록</h2>
      <vue-cal
        :events="events"
        :disable-views="['years', 'year']"
        active-view="month"
        locale="ko"
      />
    </div>
  </template>
  
  <script>
  import VueCal from "vue-cal";
  import "vue-cal/dist/vuecal.css";
  
  export default {
    components: { VueCal },
    data() {
      return {
        events: [
          { start: "2025-02-10", title: "위험 감지 (확률 0.8)" },
          { start: "2025-02-14", title: "안전" },
          { start: "2025-02-17", title: "위험 감지 (확률 0.6)" },
        ],
      };
    },
  };
  </script>
  
  <style scoped>
  .calendar-container {
    text-align: center;
    padding: 20px;
  }
  </style>
  