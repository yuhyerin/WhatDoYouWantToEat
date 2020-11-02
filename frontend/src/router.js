import Vue from "vue";
import Router from "vue-router";

Vue.use(Router);

import Login from "./pages/LogIn.vue";
import Content from "./pages/Content.vue";
import StoreList from "./pages/StoreList.vue";
import StoreDetail from "./pages/StoreDetail.vue";
import Signin from "@/components/User/Signin";
import test from "@/components/test.vue";
import HyerinChat from "./pages/HyerinChat.vue";
import Create from "./components/HyerinChat/Create.vue";
// import UserInfo from "./store/UserInfo.js";
import store from "@/store/store.js";
import { mapGetters, mapMutations } from "vuex";

const requireAuth = (to, from, next) => {
  if (localStorage.getItem("isLogin") === "true") {
    next();
  } else {
    alert("로그인이 필요합니다.");
    next("/");
  }
};

export default new Router({
  mode: "history",
  routes: [
    {
      path: "/home",
      name: "Home",
      beforeEnter: requireAuth,
      component: Content,
    },
    {
      path: "/",
      name: "Login",
      component: Login,
    },
    {
      path: "/storelist/:bigcategory",
      name: "storelist",
      component: StoreList,
      beforeEnter: requireAuth,
    },
    {
      path: "/storedetail/:storeid",
      name: "storedetail",
      component: StoreDetail,
      beforeEnter: requireAuth,
    },
    {
      path: "/create/:storeid",
      name: "CreateChat",
      component: Create,
      beforeEnter: requireAuth,
    },
    {
      path: "/loginChat",
      name: "Signin",
      component: Signin,
      beforeEnter: requireAuth,
    },
    {
      path: "/test",
      name: "test",
      component: test,
      beforeEnter: requireAuth,
    },
    {
      path: "/hrchat/:roomNumber/:roomName",
      name: "HyerinChat",
      component: HyerinChat,
      beforeEnter: requireAuth,
    },
  ],
});
