<template>
    <div class="auth-container">
      <form @submit.prevent="handleSignup">
        <div class="input-group">
          <label for="username">아이디</label>
          <input type="text" id="username" v-model="username" required />
        </div>
        <div class="input-group">
          <label for="email">이메일</label>
          <input type="email" id="email" v-model="email" required />
        </div>
        <div class="input-group">
          <label for="password">비밀번호</label>
          <input type="password" id="password" v-model="password" required />
        </div>
        <button type="submit" class="signup-button">회원가입</button>
      </form>
      <p class="switch-auth">
        이미 계정이 있으신가요? <router-link to="/login">로그인</router-link>
      </p>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  import api from "@/services/api";
  
  export default {
    data() {
      return {
        username: "",
        email: "",
        password: "",
      };
    },
    methods: {
      async handleSignup() {
        try {
          await api.post("backend/auth/signup/", {
            username: this.username,
            email: this.email,
            password: this.password,
          });
  
          alert("회원가입이 완료되었습니다! 로그인해주세요.");
          this.$router.push("/login");
        } catch (error) {
          alert("회원가입 실패: 이미 존재하는 계정입니다.");
        }
      },
    },
  };
  </script>
  
  <style scoped>
  .auth-container {
  text-align: center;
  padding: 5vh 5vw;
}

.input-group {
  margin: 2vh 0;
}

.input-group label {
  display: block;
  text-align: left;
  font-size: 1.2rem;
  margin-bottom: 0.5rem;
}

.input-group input {
  width: 80vw;
  max-width: 360px;
  padding: 1.2vh;
  border: 0.1rem solid #ccc;
  border-radius: 0.5rem;
  font-size: 1rem;
}

.signup-button {
  width: 80vw;
  max-width: 360px;
  padding: 1.5vh;
  background-color: #77C3F2;
  color: white;
  border: none;
  border-radius: 0.5rem;
  font-size: 1.2rem;
  margin-top: 1rem;
}

.switch-auth {
  margin-top: 2vh;
  font-size: 1rem;
  text-align: center;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.switch-auth a {
  font-weight: bold;
  color: #B3DAF2;
}

  </style>
  
