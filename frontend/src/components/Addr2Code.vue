<template>
  <div id="map"></div>
</template>
<script>
import { mapGetters } from "vuex";
import { EventBus } from "../utils/EventBus.js";

export default {
  data() {
    return {
      address: "",
      lat: 0,
      lng: 0,
    };
  },

  computed: {
    ...mapGetters("location", ["getLocation"]),
  },

  mounted() {
    window.kakao && window.kakao.maps ? null : this.addScript();
  },

  created() {
    EventBus.$on("addressChange", (userAddress) => {
      this.address = userAddress;
      this.searchAddr();
    });
  },

  methods: {
    addScript() {
      let script = document.createElement("script");
      /* global kakao */

      script.onload = () => kakao.maps.load(this.initMap);
      script.src =
        "https://dapi.kakao.com/v2/maps/sdk.js?autoload=false&appkey=a7bd2d0df8f5ae53b0c5e106842b94fd&libraries=services";
      document.head.appendChild(script);
    },

    searchAddr() {
      var geocoder = new kakao.maps.services.Geocoder();

      geocoder.addressSearch(this.address, (result, status) => {
        if (status === kakao.maps.services.Status.OK) {
          this.$store.commit("location/setLocation", {
            lat: result[0].y,
            lng: result[0].x,
            dong: result[0].address.region_3depth_name,
          });
          this.lat = result[0].y;
          this.lng = result[0].x;
        }
      });
    },
  },
};
</script>
