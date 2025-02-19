<script setup>
import BottomNavigation from "@/components/BottomNavigation.vue";
</script>
<template>
  <div class="history-container">
    <!-- 캘린더 컴포넌트 추가 -->
    <Calendar />
    <BottomNavigation/>
  </div>
</template>

<script>
import Calendar from "@/components/Calendar.vue";

export default {
  components: { Calendar },
};
</script>

<style scoped>
/* History 페이지 스타일 */
.history-container {
  text-align: center;
  padding: 20px;
  font-family: Arial, sans-serif;
}

</style>
