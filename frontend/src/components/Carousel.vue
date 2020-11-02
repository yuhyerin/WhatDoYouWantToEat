<template>
  <v-layout class="content" style="width:100%;" md="12" xl="12">
    <carousel
      :per-page="1"
      :mouse-drag="false"
      :autoplay="true"
      :autoplayTimeout="5000"
      :loop="true"
      :autoplayHoverPause="true"
      :paginationPosition="bottom - overlay"
    >
      <slide v-for="(item, index) in storeData" :key="index" :index="index">
        <img :src="item.store_id" alt="item.store_id" />
        <!-- <slide> -->
        <!-- <img style="height:25vh!important ; width: 250vh" src="../assets/image/background.jpg"> -->
      </slide>
    </carousel>
  </v-layout>
</template>

<script>
import Vue from "vue";
import VueCarousel from "vue-carousel";

Vue.use(VueCarousel);

export default {
  props: {
    storeData: {},
  },
  components: {},
  data: () => ({}),
};
</script>

<style></style>
