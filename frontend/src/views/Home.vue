<!-- Home.vue -->
<template>
    <div class="home-container">
      <img src="@/assets/logo.png" alt="Safe Baby Logo" class="logo" />
      <p class="description">
        <strong>Safe Baby</strong>는 아기의 안전을 위해<br />
        실시간 모니터링 및 경고를 제공합니다.
      </p>
    </div>
</template>

<script>
export default {
  data() {
    return {
      showHome: false, // ✅ 처음에는 숨김
    };
  },
  mounted() {
    setTimeout(() => {
      this.showHome = true; // ✅ 2초 후에 홈 화면이 부드럽게 나타남
    }, 2000);
  },
};
</script>

<style scoped>

.home-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  width: 100%;
  height: calc(100vh - 8vh); 
  padding: 5vh 5vw;
  overflow-x: hidden; 
  box-sizing: border-box;
}

/* 반응형 로고 */
.logo {
  width: 30vw; 
  max-width: 15rem; 
  height: auto; 
}

.description {
  max-width: 80%; /* 부모 요소 대비 너비 설정 */
  margin-top: 3vh;
  font-size: 0.8rem;
  color: #70B4EC;
  padding: 1.5vh 2vw;
  border-radius: 1rem;
  border: 1px solid rgba(112, 180, 236, 0.5); 
  box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1); 
  text-align: center;
}

@media (max-width: 600px) {
  .logo {
    width: 50vw; /* 더 작은 화면에서는 50% 너비 */
  }
  .description {
    max-width: 85%;
    font-size: 1rem; /* 폰트 크기 조정 */
  }
}
</style>
