<template>
  <div>
    <p>
      <router-link to="/">Home</router-link>
      <router-link to="/login">Login</router-link>
      <router-link to="/storelist/:category"></router-link>
      <router-link to="/storedetail/:storeid"></router-link>
      <router-view></router-view>
    </p>
  </div>
</template>

<script>
export default {};
</script>

<style></style>
