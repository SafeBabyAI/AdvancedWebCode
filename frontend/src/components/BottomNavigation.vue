<template>
    <nav class="bottom-nav">
      <router-link to="/" class="nav-item" active-class="active">
        <font-awesome-icon :icon="['fas', 'home']" />
      </router-link>
      <router-link to="/monitor" class="nav-item" active-class="active">
        <font-awesome-icon :icon="['fas', 'video']" />
      </router-link>
      <router-link to="/history" class="nav-item" active-class="active">
        <font-awesome-icon :icon="['fas', 'calendar']" />
      </router-link>
      <router-link to="/settings" class="nav-item" active-class="active">
        <font-awesome-icon :icon="['fas', 'cog']" />
      </router-link>
    </nav>
</template>
  
<style scoped>
.bottom-nav {
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 8vh; /* 네비게이션 바 높이를 화면 높이 비율로 설정 */
  display: flex;
  justify-content: space-around;
  align-items: center;
  background: #f8f8f8;
  padding: 1vh 0; /* 반응형 패딩 */
  border-top: 0.1rem solid #ddd; 
}

.nav-item {
  text-decoration: none;
  color: gray;
  font-size: 1.8rem; /* 상대적인 크기 설정 */
}

.nav-item svg {
  width: 1.8rem; /* 아이콘 크기 조정 */
  height: 1.8rem;
}

.active {
  color: #205A8C;
  font-weight: bold;
}
</style>