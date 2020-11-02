<template>
  <!-- <v-card class="mx-auto" max-width="320" outlined>
    <v-col>
      <v-row justify="center">
        <div>{{ storeData[1] }}</div>
      </v-row>
      <v-row justify="center">
        <v-list-item-avatar tile size="200" color="grey" />
      </v-row>
    </v-col>

    <v-card-actions>
      <v-btn depressed color="primary" @click="goToShop">가게 보러가기</v-btn>
    </v-card-actions>
  </v-card> -->
  <div id="showlist">
    <button @click="goToShop">
      <card
        data-image="https://images.unsplash.com/photo-1479660656269-197ebb83b540?dpr=2&auto=compress,format&fit=crop&w=1199&h=798&q=80&cs=tinysrgb&crop="
      >
        <h1 slot="header">{{ storeData.category }}</h1>
        <p slot="content">가게 보러 가기</p>
      </card>
    </button>
  </div>
</template>

<script>
import card from "../components/Card.vue";
export default {
  components: {
    card,
  },
  props: {
    storeData: {},
  },

  methods: {
    goToShop: function() {
      this.$router.push("/storelist/" + this.storeData[1]);
    },
    mvpage: function() {
      this.$router.push("/chat");
    },
  },
};
</script>
