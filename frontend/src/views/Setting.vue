<template>
  <div class="settings-page">
    <!-- 상단 메뉴 리스트 -->

    <div class="menu-list">
      <router-link to="/account" class="menu-item">
        <span>Account</span>
        <font-awesome-icon :icon="['fas', 'chevron-right']" class="arrow-icon" />
      </router-link>
      <router-link to="/alert" class="menu-item">
        <span>Alerts & Notifications</span>
        <font-awesome-icon :icon="['fas', 'chevron-right']" class="arrow-icon" />
      </router-link>
      <router-link to="/videoset" class="menu-item">
        <span>Video Settings</span>
        <font-awesome-icon :icon="['fas', 'chevron-right']" class="arrow-icon" />
      </router-link>
      <router-link to="/privacy" class="menu-item">
        <span>Privacy & Terms</span>
        <font-awesome-icon :icon="['fas', 'chevron-right']" class="arrow-icon" />
      </router-link>
    </div>
  </div>
  
</template>

<script>
export default {
  name: "SettingsPage",
};
</script>

<style scoped>
/* 전체 컨테이너 */
.settings-page {
  position: relative;
  padding-bottom: 60px; /* 탭바 영역 확보 */
}

/* 메뉴 리스트 */
.menu-list {
  border-top: 1px solid #ccc;
  border-bottom: 1px solid #ccc;
}

/* 개별 메뉴 항목 */
.menu-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 10px;
  border-bottom: 1px solid #eee;
  text-decoration: none;
  color: black;
  font-size: 16px;
  transition: background-color 0.2s ease-in-out;
}

/* 마우스 호버 시 효과 */
.menu-item:hover {
  background-color: #f0f0f0;
}

/* 오른쪽 화살표 아이콘 */
.arrow-icon {
  color: #888;
}
</style>
