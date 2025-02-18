<script setup>
import HelloWorld from './components/HelloWorld.vue'
import TheWelcome from './components/TheWelcome.vue'
</script>

<template>
  <div class="container">
    <h1>FastAPI와 Vue.js 통신</h1>
    
    <video ref="video" autoplay></video>
    <button @click="captureImage">사진 찍기</button>
    <canvas ref="canvas" style="display: none;"></canvas>
    <button @click="sendImage">FastAPI로 전송</button>
    <p v-if="responseData">분석 결과: {{ responseData.alert }}</p>
  </div>
  <!-- <div>
    <h1>FastAPI와 Vue.js 통신</h1>
    <input v-model="inputData" placeholder="보낼 데이터 입력" />
    <button @click="sendData">데이터 전송</button>
    <p>응답: {{ responseData }}</p>
  </div> -->
</template>

<script>
import api from "@/services/api";  // FastAPI와 통신하는 axios 객체

export default {
  data() {
    return {
      responseData: null,
    };
  }, 
  mounted() {
    this.initCamera();
  },
  methods: {
    async initCamera() {
      const constraints = { video: true };
      try {
        const stream = await navigator.mediaDevices.getUserMedia(constraints);
        this.$refs.video.srcObject = stream;
      } catch (error) {
        console.error("웹캠 접근 실패:", error);
      }
    },
    captureImage() {
      const canvas = this.$refs.canvas;
      const video = this.$refs.video;
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      canvas.getContext("2d").drawImage(video, 0, 0, canvas.width, canvas.height);
    },
    async sendImage() {
      const canvas = this.$refs.canvas;
      canvas.toBlob(async (blob) => {
        const formData = new FormData();
        formData.append("file", blob, "image.jpg");

        try {
          const response = await api.post("/predict/", formData, {
            headers: { "Content-Type": "multipart/form-data" },
          });
          this.responseData = response.data;
        } catch (error) {
          console.error("API 요청 실패:", error);
        }
      }, "image/jpeg");
    },
    // async sendData() {
    //   try {
    //     const response = await api.post("/data", { data: this.inputData }); // FastAPI에 데이터 전송
    //     this.responseData = response.data; // 응답 데이터를 저장
    //   } catch (error) {
    //     console.error("API 요청 실패:", error);
    //   }
    // },
  },
};
</script>
<style>
.container {
  text-align: center;
}
video {
  width: 100%;
  max-width: 640px;
}
</style>
<!-- <style scoped>
header {
  line-height: 1.5;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }
}
</style> -->
