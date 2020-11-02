<template>
  <div class="content">
    <div>
      우리동네 날씨와 시간대를 분석하여 추천하는 메뉴는 입니다.
    </div>
    <carousel
      :per-page="1"
      :navigate-to="someLocalProperty"
      :mouse-drag="false"
      :autoplay="true"
      :autoplayTimeout="2000"
      :navigationEnabled="true"
      :loop="true"
    >
      <slide v-for="(item, index) in storeData" :key="index">
        {{ item.name }} 이미지
      </slide>
    </carousel>
  </div>
</template>

<script>
import Vue from "vue";
import { Carousel, Slide } from "vue-carousel";

Vue.use(Carousel);

export default {
  props: {
    storeData: {},
  },
  components: {
    Carousel,
    Slide,
  },
  data: () => ({
    storName: "",
  }),
};
</script>

<style></style>
