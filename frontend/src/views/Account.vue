<template>
    <div class="account-page">
      <!-- 상단 제목 -->
      <h2 class="account-title">Account</h2>
  
      <!-- 사용자 정보 카드 -->
      <div class="user-info-card">
        <p class="user-name">김**님</p>
        <p class="user-email">abcd11@gmail.com</p>
      </div>
  
      <!-- 로그아웃 버튼 -->
      <button class="logout-button" @click="logout">
        Log out
      </button>
    </div>
  </template>
  
  <script>
  export default {
    name: "AccountPage",
    methods: {
      logout() {
        // 실제 로그아웃 로직(토큰 삭제, 페이지 이동 등) 추가
        console.log("Log out clicked");
      },
    },
  };
  </script>
  
  <style scoped>
  .account-page {
    padding: 20px;
    text-align: center;
    /* 하단 탭바가 있다면 아래 여백도 고려 (예: padding-bottom: 60px;) */
  }
  
  .account-title {
    margin-bottom: 20px;
    font-size: 24px;
  }
  
  .user-info-card {
    border: 1px solid #ccc;
    border-radius: 10px;
    padding: 15px;
    display: inline-block; /* 내용만큼만 카드가 감싸도록 */
    margin-bottom: 30px;
  }
  .user-name {
    font-size: 18px;
    font-weight: bold;
    margin: 0 0 5px;
  }
  .user-email {
    font-size: 14px;
    color: #666;
    margin: 0;
  }
  
  /* 로그아웃 버튼 스타일 */
  .logout-button {
    border: 1px solid #ff0000;
    color: #ff0000;
    background: transparent;
    padding: 10px 20px;
    border-radius: 20px;
    cursor: pointer;
    font-size: 16px;
  }
  .logout-button:hover {
    background-color: #ffe5e5;
  }
  </style>
  