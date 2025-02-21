<script setup>
import Calendar from "@/components/Calendar.vue";
import BottomNavigation from "@/components/BottomNavigation.vue";
</script>

<template>
  <div class="history-container">

    <!-- 캘린더 컴포넌트 -->
    <Calendar @date-selected="fetchImagesByDate" />

    <!-- 선택한 날짜의 감지된 이미지들 표시 -->
    <div v-if="selectedDate" class="image-list">
      <div v-if="images.length > 0">
        <ul>
          <li v-for="image in images" :key="image.url">
            <img :src="'data:image/jpeg;base64,' + image.image_base64" class="history-image" alt="감지 이미지" />
            <p><strong>시간:</strong> {{ formatTime(image.timestamp) }}</p>
            <p><strong>지속 시간:</strong> {{ image.duration }}초</p>
            <p><strong>상태:</strong> {{ parseObservedInfo(image.observed_info).position }}</p>
            <p><strong>코/입 감지:</strong> 
              코 {{ parseObservedInfo(image.observed_info).nose_detected ? "✅" : "❌" }}, 
              입 {{ parseObservedInfo(image.observed_info).mouth_detected ? "✅" : "❌" }}
            </p>
          </li>
        </ul>
      </div>
      <p v-else>선택한 날짜에 감지된 기록이 없습니다.</p>
    </div>

    <BottomNavigation />
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      selectedDate: null, // 선택한 날짜
      images: [], // 감지된 이미지 목록
    };
  },
  methods: {
    async fetchImagesByDate(date) {
      this.selectedDate = date; // 선택한 날짜 저장
      try {
        const response = await axios.post("http://127.0.0.1:8000/api/history/images", {
          date: this.selectedDate,
        });

        console.log("서버 응답 데이터:", response.data); // 데이터 확인
        this.images = response.data || [];  // 데이터가 없을 경우 빈 배열로 처리

      } catch (error) {
        console.error("이미지 데이터를 불러오는 중 오류 발생:", error);
        this.images = [];
      }
    },
    formatTime(timestamp) {
      if (!timestamp) return "시간 없음";  // timestamp가 없을 경우 기본값 반환

      const date = new Date(timestamp);  // UTC 기준으로 생성된 Date 객체
      date.setHours(date.getHours() + 9);  // 한국 시간 (UTC+9)으로 변환

      // 시간만 HH:mm:ss 형식으로 추출
      const hours = String(date.getHours()).padStart(2, "0");
      const minutes = String(date.getMinutes()).padStart(2, "0");
      const seconds = String(date.getSeconds()).padStart(2, "0");
      
      return `${hours}:${minutes}:${seconds}`;  // 한국 시간(HH:mm:ss) 반환
    },
    parseObservedInfo(observedInfo) {
      try {
        return JSON.parse(observedInfo);
      } catch (e) {
        console.error("observed_info JSON 파싱 오류:", e);
        return { position: "알 수 없음", nose_detected: false, mouth_detected: false }; // 기본값
      }
    }
  },
};
</script>

<style scoped>
.history-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  padding: 2rem;  /* 2rem으로 변환 */
  font-family: Arial, sans-serif;
}

.image-list {
  margin-top: 2vh;  /* 화면 높이 비율로 margin-top 설정 */
  text-align: left;
  max-width: 90vw;  /* 화면 너비 비율로 max-width 설정 */
  margin-left: auto;
  margin-right: auto;
}

.image-list h3 {
  margin-bottom: 1rem;  /* 1rem으로 margin-bottom 설정 */
}

.image-list ul {
  list-style-type: none;
  padding: 0;
}

.image-list li {
  border: 0.1rem solid #ccc;  /* border 두께를 rem으로 설정 */
  padding: 1rem;  /* 패딩을 rem으로 설정 */
  margin-bottom: 2vh;  /* 화면 높이 비율로 margin-bottom 설정 */
  border-radius: 0.5rem;  /* border-radius를 rem으로 설정 */
  background-color: #B3DAF2;
  border : none;
}

.history-image {
  width: 100%;
  max-width: 80vw;  /* 이미지 최대 너비를 화면 너비 비율로 설정 */
  display: block;
  margin-bottom: 1.5vh;  /* 화면 높이 비율로 margin-bottom 설정 */
}
</style>

