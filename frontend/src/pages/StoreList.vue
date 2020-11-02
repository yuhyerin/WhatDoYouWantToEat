<template>
  <v-app>
    <Header />
    <v-main>
      <v-container>
        <v-row>
          <v-flex>{{ $route.params.bigcategory }}</v-flex>
          <v-flex>{{ dong }}</v-flex>
        </v-row>

        <v-row
          v-if="storeList.length > 0"
          style="display: flex; align-items: center; text-align: center;"
        >
          <div v-for="(item, index) in storeList" :key="index" :index="index">
            <v-row style="margin: 10px; width: fit-content;">
              <Card v-bind:storeData="item" />
            </v-row>
          </div>
        </v-row>
        <div v-else style="flex: auto;">
          <div class="flip">
            <div
              class="front"
              style="display: flex; justify-content: center; align-items: center;"
            >
              <h1 class="text-shadow">결과가 없습니다.</h1>
            </div>
            <div
              class="back"
              style="display: flex; justify-content: center; align-items: center;"
            >
              <v-btn to="/home">돌아가기</v-btn>
            </div>
          </div>
        </div>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import axios from "axios";
// import kakaoMap from "../components/KakaoMap.vue";
import { mapGetters } from "vuex";
import Header from "../components/Header.vue";
import Card from "../components/Card.vue";

// const baseURL = "http://127.0.0.1:8000/";
const baseURL = "http://ec2-52-79-239-80.ap-northeast-2.compute.amazonaws.com/";

export default {
  data() {
    return {
      storeList: "",
      data: {
        loc: 0,
        category: "",
      },
    };
  },
  components: {
    // kakaoMap,
    Header,
    Card,
  },

  computed: {
    ...mapGetters("location", ["getLocation"]),
    ...mapGetters("server", ["getBaseURL"]),
    dong() {
      return this.getLocation.dong;
    },
  },

  created: async function() {
    this.loc = this.getLocation;
    this.category = this.$route.params.bigcategory;
    await this.getStoreInfo();
  },

  watch: {
    dong(newCount, oldCount) {
      axios
        .post(
          baseURL + "api/stores/store_bigcategory/",
          {
            bigcategory: this.category,
            user_location: newCount,
          },
          {
            headers: {
              Authorization: `Token ${this.$cookies.get("auth-token")}`,
            },
          }
        ) // post > post
        .then((res) => {
          this.storeList = res.data;
        })
        .catch((res) => {
          console.log(res);
        }); // post > post > then
    },
  },

  methods: {
    test() {},
    async getStoreInfo() {
      await axios
        .post(
          baseURL + "api/stores/store_bigcategory/",
          {
            bigcategory: this.category,
            user_location: this.getLocation.dong,
          },
          {
            headers: {
              Authorization: `Token ${this.$cookies.get("auth-token")}`,
            },
          }
        ) // post > post
        .then((res) => {
          this.storeList = res.data;
        })
        .catch((res) => {
          console.log(res);
        }); // post > post > then
    },
  },
};
</script>
<style lang="scss" scoped src="../assets/css/Card.scss">
.shopList {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
}
</style>
