<template>
  <v-main>
    <Header />
    <v-container>
      <h1>{{ this.storeInfo.store_name }}</h1>
      <v-card>
        <v-row>
          <v-col justify="center" lg="4" md="4">
            <div>
              <img
                :src="require(`@/assets/image/storelist/default.jpg`)"
                style="width: 75%;"
              />
            </div>
          </v-col>
          <v-col style="text-align: left;" lg="5" md="5">
            <div>
              <img
                src="../assets/image/placeholder.png"
                style="width:15px;"
                alt=""
              />
              {{ this.storeInfo.address }}
            </div>
            <div>
              <img
                src="../assets/image/category.png"
                style="width:15px;"
                alt=""
              />
              {{ this.storeInfo.bigcategory }}
            </div>
            <div>
              <img src="../assets/image/money.png" style="width:15px;" alt="" />
              {{ this.storeInfo.min_price }}원
            </div>
            <div>
              <img src="../assets/image/clock.png" style="width:15px;" alt="" />
              {{ this.businessDay }}
              {{ this.startTime }} -
              {{ this.endTime }}
            </div>
            <div>
              <img src="../assets/image/star.png" style="width:15px;" alt="" />
              {{ this.storeInfo.average_rating }}
            </div>
            <div style="display: flex; justify-content: start;"></div>
          </v-col>
          <v-col lg="3" md="3">
            <KakaoMap :storeData="this.storeInfo" />
          </v-col>
        </v-row>
      </v-card>
      <br />

      <v-row>
        <v-tabs v-model="tab" fixed-tabs color="orange accent-4">
          <v-tab @click="showContent(1)"
            ><img src="../assets/image/menu.png" alt="menu" width="35"
          /></v-tab>
          <v-tab class="review" @click="showContent(2)"
            ><img src="../assets/image/review.png" alt="review" width="35"
          /></v-tab>
          <v-tab class="party" @click="showContent(3)"
            ><img src="../assets/image/high-five.png" alt="party" width="35"
          /></v-tab>
        </v-tabs>
      </v-row>
      <v-row>
        <v-col>
          <div
            v-if="contentTrigger1"
            style="font-size: 50px; opacity: 0.5; color: rgb(49, 49, 49);"
          >
            <br />
            현재 메뉴를 준비중입니다.
          </div>
          <review v-if="contentTrigger2" />
          <party v-if="contentTrigger3" :storeInfo="storeInfo" />
        </v-col>
      </v-row>
    </v-container>
  </v-main>
</template>
<script>
// import StoreData from "../assets/datas/all_store_encoding2.json";
import Header from "../components/Header.vue";
import review from "../components/review.vue";
import party from "../components/party.vue";
import axios from "axios";
import KakaoMap from "../components/KakaoMap.vue";
import { mapGetters } from "vuex";

// const baseURL = "http://127.0.0.1:8000/";
const baseURL = "http://ec2-52-79-239-80.ap-northeast-2.compute.amazonaws.com/";

export default {
  components: {
    Header,
    KakaoMap,
    review,
    party,
  },
  data() {
    return {
      storeInfo: "",
      contentTrigger1: true,
      contentTrigger2: false,
      contentTrigger3: false,
      startTime: "",
      endTime: "",
      days: [],
      businessDay: "",
      imgUrl: "",
    };
  },
  created() {
    this.getStoreDetail();
  },
  computed: {
    ...mapGetters("server", ["getBaseURL"]),
  },
  methods: {
    changeEndTime(time) {
      if (time == "00:00:00") {
        this.endTime = "24:00";
      } else {
        this.endTime = time.substring(0, 5);
      }
    },

    getBusinessDay(day) {
      // 0: 휴무
      if (day.mon == 1 ? this.days.push("월") : this.days.push(0));
      if (day.tue == 1 ? this.days.push("화") : this.days.push(0));
      if (day.wed == 1 ? this.days.push("수") : this.days.push(0));
      if (day.thu == 1 ? this.days.push("목") : this.days.push(0));
      if (day.fri == 1 ? this.days.push("금") : this.days.push(0));
      if (day.sat == 1 ? this.days.push("토") : this.days.push(0));
      if (day.sun == 1 ? this.days.push("일") : this.days.push(0));

      // if (!this.days.includes(0)) {
      //   this.businessDay = "매일";
      // }
      for (var d in this.days) {
        if (this.days[d] != 0) this.businessDay += this.days[d] + ",";
      }
      if (this.businessDay == "월,화,수,목,금,") this.businessDay = "평일";
      else if (this.businessDay == "월,화,수,목,금,토,일,")
        this.businessDay = "매일";
      else if (this.businessDay == "토,일,") this.businessDay = "주말";
      else
        this.businessDay = this.businessDay.substring(
          0,
          this.businessDay.length - 1
        );
    },

    getStoreDetail() {
      axios
        .post(baseURL + `api/stores/${this.$route.params.storeid}/`, null, {
          headers: {
            Authorization: `Token ${this.$cookies.get("auth-token")}`,
          },
        }) // post > post
        .then((res) => {
          this.storeInfo = res.data;
          // this.imgUrl = require("../assets/image/storelist/" +
          //   this.storeInfo.store_name.replace(/(\s*)/g, "") +
          //   ".jpg");
          this.imgUrl = require("../assets/image/storelist/default.jpg");
          this.startTime = res.data.start_time.substring(0, 5);
          this.changeEndTime(res.data.end_time);
          this.getBusinessDay(res.data);
        })
        .catch((res) => {}); // post > post > then
    },

    showContent(num) {
      if (num == 1) {
        this.contentTrigger1 = true;
        this.contentTrigger2 = false;
        this.contentTrigger3 = false;
      } else if (num == 2) {
        this.contentTrigger1 = false;
        this.contentTrigger2 = true;
        this.contentTrigger3 = false;
      } else if (num == 3) {
        this.contentTrigger1 = false;
        this.contentTrigger2 = false;
        this.contentTrigger3 = true;
      }
    },
    // getStoreDetail() {
    //   for (var i = 0; i < StoreData.data.length; i++) {
    //     if (StoreData.data[i].store_id == this.$route.params.storeid) {
    //       this.storeInfo = StoreData.data[i];
    //     }
    //   }
    // },
  },
};
</script>
<style></style>
