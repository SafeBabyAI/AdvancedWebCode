<template>
    <div v-if="showTopNav" class="top-nav">
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
        };
        return titles[route.path] || "";
      });
  
      // 홈 화면('/')에서는 TopNav를 숨김
      const showTopNav = computed(() => route.path !== "/");
  
      return { pageTitle, showTopNav };
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
    background: white;
  }
  </style>
  