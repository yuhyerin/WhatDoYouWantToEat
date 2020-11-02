<template>
  <div>
    <div class="party">
    <v-btn @click='mvtopage()'>
      <v-icon left>mdi-forum</v-icon>
      파티만들기
    </v-btn>
    </div>
    <!-- <v-btn text to="/discover">
      <v-icon left>mdi-chat</v-icon>
      <div class="hidden-xs-only">파티찾기</div>
    </v-btn> -->
    <div>
      <ChatList :store_id='storeInfo.store_id' />
    </div>
  </div>
</template>
<script>
// import ChatList from "./Chat/ChatList.vue";
import ChatList from "./HyerinChat/ChatList.vue";

export default {
  props:{
    storeInfo: []
  },
  components: {
    ChatList,
  },
  methods:{
    mvtopage(){
      this.$router.push('/create/'+this.storeInfo.store_id)
    }
  }
};
</script>
<style scoped>
.party {
  display: flex;
  justify-content: flex-end;
  align-items: center;
}
</style>
