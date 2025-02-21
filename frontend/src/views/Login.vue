<template>
  <div class="auth-container">
    <form @submit.prevent="login">
      <div class="input-group">
        <label for="username">아이디</label>
        <input type="text" id="username" v-model="username" required />
      </div>
      <div class="input-group">
        <label for="password">비밀번호</label>
        <input type="password" id="password" v-model="password" required />
      </div>
      <!-- 로그인 실패 시 오류 메시지 표시 -->
      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>

      <button type="submit" class="login-button">로그인</button>
    </form>
    <div class="signup-prompt">
      <p>아직 회원이 아니신가요?</p>
      <button @click="$router.push('/signup')" class="signup-button">회원가입</button>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      username: "",
      password: "",
      errorMessage: "", // 에러 메시지를 저장할 변수
    };
  },
  methods: {
    async login() {
      this.errorMessage = ""; 
      try {
        const response = await axios.post("http://127.0.0.1:8000/auth/login", {
          username: this.username,
          password: this.password,
        });
        console.log(response.data.access_token)
        localStorage.setItem("token", response.data.access_token); // 토큰 저장
        this.$router.push("/"); // 로그인 성공 -> 홈으로 리다이렉션 
      } catch (error) {
        console.error("로그인 실패:", error);
        if (error.response && error.response.data) {
          this.errorMessage = error.response.data.detail; // 서버에서 받은 메시지를 errorMessage에 저장
        } else {
          this.errorMessage = "서버 오류가 발생했습니다. 다시 시도해주세요.";
        }
      }
    },
  },
};
</script>

<style scoped>
.auth-container {
  text-align: center;
  padding: 2vh;
}

.input-group {
  margin: 2vh 0;
}

.input-group label {
  display: block;
  text-align: left;
  font-size: 1.2rem;
  margin-bottom: 0.7rem;
}

.input-group input {
  width: 80vw;
  max-width: 400px;
  padding: 1vh;
  border: 0.1rem solid #ccc;
  border-radius: 0.5rem;
  font-size: 1rem;
}

.login-button {
  width: 85vw;
  max-width: 400px;
  padding: 1.5vh;
  background-color: #77C3F2;
  color: white;
  margin-top: 1.2rem;
  border: none;
  border-radius: 0.5rem;
  font-size: 1.2rem;
}

.signup-prompt {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 1rem;
  text-align: center;
  margin-top: 2vh;
}

.signup-button {
  padding: 1vh 2vh;
  font-size: 1rem;
  background-color: white;
  color: #B3DAF2;
  border: none;
  border-radius: 0.5rem;
  cursor: pointer;
}

.error-message {
  color: red;
  font-size: 1rem;
  margin-top: 3vh;
}
</style>