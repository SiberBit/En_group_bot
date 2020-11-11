<template>
  <div>
    <b-navbar toggleable="lg" type="dark" variant="info">
      <b-navbar-brand href="#">En+ group bot</b-navbar-brand>

      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav>
          <b-nav-item>
            <router-link to="/">Главная</router-link>
          </b-nav-item>
          <b-nav-item>
            <router-link to="/department">Подразделения</router-link>
          </b-nav-item>

          <b-nav-item disabled>
            <router-link to="">Чат боты</router-link>
          </b-nav-item>
        </b-navbar-nav>


        <!-- Right aligned nav items -->
        <b-navbar-nav class="ml-auto">
          <!--          <b-nav-item-dropdown  v-model="selected" text="Организация 1" right>-->
          <!--            <b-dropdown-item>Организация 1</b-dropdown-item>-->
          <!--            <b-dropdown-item>Организация 2</b-dropdown-item>-->
          <!--            <b-dropdown-item>Организация 3</b-dropdown-item>-->

          <!--          </b-nav-item-dropdown>-->

          <select v-model="organization">
            <option v-for="org in organizations" v-bind:value="org">
              {{ org.name }}
            </option>
          </select>

          <b-nav-form>
            <b-form-input size="sm" class="mr-sm-2" placeholder="Search"></b-form-input>
            <b-button size="sm" class="my-2 my-sm-0" type="submit">Search</b-button>
          </b-nav-form>


          <b-nav-item-dropdown right>
            <!-- Using 'button-content' slot -->
            <template #button-content>
              <em>{{ user.username }}</em>
            </template>
            <b-dropdown-item>Профиль</b-dropdown-item>
            <b-dropdown-item><a @click="logout">Выход</a></b-dropdown-item>
          </b-nav-item-dropdown>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
  </div>


</template>

<script>

export default {
  name: "NavBar",
  computed: {
    user() {
      return this.$store.getters.user
    },
    organizations() {
      return this.$store.getters.user.profile.organization
    },
    organization: {
      get() {
        return this.$store.getters.organization
      },
      set(organization) {
        this.$store.commit('set_organization', organization)
      }
    }
  },

  data: function () {
    return {
    }
  },
  methods: {
    logout: function () {
      this.$store.dispatch('logout')
          .then(() => {
            this.$router.push('/login')
          })
    }
  },

}
</script>

<style scoped>

</style>