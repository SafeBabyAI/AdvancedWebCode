//Vue Router 사용
import { createRouter, createWebHistory } from "vue-router";
import Home from "@/views/Home.vue";
import Monitor from "@/views/Monitor.vue";
import History from "@/views/History.vue";
import Settings from "@/views/Settings.vue";

const routes = [
  { path: "/", component: Home },
  { path: "/monitor", component: Monitor },
  { path: "/history", component: History},
  { path: "/settings", component: Settings }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
