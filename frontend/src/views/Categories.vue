<template>

  <div>

    <span>{{ department.name }}</span>

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
        categories_api: this.$store.state.api_url + 'categories/',
      },
      categories: [],
      category: [],
    }
  },

  computed: {
    organization: {
      get() {
        return this.$store.getters.organization
      },
    },
    department: {
      get() {
        return this.$store.getters.department
      },
    }
  },

  created: function () {
    this.get_start_categories();
  },
  methods: {
    get_categories(category) {
      // получаем подкатегории
      axios.get(this.url.categories_api + this.organization.slug + '/' + this.department.slug + '/' + category.id + '/').then((response) => {
        console.log(response.data);
        const categories = response.data;
        this.categories = categories;
        if (this.category[-1] != category) {
          this.category.push(category)
        } else {
          this.category.pop()
        }
      });
    },
    get_start_categories() {
      // получаем начальные категории
      axios.get(this.url.categories_api + this.organization.slug + '/' + this.department.slug + '/').then((response) => {
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