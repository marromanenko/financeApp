import Vue from "vue";
import VueRouter from "vue-router";
import Auth from "../components/pages/Auth.vue"
import Register from "../components/pages/Register.vue"
import About from "../components/pages/About.vue"
import Main from "../components/pages/Main.vue"
import Profile from "../components/pages/Profile.vue"
import Chat from "../components/pages/Chat.vue"
import Result from "../components/pages/Result.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/about",
    name: "about",
    component: About
  },
  {
    path: "/login",
    name: "auth",
    component: Auth
  },
  {
    path: "/register",
    name: "register-page",
    component: Register
  },
  {
    path: "/main",
    name: "main-page",
    component: Main
  },
  {
    path: "/profile",
    name: "profile-page",
    component: Profile
  },
  {
    path: "/chat",
    name: "chat-page",
    component: Chat
  },
  {
    path: "/result",
    name: "result",
    component: Result
  }
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

router.beforeEach((to, from, next) => {
  document.title = to.name.charAt(0).toUpperCase() + to.name.slice(1);
  next();
});

export default router;
