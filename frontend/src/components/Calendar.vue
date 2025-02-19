<template>
    <div class="calendar-container">
      <!-- 현재 선택된 날짜 -->
      <div class="calendar-header">
        <span class="date-text">{{ formattedDate }}</span>
        <font-awesome-icon icon="pen" class="edit-icon" @click="toggleDatePicker" />
      </div>
      <hr>
      <!-- 달력 컴포넌트 -->
      <VueDatePicker
        v-if="showDatePicker"
        v-model="selectedDate"
        @update:model-value="updateDate"
        inline
        :dark="true"
        auto-apply
        :enable-time-picker="false"
        :locale="'en'"
      />
    </div>
  </template>
  
  <script>
  import { ref, computed } from "vue";
  import VueDatePicker from "@vuepic/vue-datepicker";
  import "@vuepic/vue-datepicker/dist/main.css";
  
  export default {
    components: { VueDatePicker },
    setup() {
      const selectedDate = ref(new Date());
      const showDatePicker = ref(true); // 항상 달력을 보이게 설정
  
      // 날짜 포맷 (예: "Mon, Aug 17")
      const formattedDate = computed(() =>
        selectedDate.value.toLocaleDateString("en-US", {
          weekday: "short",
          month: "short",
          day: "2-digit",
        })
      );
  
      // 날짜 변경 핸들러
      const updateDate = (newDate) => {
        selectedDate.value = newDate;
      };
  
      return { selectedDate, formattedDate, showDatePicker, updateDate };
    },
  };
  </script>
  
  <style scoped>

  /* ✅ 캘린더 전체 컨테이너 */
  .calendar-container {
    width: 90%;
    max-width: 400px;
    margin: 20px auto;
    background: #f8f9fa;
    border-radius: 12px;
    box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
    padding: 15px;
  }
  
  /* ✅ 캘린더 헤더 */
  .calendar-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: #f8f9fa;
    padding: 10px 15px;
    border-radius: 10px;
    font-size: 1.4rem;
    font-weight: bold;
    color: #333;
  }
  
  /* ✅ 날짜 텍스트 */
  .date-text {
    display: flex;
    align-items: center;
    gap: 10px;
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
  :deep(.dp__calendar_header_separator){
    display: none;
  }
  :deep(.dp__calendar_header){
    font-weight: normal;
  }
  
</style>
  