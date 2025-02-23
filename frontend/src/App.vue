<script setup>
import BottomNavigation from "@/components/BottomNavigation.vue";
import TopNav from "@/components/TopNavigation.vue";
import api from "@/services/api";
</script>

<template>
  <div id="app">
    <SplashScreen v-if="showSplash" @splashEnd="handleSplashEnd" />
    <TopNav v-if="!showSplash" />

    <router-view v-slot="{ Component }">
      <component :is="Component" v-if="!showSplash" />
    </router-view>

    <BottomNavigation v-if="!showSplash" />
  </div>
</template>

<script>
import SplashScreen from "@/components/SplashScreen.vue";
import axios from "axios";

export default {
  components: {
    SplashScreen,
  },
  data() {
    return {
      showSplash: true, // 처음에는 스플래시 화면을 표시
      isLoggedIn: false, // 로그인 여부
    };
  },
  methods: {
    async checkLogin() {
      const token = localStorage.getItem("token"); // 저장된 JWT 토큰 확인

      if (token) {
        try {
		const response = await api.get("backend/auth/check", {
            headers: { Authorization: `Bearer ${token}` },
          });

          if (response.status === 200) {
            this.isLoggedIn = true; // 로그인 성공
          } else {
            this.redirectToLogin();
          }
          console.log('로그인 확인')
        } catch (error) {
          console.error("로그인 확인 실패:", error);
          this.redirectToLogin();
        }
      } else {
        this.redirectToLogin();
      }
    },

    redirectToLogin() {
      this.isLoggedIn = false;
      this.$router.push("/login"); // 로그인 페이지로 이동
    },

    async handleSplashEnd() {
      setTimeout(async () => {
        await this.checkLogin(); // 로그인 여부 체크
        this.showSplash = false;
      }, 1000); // 스플래시 후 딜레이
    },
  },
  // mounted() {
  //   this.checkLogin(); // 앱이 시작될 때 자동 로그인 확인
  // },
};
</script>

<style>
#app {
  width: 100%;
  max-width: 100vw; 
  margin: 0;
  padding: 0;
  font-weight: normal;
  overflow-x: hidden; 
}
</style>
