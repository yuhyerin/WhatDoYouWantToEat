<template>
  <v-app-bar app style="box-shadow:none;">
    <v-toolbar-title>
      <router-link
        style="text-decoration: none; color: rgb(233,105,30); display:flex; align-items: center;"
        to="/home"
      >
        <img
          style="height:65px; width: 65px;"
          src="../assets/image/home1.png"
        />
      </router-link>
    </v-toolbar-title>
    <v-spacer />
    <v-toolbar-title>
      <v-col>
        <v-select
          @change="changeAddress"
          v-model="initLocation"
          :items="userInfo"
          item-text="location"
          style="margin:10px; margin-top:25px; width:250px;"
          color="rgb(233,105,30)"
          item-color="none"
        />
      </v-col>
    </v-toolbar-title>
    <button @click="findAddress()">추가하기</button>
    <v-spacer />
    <v-toolbar-title>
      <div
        v-if="
          $cookies.get('auth-token') === null ||
            $cookies.get('auth-token') === ''
        "
      >
        <button @click="login()"><h2>login</h2></button>
      </div>
      <div v-else>
        <button @click="logout()"><h2>logout</h2></button>
      </div>
    </v-toolbar-title>
  </v-app-bar>
</template>

<script src="http://dmaps.daum.net/map_js_init/postcode.v2.js"></script>
<script src="//dapi.kakao.com/v2/maps/sdk.js?appkey=48cbffa8392e1a7acffc1975347ec0d3&libraries=services"></script>

<script>
import user from "../assets/datas/user.json";
import { mapGetters, mapMutations } from "vuex";
import { EventBus } from "../utils/EventBus.js";
import * as firebase from "firebase";
import axios from "axios";

// const baseURL = "http://127.0.0.1:8000/";
const baseURL = "http://ec2-52-79-239-80.ap-northeast-2.compute.amazonaws.com/";

export default {
  data() {
    return {
      initLocation: "",
      userInfo: [],
      showAddrModal: false,
      seletedAddress: "",
      isLogined: false,
      newAddress: "",
      AddrTrigger: false,
    };
  },
  components: {},
  computed: {
    ...mapGetters("location", ["getLocation"]),
    ...mapGetters("userInfo", ["getUserInfo"]),
    ...mapGetters("userInfo", ["getUserType"]),
    ...mapGetters("server", ["getBaseURL"]),
  },

  created() {
    this.getUserAddress();
    // console.log("isAdmin?", this.getUserType);
  },

  mounted() {
    window.kakao && window.kakao.maps ? null : this.addScript();
  },

  methods: {
    ...mapMutations(("location", ["setLocation"])),
    ...mapMutations(("userInfo", ["setUserInfo"])),

    addAddress: function() {
      axios
        .post(
          baseURL + "api/accounts/user_order/",
          {
            location: this.newAddress,
          },
          {
            headers: {
              Authorization: `Token ${this.$cookies.get("auth-token")}`,
            },
          }
        ) // post > post
        .then((res) => {
          // console.log(res.data);
        })
        .catch((res) => {
          console.log(res);
        }); // post > post > then
    },

    changeAddress: function() {
      this.searchAddr();
      this.$store.commit("userInfo/setUserInfo", {
        userAddress: this.initLocation,
      });
    },

    logout() {
      firebase
        .auth()
        .signOut()
        .then(() => {
          this.$cookies.remove("auth-token");
          this.$router.push("/");
        });

      this.$store.commit("userInfo/setUserInfo", {
        userAddress: "",
      });
      localStorage.setItem("isLogin", false);
      this.initLocation = "";
    },

    getUserAddress() {
      this.initLocation = this.getUserInfo.userAddress;
      axios
        .post(baseURL + "api/accounts/user_order_list/", null, {
          headers: {
            Authorization: `Token ${this.$cookies.get("auth-token")}`,
          },
        }) // post > post
        .then((res) => {
          this.userInfo = res.data;
        })
        .catch((res) => {
          console.log("user Address error", res);
        }); // post > post > then
      this.searchAddr();
    },

    addScript() {
      let script = document.createElement("script");
      /* global kakao */

      script.onload = () => kakao.maps.load(this.initMap);
      script.src =
        "https://dapi.kakao.com/v2/maps/sdk.js?autoload=false&appkey=a7bd2d0df8f5ae53b0c5e106842b94fd&libraries=services";
      document.head.appendChild(script);
    },

    searchAddr() {
      var geocoder = new kakao.maps.services.Geocoder();

      geocoder.addressSearch(this.initLocation, (result, status) => {
        if (status === kakao.maps.services.Status.OK) {
          this.$store.commit("location/setLocation", {
            lat: result[0].y,
            lng: result[0].x,
            dong: result[0].address.region_3depth_name,
          });
        }
      });
    },

    login() {
      this.$router.push("/");
    },

    findAddress() {
      new daum.Postcode({
        oncomplete: (data) => {
          var fullAddr = data.address;
          var extraAddr = "";

          if (data.addressType === "R") {
            if (data.bname !== "") {
              extraAddr += data.bname;
            }
            if (data.buildingName !== "") {
              extraAddr +=
                extraAddr !== "" ? ", " + data.buildingName : data.buildingName;
            }
            fullAddr += extraAddr !== "" ? " (" + extraAddr + ")" : "";
          }

          axios
            .post(
              baseURL + "api/accounts/user_order/",
              {
                location: fullAddr,
              },
              {
                headers: {
                  Authorization: `Token ${this.$cookies.get("auth-token")}`,
                },
              }
            ) // post > post
            .then((res) => {
              location.reload();
            })
            .catch((res) => {
              console.log(res);
            }); // post > post > then
        },
      }).open({});
    },
  },
};
</script>
<style>
.address {
  margin-top: 25px;
}
button {
  color: rgb(233, 105, 30);
}
</style>
