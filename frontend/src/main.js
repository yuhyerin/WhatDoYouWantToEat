import Vue from "vue";
import App from "./App.vue";
import router from "./router.js";
import vuetify from "@/plugins/vuetify";
import { store } from "./store/store.js";
import * as firebase from "firebase";

import VueCookies from "vue-cookies";
Vue.use(VueCookies);

// import { store } from './store'

Vue.config.productionTip = false;

new Vue({
  router,
  vuetify,
  store,
  render: (h) => h(App),
  created() {
    firebase.initializeApp({
      apiKey: "AIzaSyBLLbDAcF_E4SIDDtT6sGd_BNHLtiudxZc",
      authDomain: "babygoat-aeb58.firebaseapp.com",
      databaseURL: "https://babygoat-aeb58.firebaseio.com",
      projectId: "babygoat-aeb58",
      storageBucket: "babygoat-aeb58.appspot.com",
      messagingSenderId: "320378947501",
      appId: "1:320378947501:web:9f4dddf54f047b380c4324",
      measurementId: "G-CYPY4K6VGB",
    });
  },
}).$mount("#app");
