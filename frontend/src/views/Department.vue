<template>


</template>

<script>
import axios from 'axios'

// console.log(this.$store.state.api_url) // получение глобальной переменной

export default {
  name: "Department",
  data: function () {
    return {}
  },
  created: function () {

  },
  methods: {
    get_departments() {
      axios.get(this.url.categories_api).then((response) => {
        console.log(response.data);
        const categories = response.data;
        this.categories = categories;
        this.category = [];
      });
    }
  },
}
</script>

<style scoped>
</style>