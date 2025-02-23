import axios from "axios";
//Vue.js 프론트엔드에서 FasiAPI 백엔드와 통신할 때 쓰는 인스턴스 생성
const API_URL = process.env.VUE_APP_API_URL;
console.log("API_URL:", API_URL);

const api = axios.create({
  baseURL: API_URL, // "https://my-backend-api.azurewebsites.net", local, 배포 후 서버 주소
headers: {
    "Content-Type": "application/json", // JSON 데이터로 요청을 보냄
  },
});
export default api;
