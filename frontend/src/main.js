import router from './router/index';

import { library } from "@fortawesome/fontawesome-svg-core";
import { faHome, faVideo, faCalendar, faCog, faVideoSlash, faBell, faCalendarAlt, faPen, faChevronRight, faArrowLeft, faChevronLeft } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
//import './registerServiceWorker'

// 여기에 개별 아이콘을 추가해야 함!
library.add(faHome, faVideo, faCalendar, faCog, faVideoSlash, faBell, faCalendarAlt, faPen, faChevronRight, faArrowLeft, faChevronLeft );

const app = createApp(App)

app.use(createPinia())
app.use(router);

app.component("font-awesome-icon", FontAwesomeIcon);

// 서비스 워커 등록
/*if (process.env.NODE_ENV === 'production') {
    if ('serviceWorker' in navigator) {
      window.addEventListener('load', () => {
        navigator.serviceWorker
          .register('/service-worker.js')  // 서비스 워커 파일을 등록
          .then(registration => {
            console.log('Service Worker registered with scope: ', registration.scope);
          })
          .catch(error => {
            console.log('Service Worker registration failed: ', error);
          });
      });
    }
  }
  */
app.mount('#app');
