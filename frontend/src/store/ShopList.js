const state = {
  shopList: [],
};

const getters = {
  getShopList: function(state) {
    return state;
  },
};

const mutations = {
  setShopList: function(state, payload) {
    state = payload;
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
