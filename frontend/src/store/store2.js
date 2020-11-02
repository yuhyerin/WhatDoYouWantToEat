import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

export const store = new Vuex.Store({
  state: {
    lat: 1,
    lng: 2,
  },
  getters: {
    getLocation: function(state) {
      return state;
    },
  },
  mutations: {
    setLocation: function(state, payload) {
      state.lat = payload.lat;
      state.lng = payload.lng;
    },
  },
});
