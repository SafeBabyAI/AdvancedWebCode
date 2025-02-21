<template>
    <div v-if="showTopNav" class="top-nav">
      <button v-if="showBackButton" class="back-button" @click="$router.go(-1)">
        <font-awesome-icon :icon="['fas', 'chevron-left']" class="arrow-icon" />
      </button>
      <p>{{ pageTitle }}</p>
    </div>
  </template>
  
  <script>
  import { computed } from "vue";
  import { useRoute } from "vue-router";
  
  export default {
    setup() {
      const route = useRoute();
  
      // 페이지 제목 동적 설정
      const pageTitle = computed(() => {
        const titles = {
          "/monitor": "Monitoring",
          "/history": "History",
          "/settings": "Settings",
          "/login": "Login",
          "/account": "Account",
          "/videoset": "Video Settings",
          "/alert": "Alerts & Notifications",
          "/privacy": "Privacy & Terms",
        };
        return titles[route.path] || "";
      });
  
      // 홈 화면('/')에서는 TopNav를 숨김
      const showTopNav = computed(() => route.path !== "/");

      // 뒤로 가기 버튼을 표시할 조건 (예: '/monitor', '/history' 페이지 등)
      const showBackButton = computed(() => {
        const excludedPages = ["/monitor", "/history", "/settings", "/login", "/signup"];
        return !excludedPages.includes(route.path);
      });

      return { pageTitle, showTopNav, showBackButton };
    },
  };
  </script>
  
<style scoped>
/* Top Navigation Bar 스타일 */
.top-nav {
    text-align: center;
    font-size: 1.4rem;
    font-weight: bold;
    border-bottom: 1px solid #ddd;
}
.back-button {
  position: absolute;
  left: 10px;
  font-size: 1.5rem;
  background: none;
  border: none;
  cursor: pointer;
}
.arrow-icon {
  margin-top: 0.3rem;
  color: #888;
}
  </style>
  