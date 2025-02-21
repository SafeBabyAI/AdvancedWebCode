//Vue Router 사용
import { createRouter, createWebHistory } from "vue-router";
import Home from "@/views/Home.vue";
import Monitor from "@/views/Monitor.vue";
import History from "@/views/History.vue";
import Settings from "@/views/Setting.vue";
import Account from "@/views/Account.vue";
import Alert from "@/views/Alert.vue";
import VideoSet from "@/views/VideoSet.vue";
import Privacy from "@/views/Privacy.vue";
import Signup from "@/views/Signup.vue";
import Login from "@/views/Login.vue";

const routes = [
  { path: "/", component: Home },
  { path: "/monitor", component: Monitor, meta: { requiresAuth: true } },
  { path: "/history", component: History, meta: { requiresAuth: true } },
  { path: "/settings", component: Settings, meta: { requiresAuth: true } },
  { path: "/account", component: Account, meta: { requiresAuth: true } },
  { path: "/alert", component: Alert, meta: { requiresAuth: true } },
  { path: "/videoset", component: VideoSet, meta: { requiresAuth: true } },
  { path: "/privacy", component: Privacy, meta: { requiresAuth: true } },
  { path: "/login", component: Login },
  { path: "/signup", component: Signup },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// 인증된 사용자만 특정 페이지 접근 가능하도록 설정
router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem("token");
  if (to.matched.some(record => record.meta.requiresAuth) && !isAuthenticated) {
    next("/login"); // 인증되지 않은 사용자는 로그인 페이지로 리디렉션
  } else {
    next();
  }
});

export default router;
