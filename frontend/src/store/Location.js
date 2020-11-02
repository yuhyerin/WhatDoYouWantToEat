const state = {
  lat: 0,
  lng: 0,
  dong: "",
};

const getters = {
  getLocation: function(state) {
    return state;
  },
};

const mutations = {
  setLocation: function(state, payload) {
    state.lat = payload.lat;
    state.lng = payload.lng;
    state.dong = payload.dong;
  },
};

export default {
  strict: process.env.NODE_ENV !== "production",
  state: {
    ...state,
  },
  getters,
  mutations,
  namespaced: true,
};
