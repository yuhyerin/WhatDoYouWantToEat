<template>
  <v-container v-on:scroll="onScroll" ref="chatlistContainer">
    <v-main style="margin: 0; padding: 0;">
      <v-row style="margin: 0;" no-gutters>
        <v-col
          v-for="(chat, index) in chatList"
          :index="index"
          :key="chat.room_name"
          cols="12"
          sm="4"
        >
          <div class="chatlist">
            <img :src="chattingIMG[num[index]]" alt="" />
            <div class="title">
              <h1>{{ chat.room_name }}</h1>
              <p>주소주소</p>
            </div>
            <v-btn
              style="width: 80%; color: white;"
              color="black"
              @click="mvtochatting(chat)"
              >참가하기</v-btn
            >
          </div>
        </v-col>
      </v-row>
    </v-main>
  </v-container>
</template>

<script>
import axios from "axios";
import { mapGetters } from "vuex";
// const baseURL = "http://127.0.0.1:8000/";
const baseURL = "http://ec2-52-79-239-80.ap-northeast-2.compute.amazonaws.com/";

export default {
  props: {
    store_id: [],
  },
  data() {
    return {
      chatList: [],
      loading: false,
      chattingIMG: [
        require("../../assets/image/chattingroom/diet.png"),
        require("../../assets/image/chattingroom/eat.png"),
        require("../../assets/image/chattingroom/foodtray.png"),
        require("../../assets/image/chattingroom/messenger.png"),
        require("../../assets/image/chattingroom/roomservice.png"),
        require("../../assets/image/chattingroom/sale.png"),
        require("../../assets/image/chattingroom/team.png"),
        require("../../assets/image/chattingroom/tray.png"),
      ],
      num: [],
    };
  },
  mounted() {
    // 여기서 ldj_loadChats 호출
    this.ldj_loadChats();
  },
  computed: {
    ...mapGetters("server", ["getBaseURL"]),
  },
  methods: {
    ldj_loadChats() {
      // backend 요청
      // this.chatList = backend에서 전달받은 데이터
      axios
        .post(
          baseURL + "api/chatroom/store_chatroom_list/",
          {
            store_id: this.store_id,
          },
          {
            headers: {
              Authorization: `Token ${this.$cookies.get("auth-token")}`,
            },
          }
        )
        .then((res) => {
          // this.chats = res.data;
          if (res.data.message) {
            this.chatList = [];
          } else {
            this.chatList = res.data;
            this.rand();
          }
        });
    },
    rand() {
      for (var i = 0; i < this.chatList.length; i++) {
        this.num.push(Math.floor(Math.random() * 8));
      }
    },
    ldj_loadChats_On_Scrool(lastKey) {
      // backend 요청
      // this.chatList에 Append
    },
    mvtochatting(chat) {
      const key = chat.store_id + "_" + chat.user;
      this.$router.push("/hrchat/" + key + "/" + chat.room_name);
    },
    onScroll() {
      if (
        window.top.scrollY + window.innerHeight >=
          document.body.scrollHeight - 100 &&
        !this.loading
      ) {
        this.ldj_loadChats_On_Scrool(
          this.chatList[this.chatList.length - 1].key
        );
      }
    },
  },
  created() {
    window.addEventListener("scroll", this.onScroll);
    // this.num = parseInt(Math.random() * 8);
  },
  destroyed() {
    window.removeEventListener("scroll", this.onScroll);
  },
  // watch: {
  //   loadedChats: {
  //     deep: true,
  //     handler() {},
  //   },
  // },
};
</script>

<style scoped>
* {
  font-family: "Do Hyeon";
}
.chatlist {
  position: relative;
  margin: auto auto;
  /* margin-top: 50px; */
  /* width: 300px;
  height: 300px; */
  width: fit-content;
  height: fit-content;
}

img {
  opacity: 0.5;
  display: block;
  /* width: 100%; */
  /* height: auto; */
  margin: auto auto;
  width: 250px;
  height: 250px;
  transition: 0.5s ease;
  backface-visibility: hidden;
}
.chatlist:hover img {
  /* opacity: 0.3; */
  background-color: black;
  border-radius: 5%;
}
.title {
  position: absolute;
  padding-left: 20%;
  /* width: 300px; */
  margin-top: -45%;
  /* font-weight: 700; */
  /* font-size: 30px; */
  /* text-align: center; */
  /* text-transform: uppercase; */
  z-index: 1;
  transition: top 0.5s ease;
}

.chatlist:hover .title {
  margin-top: -55%;
  transition: top 0.5s ease;
}
/* .chatlist:hover {
  border-radius: 5%;
} */
/* .button {
  position: absolute;
  width: 500px;
  left:0;
  top: 180px;
  text-align: center;
  opacity: 0;
  transition: opacity .35s ease;
}

.button a {
  width: 200px;
  padding: 12px 48px;
  text-align: center;
  color: black;
  border: solid 2px black;
  z-index: 1;
} */

/* .chatlist:hover .button {
  opacity: 1;
} */
</style>
