import Vue from "vue";
import Vuex from "vuex";
import Location from "./Location";
import ShopList from "./ShopList";
import UserInfo from "./UserInfo";
import Server from "./Server";

import createPersistedState from "vuex-persistedstate";

import AuthModule from "./AuthModule";
import ChatModule from "./ChatModule";
import * as firebase from "firebase";

Vue.use(Vuex);
export const store = new Vuex.Store({
  modules: {
    location: Location,
    shopList: ShopList,
    userInfo: UserInfo,
    auth: AuthModule,
    chat: ChatModule,
    server: Server,
  },

  state: {
    loading: false,
    error: null,
    onlineUsers: [],
  },

  mutations: {
    setLoading(state, payload) {
      state.loading = payload;
    },
    setError(state, payload) {
      state.error = payload;
    },
    clearError(state) {
      state.error = null;
    },
    setOnlineUsers(state, payload) {
      state.onlineUsers = payload;
    },
  },

  actions: {
    loadOnlineUsers({ commit }) {
      firebase
        .database()
        .ref("presence")
        .on("value", function(snapshot) {
          let result = [];
          result[0] = snapshot.numChildren();
          result[1] = snapshot.val();
          commit("setOnlineUsers", result);
        });
    },
    clearError({ commit }) {
      commit("clearError");
    },
  },

  getters: {
    loading(state) {
      return state.loading;
    },
    error(state) {
      return state.error;
    },
    onlineUsers(state) {
      return state.onlineUsers;
    },
  },

  plugins: [createPersistedState()],
});
