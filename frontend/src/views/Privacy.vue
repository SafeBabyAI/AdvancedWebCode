<template>
    <div class="privacy-container">
      <!-- 🔹 헤더 (뒤로가기 + 제목) -->
      <div class="header">
        <button @click="$router.go(-1)" class="back-button">
          <font-awesome-icon :icon="['fas', 'arrow-left']" />
        </button>
        <h2>Privacy & Terms</h2>
      </div>
  
      <!-- 🔹 정책 본문 -->
      <div class="content">
        <h3>Privacy Policy & Terms of Use</h3>
        <p class="updated-date">Last Updated: 2025.02.19</p>
  
        <!-- 🔹 정책 목록 -->
        <div class="policy-section" v-for="(section, index) in policies" :key="index">
          <h4>{{ index + 1 }}. {{ section.title }}</h4>
          <ul>
            <li v-for="(item, idx) in section.details" :key="idx">{{ item }}</li>
          </ul>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        policies: [
          {
            title: "데이터 수집 및 사용",
            details: [
              "본 애플리케이션은 아기의 안전한 모니터링을 위해 카메라를 통한 실시간 영상 처리를 수행합니다.",
              "수집된 영상 데이터는 기기 내에서만 처리되며, 외부 서버로 전송되거나 저장되지 않습니다.",
              "위험 상황 감지 시 알림 기능 제공을 위해 필요한 최소한의 권한만을 요청합니다.",
            ],
          },
          {
            title: "보안",
            details: [
              "모든 영상 처리는 사용자의 로컬 기기에서만 이루어집니다.",
              "실시간 스트리밍 데이터는 암호화되어 처리됩니다.",
              "애플리케이션은 권한이 있는 사용자만 접근할 수 있도록 설계되었습니다.",
            ],
          },
          {
            title: "카메라 사용 권한",
            details: [
              "본 애플리케이션은 아기 모니터링을 위해 카메라 접근 권한이 필요합니다.",
              "카메라 권한은 앱 사용 중에만 활성화되며, 사용자가 언제든지 설정에서 변경할 수 있습니다.",
            ],
          },
          {
            title: "책임 제한",
            details: [
              "본 애플리케이션은 보조적인 모니터링 도구로서, 직접적인 육아 감독을 대체할 수 없습니다.",
              "항상 보호자의 직접적인 관찰과 함께 사용되어야 합니다.",
              "기술적 문제나 오작동으로 인한 미감지 가능성이 있음을 인지하시기 바랍니다.",
            ],
          },
          {
            title: "데이터 저장",
            details: [
              "알림 기록을 제외한 영상 데이터는 저장되지 않습니다.",
              "사용자의 설정 정보만 로컬 기기에 저장됩니다.",
            ],
          },
        ],
      };
    },
  };
  </script>
  
  <style scoped>
  /* ✅ 전체 컨테이너 스타일 */
  .privacy-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20px;
    font-family: Arial, sans-serif;
  }
  
  /* ✅ 헤더 스타일 */
  .header {
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 10px 0;
    font-size: 20px;
  }
  
  .back-button {
    background: none;
    border: none;
    font-size: 20px;
    cursor: pointer;
  }
  
  /* ✅ 본문 스타일 */
  .content {
    width: 100%;
    max-width: 600px;
    padding: 10px;
    text-align: left;
  }
  
  .updated-date {
    font-size: 14px;
    color: #777;
    margin-bottom: 15px;
  }
  
  /* ✅ 정책 섹션 스타일 */
  .policy-section {
    margin-bottom: 20px;
  }
  
  .policy-section h4 {
    font-size: 16px;
    font-weight: bold;
    margin-bottom: 5px;
  }
  
  .policy-section ul {
    list-style-type: disc;
    padding-left: 20px;
  }
  
  .policy-section ul li {
    font-size: 14px;
    color: #333;
    margin-bottom: 5px;
  }
  </style>
  