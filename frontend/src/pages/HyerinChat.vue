<template>
  <v-main style="padding: 3.5%;">
    <Header />
    <v-col>
      <div class="menu">
        <div class="back" @click="exit()">
          <i class="material-icons">&#xE5C4;</i>
        </div>
        <div class="name">{{ roomName }}</div>
      </div>
      <div v-for="(chatting, index) in chattings" :key="index">
        <ol class="chat">
          <li
            v-if="$cookies.get('nickname') === chatting.nickname"
            class="self"
          >
            <div class="msg">
              {{ chatting.msg }}
            </div>
            <p>{{ chatting.nickname }}</p>
          </li>
          <li v-else class="other">
            <p>{{ chatting.nickname }}</p>
            <div class="msg">
              {{ chatting.msg }}
            </div>
          </li>
        </ol>
      </div>
      <input
        v-on:keyup.enter="yhr()"
        class="textarea"
        type="text"
        v-model="message"
      /><v-btn class="submit" @click="yhr()">전송</v-btn>
    </v-col>
  </v-main>
</template>

<script>
import Header from "../components/Header.vue";
import { mapGetters } from "vuex";

const baseURL = "http://127.0.0.1:8000/";
// const baseURL = "http://ec2-52-79-239-80.ap-northeast-2.compute.amazonaws.com/";

export default {
  components: {
    Header,
  },
  watch: {},
  data() {
    return {
      roomName: "",
      roomNumber: "",
      chatSocket: "",
      message: "",
      msg: "",
      chattings: [],
    };
  },
  created() {
    var URL = baseURL.substring(5, baseURL.length);

    this.roomNumber = this.$route.params.roomNumber; // 채팅방 uid
    this.roomName = this.$route.params.roomName; // 채팅방 이름
    this.chatSocket = new WebSocket( // 웹소켓에 연결하는 부분
      "ws://" +
        // "ec2-52-79-250-4.ap-northeast-2.compute.amazonaws.com/" +
        URL +
        "ws/chat/" +
        this.roomNumber +
        "/"
    ); // ws://127.0.0.1:8000/ws/chat/roomName/

    // 이벤트 등록. onmessage -> chatSocket에 메세지가 도착했을 때 일어날 이벤트를 여기에 작성.
    this.chatSocket.onmessage = (e) => {
      const data = JSON.parse(e.data);
      let nickname = data.message.split("&&&&")[0];
      let msg = data.message.split("&&&&")[1];
      this.chattings.push({ nickname: nickname, msg: msg });
      // document.querySelector('#chat-log').value += (nickname+" ) "+ msg + '\n');
    };
    this.chatSocket.onclose = function() {
      console.error("Chat socket closed unexpectedly");
    };
  },
  computed: { ...mapGetters("server", ["getBaseURL"]) },
  methods: {
    exit() {
      location.href = "/home";
    },
    yhr() {
      // const messageInputDom = document.querySelector('#chat-message-input');
      // this.message = messageInputDom.value; // message : 채팅창에 입력한 텍스트
      // message = 닉네임 + "&&&&" + message
      if (this.message == "" || this.message == null) {
        return;
      } else {
        this.msg = this.$cookies.get("nickname") + "&&&&" + this.message;
        this.chatSocket.send(
          JSON.stringify({
            message: this.msg,
          })
        );
      }
      // messageInputDom.value = '';
      this.message = "";
    },
  },
};
</script>

<style>
/* ::selection{
  background: rgba(82,179,217,0.3);
  color: inherit;
} */
/* a{
  color: rgb(233,105,30);
} */

/* M E N U */
.menu {
  margin: 0;
  width: 100%;
  height: 50px;
  background: rgb(0, 0, 0);
  z-index: 100;
  /* -webkit-touch-callout: none;
    -webkit-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none; */
  display: flex;
}
.back {
  width: 90px;
  height: 50px;
  top: 0px;
  left: 0px;
  color: #fff;
  line-height: 50px;
  font-size: 30px;
  padding-left: 10px;
  cursor: pointer;
}
.back img {
  position: absolute;
  top: 5px;
  left: 30px;
  width: 40px;
  height: 40px;
  background-color: rgba(255, 255, 255, 0.98);
  border-radius: 100%;
  -webkit-border-radius: 100%;
  -moz-border-radius: 100%;
  -ms-border-radius: 100%;
  margin-left: 15px;
}
.back:active {
  background: rgba(255, 255, 255, 0.2);
}
.name {
  font-size: 35px;
  color: rgb(255, 255, 255);
  cursor: default;
  margin-left: 35%;
}
.last {
  position: absolute;
  top: 30px;
  left: 115px;
  font-family: "Lato";
  font-size: 11px;
  font-weight: 400;
  color: rgba(255, 255, 255, 0.6);
  cursor: default;
}

/* M E S S A G E S */

.chat {
  list-style: none;
  background: none;
  margin: 0;
  padding: 0 0 50px 0;
  margin-top: 60px;
  margin-bottom: 10px;
}
.chat li {
  padding: 0.5rem;
  overflow: hidden;
  display: flex;
}
.chat .avatar {
  width: 40px;
  height: 40px;
  position: relative;
  display: block;
  z-index: 2;
  border-radius: 100%;
  -webkit-border-radius: 100%;
  -moz-border-radius: 100%;
  -ms-border-radius: 100%;
  background-color: rgba(255, 255, 255, 0.9);
}
.chat .avatar img {
  width: 40px;
  height: 40px;
  border-radius: 100%;
  -webkit-border-radius: 100%;
  -moz-border-radius: 100%;
  -ms-border-radius: 100%;
  background-color: rgba(255, 255, 255, 0.9);
  -webkit-touch-callout: none;
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
}
.other .msg {
  order: 1;
  border-top-left-radius: 1%;
  box-shadow: -1px 2px 0px rgba(0, 0, 0, 0.3);
  font-family: Jua;
}
.other:before {
  content: "";
  position: relative;
  top: 0px;
  right: 0px;
  left: 40px;
  width: 0px;
  height: 0px;
  border: 5px solid #fff;
  border-left-color: transparent;
  border-bottom-color: transparent;
}

.self {
  justify-content: flex-end;
  align-items: flex-end;
}
.self .msg {
  order: 1;
  border-bottom-right-radius: 0px;
  border-radius: 1%;
  box-shadow: 1px 2px 0px rgba(233, 103, 30, 0.3);
  font-family: Jua;
}
.msg {
  background: white;
  min-width: 50px;
  padding: 10px;
  border-radius: 2px;
  box-shadow: 0px 2px 0px rgba(0, 0, 0, 0.07);
  font-family: Jua;
}
.msg p {
  font-size: 0.8rem;
  margin: 0 0 0.2rem 0;
  color: #777;
  font-family: Jua;
}

/* @media screen and (max-width: 800px) {
    .msg img {
    width: 300px;
}
}
@media screen and (max-width: 550px) {
    .msg img {
    width: 200px;
}
} */

/* @-webikt-keyframes pulse {
  from { opacity: 0; }
  to { opacity: 0.5; }
} */

/* ::-webkit-scrollbar {
    min-width: 12px;
    width: 12px;
    max-width: 12px;
    min-height: 12px;
    height: 12px;
    max-height: 12px;
    background: #e5e5e5;
    box-shadow: inset 0px 50px 0px rgba(82,179,217,0.9), inset 0px -52px 0px #fafafa;
}

::-webkit-scrollbar-thumb {
    background: #bbb;
    border: none;
    border-radius: 100px;
    border: solid 3px #e5e5e5;
    box-shadow: inset 0px 0px 3px #999;
}

::-webkit-scrollbar-thumb:hover {
    background: #b0b0b0;
  box-shadow: inset 0px 0px 3px #888;
}

::-webkit-scrollbar-thumb:active {
    background: #aaa;
  box-shadow: inset 0px 0px 3px #7f7f7f;
}

::-webkit-scrollbar-button {
    display: block;
    height: 26px;
} */

input.textarea {
  position: fixed;
  bottom: 0px;
  left: 5%;
  right: 0px;
  width: 88%;
  height: 50px;
  margin: 0;
  z-index: 99;
  background: rgba(0, 0, 0, 0.3);
  border: none;
  outline: none;
  padding-left: 1%;
  color: #000;
  font-weight: 400;
  font-family: Jua;
}
button.submit {
  position: fixed;
  bottom: 1%;
  left: 93%;
}
</style>
