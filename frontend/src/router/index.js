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

const routes = [
  { path: "/", component: Home },
  { path: "/monitor", component: Monitor },
  { path: "/history", component: History},
  { path: "/settings", component: Settings },
  { path: "/account", component: Account },
  { path: "/alert", component: Alert },
  { path: "/videoset", component: VideoSet },
  { path: "/privacy", component: Privacy },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
