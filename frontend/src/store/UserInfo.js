const state = {
  userAddress: [],
  isLogin: "",
  userType: "",
};

const getters = {
  getUserInfo: function(state) {
    return state;
  },
  getIsLogin: function(state) {
    return state.isLogin;
  },
  getUserType: function(state) {
    return state.userType;
  },
};

const mutations = {
  setUserInfo: function(state, payload) {
    state.userAddress = payload.userAddress;
  },
  setIsLogin: function(state, payload) {
    state.isLogin = payload.isLogin;
  },
  setUserType: function(state, payload) {
    console.log("setUserType is called");
    state.userType = payload.userType;
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
