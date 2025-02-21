<template> 
  <div class="account-page">
    <!-- 사용자 정보 카드 -->
    <div class="user-info-card">
      <p class="user-name">{{ username || "Guest" }}님</p>
      <p class="user-email">{{ email || "이메일 정보 없음" }}</p>
    </div>
    <!-- 로그아웃 버튼 -->
    <button class="logout-button" @click="logout">
      Log out
    </button>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "AccountPage",
  data() {
    return {
      username: "", // 사용자 이름
      email: "",    // 이메일
    };
  },
  methods: {
    async fetchUserInfo() {
      try {
        const token = localStorage.getItem("token");
        if (!token) {
          this.$router.push("/login");
          return;
        }

        const response = await axios.get("http://127.0.0.1:8000/auth/user/me", {
          headers: { Authorization: `Bearer ${token}` }
        });

        this.username = response.data.username;
        this.email = response.data.email;
      } catch (error) {
        console.error("사용자 정보 가져오기 실패:", error);
        // alert("사용자 정보를 불러오는데 실패했습니다. 다시 로그인 해주세요.");
        this.$router.push("/login");
      }
    },
    logout() {
      localStorage.removeItem("token"); // JWT 토큰 삭제
      this.$router.push("/login");
    },
  },
  mounted() {
    this.fetchUserInfo(); // 페이지 로드 시 사용자 정보 가져오기
  },
};
</script>

<style scoped>
.account-page {
  padding: 5vh 5vw;
  text-align: center;
}

.header {
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  margin-bottom: 3vh;
}

.back-button {
  position: absolute;
  left: 0;
  font-size: 1.5rem;
  background: none;
  border: none;
  cursor: pointer;
}

.account-title {
  font-size: 1.5rem;
  font-weight: bold;
}

.user-info-card {
  border: 0.1rem solid #ccc;
  border-radius: 1rem;
  padding: 2vh;
  display: inline-block;
  width: 80vw;
  background-color: white;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
  margin-bottom: 4vh;
}

.user-name {
  font-size: 1.2rem;
  font-weight: bold;
  margin: 0 0 0.5vh;
}

.user-email {
  font-size: 1rem;
  color: #333;
  margin: 0;
}

/* 로그아웃 버튼 스타일 */
.logout-button {
  border: 0.1rem solid #ff0000;
  color: #ff0000;
  background: transparent;
  padding: 1vh 3vw;
  border-radius: 2rem;
  cursor: pointer;
  font-size: 1rem;
}
.logout-button:hover {
  background-color: #ffe5e5;
}
</style>