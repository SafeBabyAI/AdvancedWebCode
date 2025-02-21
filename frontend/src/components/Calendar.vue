<template>
  <div class="calendar-container">
    <!-- 현재 선택된 날짜 -->
    <div class="calendar-header">
      <span class="date-text">{{ formattedDate }}</span>
      <font-awesome-icon icon="pen" class="edit-icon" />
    </div>
    <hr />

    <!-- 달력 컴포넌트 -->
    <VueDatePicker
      v-model="selectedDate"
      @update:model-value="updateDate"
      inline
      auto-apply
      :enable-time-picker="false"
      :locale="'ko'"
    />
  </div>
</template>

<script>
import VueDatePicker from "@vuepic/vue-datepicker";
import "@vuepic/vue-datepicker/dist/main.css";

export default {
  components: { VueDatePicker },
  data() {
    return {
      selectedDate: new Date(),
    };
  },
  computed: {
    formattedDate() {
      return this.selectedDate.toLocaleDateString("ko-KR", {
        weekday: "short",
        month: "short",
        day: "2-digit",
      });
    },
  },
  methods: {
    updateDate(newDate) {
      this.selectedDate = newDate;
      //  UTC 기준으로 변환하여 백엔드로 전송
      const formatted = newDate.toISOString().split("T")[0];
      this.$emit("date-selected", formatted);
    },
  },
};
</script>
<style scoped>
/* ✅ 캘린더 전체 컨테이너 */
.calendar-container {
  width: 75vw;
  margin-bottom: 1.5vh; 
  background-color: #f8f9fa;
  border-radius: 1rem; /* border-radius를 rem으로 설정 */
  padding: 1.5rem; /* 패딩을 rem으로 설정 */
}

/* ✅ 캘린더 헤더 */
.calendar-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1rem;
  background-color: #f8f9fa;
  border-radius: 1rem; /* border-radius를 rem으로 설정 */
  font-size: 1.4rem; /* 폰트 크기를 rem으로 설정 */
  font-weight: bold;
  color: #333;
}

/* ✅ 날짜 텍스트 */
.date-text {
  display: flex;
  align-items: center;
  gap: 1rem; /* 간격을 rem으로 설정 */
}

/* ✅ 수정 아이콘 */
.edit-icon {
  cursor: pointer;
  color: #888;
  transition: color 0.3s;
}

.edit-icon:hover {
  color: #555;
}

/* ✅ VueDatePicker 기본 스타일 변경 */
:deep(.dp__theme_dark) {
  border: none;
  --dp-background-color: #f8f9fa;
  --dp-text-color: #333;
  --dp-hover-color: #eef2ff;
  --dp-primary-color: #3b82f6;
  --dp-primary-text-color: white;
}

:deep(.dp__calendar_header_separator) {
  display: none;
}

:deep(.dp__calendar_header) {
  font-weight: normal;
}
</style>