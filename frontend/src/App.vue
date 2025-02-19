<!-- App.vue -->
<script setup>
import BottomNavigation from "@/components/BottomNavigation.vue";
import TopNav from "@/components/TopNavigation.vue";
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
import BottomNavigation from "@/components/BottomNavigation.vue";

export default {
  components: {
    SplashScreen,
    BottomNavigation,
  },
  data() {
    return {
      showSplash: true, // 처음에는 스플래시 화면을 표시
    };
  },
  methods: {
    handleSplashEnd() {
      setTimeout(() => {
        this.showSplash = false; 
      }, 1000); // 살짝 딜레이 추가해서 더 자연스럽게 전환
    },
  },
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
