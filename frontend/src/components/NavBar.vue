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
          <b-nav-item-dropdown text="Оргинизация 1" right>
            <b-dropdown-item >Оргинизация 1</b-dropdown-item>
            <b-dropdown-item >Оргинизация 2</b-dropdown-item>
            <b-dropdown-item >Оргинизация 3</b-dropdown-item>

          </b-nav-item-dropdown>
          <b-nav-form>
            <b-form-input size="sm" class="mr-sm-2" placeholder="Search"></b-form-input>
            <b-button size="sm" class="my-2 my-sm-0" type="submit">Search</b-button>
          </b-nav-form>


          <b-nav-item-dropdown right>
            <!-- Using 'button-content' slot -->
            <template #button-content>
              <em>User</em>
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