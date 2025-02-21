import router from './router/index'; 

import { library } from "@fortawesome/fontawesome-svg-core";
import { faHome, faVideo, faCalendar, faCog, faVideoSlash, faBell, faCalendarAlt, faPen, faChevronRight, faArrowLeft, faChevronLeft } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'

// 여기에 개별 아이콘을 추가해야 함!
library.add(faHome, faVideo, faCalendar, faCog, faVideoSlash, faBell, faCalendarAlt, faPen, faChevronRight, faArrowLeft, faChevronLeft );

const app = createApp(App)

app.use(createPinia())
app.use(router);

app.component("font-awesome-icon", FontAwesomeIcon);
app.mount('#app')
