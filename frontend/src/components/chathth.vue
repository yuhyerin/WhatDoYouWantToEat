<template>
  <div id="app">
  <v-app id="inspire">
    <!-- <v-expansion-panels> -->
      <v-expansion-panel>
        <v-expansion-panel-header>
          <template v-slot:default="{ open }">
            <v-row no-gutters>
              <v-col cols="4">답글</v-col>
              <v-col cols="8" class="text--secondary">
                <v-fade-transition leave-absolute>
                  <span v-if="open" key="0">
                    Enter a name for the trip
                  </span>
                  <span v-else key="1">
                    {{ trip.name }}
                  </span>
                </v-fade-transition>
              </v-col>
            </v-row>
          </template>
        </v-expansion-panel-header>
        <v-expansion-panel-content>
          <v-text-field v-model="trip.name" placeholder="답글"></v-text-field>
        </v-expansion-panel-content>
      </v-expansion-panel>
    <!-- </v-expansion-panels> -->
  </v-app>
</div>
</template>

<script>
export default {
    data () {
        return {
            date: null,
            trip: {
            name: '',
            },
            locations: ['Australia', 'Barbados', 'Chile', 'Denmark', 'Ecuador', 'France'],
                }
    }

}
</script>

<style>

</style>