<!-- SplashScreen -->
<template>
    <div class="splash-container" v-if="showSplash">
      <img src="@/assets/logo.png" alt="Safe Baby Logo" class="logo" />
    </div>
</template>
  
  <script>
  export default {
    data() {
      return {
        showSplash: true, // 처음에는 스플래시 화면을 표시
      };
    },
    mounted() {
      setTimeout(() => {
        this.showSplash = false; // ✅ 2초 후에 스플래시 화면을 숨김
        this.$emit("splashEnd"); // ✅ 부모 컴포넌트(App.vue)에서 화면 전환을 트리거
      }, 2000);
    },
  };
  </script>
  
<style scoped>

.splash-container {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    background: white;
    transition: opacity 1s ease-in-out;
    z-index: 9999;
}
.logo {
    width: 50vw;
    max-width: 200px;
}
</style>
  