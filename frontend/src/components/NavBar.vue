<template>
  <div>
    <b-navbar class="navbar" toggleable="lg" type="white" variant="muted">
      <b-navbar-brand>
        <router-link class="logo" style="text-decoration: none;" to="/" tag="a">En+ group bot</router-link>
      </b-navbar-brand>

      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav>
          <b-nav-item>
            <router-link class="navbar-item" tag="a" active-class="active" to="/" exact>Главная</router-link>
          </b-nav-item>
          <b-nav-item>
            <router-link class="navbar-item" tag="a" active-class="active" to="/department">Подразделения</router-link>
          </b-nav-item>

          <b-nav-item>
            <router-link class="navbar-item" tag="a" active-class="active" to="/chat-bots">Чат боты</router-link>
          </b-nav-item>
        </b-navbar-nav>


        <!-- Right aligned nav items -->
        <b-navbar-nav class="ml-auto">
          <b-form-select v-model="organization" class="border-0">
            <option v-for="org in organizations" v-bind:value="org">
              {{ org.name }}
            </option>
          </b-form-select>

          <b-nav-item-dropdown right>
            <!-- Using 'button-content' slot -->
            <template #button-content>
              <em class="user-name">{{ user.username }} <span v-if="user.is_staff">(администратор)</span></em>
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

import axios from "axios";

export default {
  name: "NavBar",
  computed: {
    user: {
      get() {
        return this.$store.getters.user
      },
      set(user) {
        this.$store.commit('set_user', user)
      }
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
    created: function () {
    this.get_user()
  },
  methods: {
    logout: function () {
      this.$store.dispatch('logout')
          .then(() => {
            this.$router.push('/login')
          })
    },

    get_user() {
      axios.get(this.$store.state.user_url).then((response) => {
        this.user = response.data
      }).catch((error) => {
        console.log(error);
        this.$store.dispatch('logout')
            .then(() => {
              this.$router.push('/login')
            })
      });
    },
  },

}
</script>

<style scoped>

.navbar-item {
  color: #393330;
}

.logo {

  color: #393330;
}

.logo:hover {
  text-decoration: none;
}

.active {

}

/*Пользователь*/
.user-name {
  color: #eea65b;
}

/*Организация*/
.custom-select:focus {
  -webkit-box-shadow: none;
  box-shadow: none;
}

</style>