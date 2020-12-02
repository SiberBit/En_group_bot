<template>
  <div class="loading">
    <img src="../assets/loading.gif">
  </div>
</template>

<script>
export default {
  name: "Loading"
}
</script>

<style scoped>
.loading {
  height: 100%;
}
.loading img {
  width: 50px;
  margin: 0;
  position: absolute;
  top: 50%;
  left: 50%;
  margin-right: -50%;
  transform: translate(-50%, -50%)
}
</style>