<template>
  <div class="flip">
    <div
      class="front"
      :style="{ backgroundImage: `url(` + imgUrl + `),url(` + second + `)` }"
    >
      <h1 class="text-shadow">{{ this.storeData.store_name }}</h1>
    </div>
    <div class="back">
      <h2>{{ this.storeData.store_name }}</h2>
      <p>별점 : {{ parseInt(this.storeData.average_rating) }}</p>
      <v-btn @click="goToShopDetail()">가게보러가기</v-btn>
    </div>
  </div>
</template>
<script>
import axios from "axios";
import { mapGetters } from "vuex";

// const baseURL = "http://127.0.0.1:8000/";
const baseURL = "http://ec2-52-79-239-80.ap-northeast-2.compute.amazonaws.com/";

export default {
  props: {
    storeData: {},
  },
  data() {
    return {
      imgUrl: "",
      data: {
        category: "",
      },
      storeId: "",
      second: require("../assets/image/storelist/default.jpg"),
    };
  },
  components: {},
  computed: {
    ...mapGetters("server", ["getBaseURL"]),
  },

  created: function() {
    this.imgUrl = require("../assets/image/storelist/" +
      this.storeData.store_name.replace(/(\s*)/g, "") +
      ".jpg");
    // console.log(this.imgUrl);
    // this.imgUrl = require("../assets/image/storelist/default.jpg");
  },

  methods: {
    goToShopDetail() {
      // console.log("this.storeData.store_id", this.storeData.store_id);
      this.$router.push("/storedetail/" + this.storeData.store_id);
      // this.$router.push("/storedetail/", {
      //   params: {
      //     store_id: this.storeData.store_id,
      //     store_user_id: this.storeData.user_id,
      //   },
      // });
    },
    showShopList: function() {
      axios
        .post(
          baseURL + "api/stores/store_category/",
          {
            category: this.$route.params.category,
          },
          {
            headers: {
              Authorization: `Token ${this.$cookies.get("auth-token")}`,
            },
          }
        ) // post > post
        .then((res) => {
          this.userInfo = res.data;
        })
        .catch((res) => {
          console.log("user Address error", res);
        }); // post > post > then
    },
  },
};
</script>

<style lang="scss" scoped src="../assets/css/Card.scss"></style>
