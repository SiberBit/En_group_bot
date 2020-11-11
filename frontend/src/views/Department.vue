<template>

  <div class="row">
    <div v-for="department in departments" v-bind:key=department.id style="padding: 10px">
      <button type="button" class="btn btn-success">{{ department.name }}</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios'


export default {
  name: "Department",
  computed: {
    organization: {
      get() {
        return this.$store.getters.organization
      },
    }
  },
  data: function () {
    return {
      url: {
        department_api: this.$store.state.api_url + 'departments/',
      },
      departments: [],
    }
  },
  created: function () {
    this.get_departments()

  },

  methods: {
    get_departments() {
      axios.get(this.url.department_api + this.organization.slug + '/').then((response) => {
        console.log(response.data);
        const departments = response.data;
        this.departments = departments;
      });
    }
  },

  watch: {
    organization: function () {
      this.get_departments()
    }
  },
}
</script>

<style scoped>
</style>