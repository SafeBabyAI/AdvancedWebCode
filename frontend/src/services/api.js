import axios from "axios";
//Vue.js 프론트엔드에서 FasiAPI 백엔드와 통신할 때 쓰는 인스턴스 생성

const api = axios.create({
  baseURL: "http://localhost:8000", // "https://my-backend-api.azurewebsites.net", local, 배포 후 서버 주소
});

export default api;
