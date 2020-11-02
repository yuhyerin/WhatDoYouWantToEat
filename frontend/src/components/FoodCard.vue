<template>
  <div class="flip" style="width: 18vw;">
    <div class="front" :style="{ backgroundImage: `url(` + imgUrl + `)` }">
      <h1 class="text-shadow">{{ this.categoryData.cat_title }}</h1>
    </div>
    <div class="back">
      <h2>{{ this.categoryData.cat_title }}</h2>
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
    categoryData: {},
  },
  data() {
    return {
      imgUrl: "",
      data: {
        category: "",
      },
      storeId: "",
    };
  },
  components: {},
  created: function() {
    // this.imgUrl = require("../assets/image/storelist/" +
    //   this.storeData.store_name.replace(/(\s*)/g, "") +
    //   ".jpg");
    // console.log(this.imgUrl);
    this.imgUrl = require(`../assets/category/${this.categoryData.cat_title}.jpg`);
  },

  computed: {
    ...mapGetters("location", ["getLocation"]),
    ...mapGetters("server", ["getBaseURL"]),
  },

  methods: {
    goToShopDetail() {
      this.$router.push("/storelist/" + this.categoryData.cat_title);
      // this.showShopList();
    },
    // showShopList: function() {
    //   axios
    //     .post(
    //       baseURL + "api/stores/store_bigcategory/",
    //       {
    //         bigcategory: this.categoryData.cat_title,
    //         user_location: this.getLocation.dong,
    //       },
    //       {
    //         headers: {
    //           Authorization: `Token ${this.$cookies.get("auth-token")}`,
    //         },
    //       }
    //     ) // post > post
    //     .then((res) => {
    //       console.log("hihihihi", res.data);
    //     })
    //     .catch((res) => {
    //       console.log("user Address error", res);
    //     }); // post > post > then
    // },
  },
};
</script>

<style lang="scss" scoped src="../assets/css/Card.scss"></style>
