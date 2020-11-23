<template>
  <div>
    <b-navbar class="navbar" toggleable="lg" type="dark" variant="primary">
      <b-navbar-brand>
        <router-link style="color: white" to="/"  tag="a">En+ group bot</router-link>
      </b-navbar-brand>

      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav>
          <b-nav-item>
            <router-link class="navbar-item" tag="a" active-class="active" to="/" exact>Главная</router-link>
          </b-nav-item>
          <b-nav-item>
            <router-link class="navbar-item" tag="a" active-class="active"  to="/department">Подразделения</router-link>
          </b-nav-item>

          <b-nav-item>
            <router-link class="navbar-item" tag="a" active-class="active" to="/chat-bots">Чат боты</router-link>
          </b-nav-item>
        </b-navbar-nav>


        <!-- Right aligned nav items -->
        <b-navbar-nav class="ml-auto">

          <b-form-select v-model="organization">
            <option v-for="org in organizations" v-bind:value="org">
              {{ org.name }}
            </option>
          </b-form-select>

          <b-nav-item-dropdown right>
            <!-- Using 'button-content' slot -->
            <template #button-content>
              <em>{{ user.username }} <span v-if="user.is_staff">(администратор)</span></em>
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
    return {}
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

.navbar-item {
  color: white;
}

.active {

 }

</style>