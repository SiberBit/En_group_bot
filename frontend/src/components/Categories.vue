<template>

  <div>
    <p><a class="btn" @click="get_start_categories">В начало</a>/
      <a class="btn" @click="get_categories(cat)" v-for="cat in category" v-bind:key=cat.id> {{ cat.name }} /</a></p>


    <div class="row">
      <div v-for="category in categories" v-bind:key=category.id style="padding: 10px">
        <button type="button" @click="get_categories(category)" class="btn btn-success">{{ category.name }}</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: "Categories",
  data: function () {
    return {
      url: {
        categories_api: 'http://127.0.0.1:8000/api/v1/categories/testovaya-organizaciya/testovoe-podrazdelen/',
      },
      categories: [],
      category: []
    }
  },
  created: function () {
    // this.categories = categories;
    this.get_start_categories();
  },
  methods: {
    get_categories(category) {
      // получаем подкатегории
      axios.get(this.url.categories_api + category.id + '/').then((response) => {
        console.log(response.data);
        const categories = response.data;
        this.categories = categories;
        if (this.category[-1] != category) {
          this.category.push(category)
        } else {
          this.category.pop()
        }
        console.log(this.category);
      });
    },
    get_start_categories() {
      // получаем начальные категории
      axios.get(this.url.categories_api).then((response) => {
        console.log(response.data);
        const categories = response.data;
        this.categories = categories;
        this.category = [];
      });
    },
  }
}
</script>

<style scoped>
</style>