<template>
  <v-main>
    <v-container>
      <v-row no-gutters>
        <v-col sm="6" xs="12" offset-sm="3">
          <v-col xs="12">
            <v-text-field
              name="chatname"
              label="Chat Name"
              id="chatname"
              v-model="chatName"
              type="text"
              required
            ></v-text-field>
            <v-text-field
              label="주소"
              @click="findAddress(true)"
              readonly="readonly"
              v-model="address"
            ></v-text-field>
            <!-- <v-btn type="submit">Create</v-btn> -->
            <v-btn @click="createChat()">CREATE</v-btn>
          </v-col>
        </v-col>
      </v-row>
    </v-container>
  </v-main>
</template>

<script src="http://dmaps.daum.net/map_js_init/postcode.v2.js"></script>
<script src="//dapi.kakao.com/v2/maps/sdk.js?appkey=48cbffa8392e1a7acffc1975347ec0d3&libraries=services"></script>
<script>
import axios from "axios";
import { mapGetters } from "vuex";
// const baseURL = "http://127.0.0.1:8000/";
const baseURL = "http://ec2-52-79-239-80.ap-northeast-2.compute.amazonaws.com/";
// import * as firebase from "firebase";
// this.$route.params.storeid

export default {
  data() {
    return {
      chatName: "",
      // loading: false,
      address: "",
    };
  },
  computed: {
    ...mapGetters("server", ["getBaseURL"]),
  },

  methods: {
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
            this.address = fullAddr;
          }
        },
      }).open();
    },

    createChat() {
      if (this.chatName == null || this.chatName === "") {
        alert("채팅방이름을 입력하세요");
        return;
      }
      if (this.address == null || this.address === "") {
        alert("주소지를 알려주세요");
        return;
      }
      axios
        .post(
          baseURL + "api/chatroom/createchatroom/",
          {
            store_id: this.$route.params.storeid,
            room_name: this.chatName,
          },
          {
            headers: {
              Authorization: `Token ${this.$cookies.get("auth-token")}`,
            },
          }
        ) // post > post
        .then((res) => {
          console.log(res.data);
          this.$router.push("/hrchat/" + res.data.key + "/" + this.chatName);
        })
        .catch((err) => {
          console.log(err.response);
          // let token = res.data.key;
          this.$store.dispatch("signUserUp", {
            email: this.nm_email,
            password: this.nm_password,
            username: this.nm_nickname,
          });
        });
    },

    // createChat() {
    //   if (this.chatName == "" || this.loading) {
    //     return;
    //   }

    //   this.loading = true;

    //   let time = new Date().valueOf();
    //   let newPostKey = firebase
    //     .database()
    //     .ref()
    //     .child("chats")
    //     .push().key;

    //   let updates = {};
    // updates["/chats/" + newPostKey] = { name: this.chatName };
    // updates["/chat_members/" + newPostKey + "/users/" + this.user.id] = {
    //   timestamp: time,
    // };
    // updates["users/" + this.user.id + "/chats/" + newPostKey] = {
    //   timestamp: time,
    // };
    // firebase
    //   .database()
    //   .ref()
    //   .update(updates)
    //   .then(() => {
    //     this.loading = false;
    //     this.$router.push("/chat/" + newPostKey);
    //   });
    // },
  },
};
</script>
