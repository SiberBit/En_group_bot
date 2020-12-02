<template>
  <div id="app">
    <div v-if="isLoggedIn" id="nav">
      <NavBar/>
    </div>
    <div class="container">
      <router-view/>
    </div>
  </div>
</template>
<script>

import NavBar from "@/components/NavBar";

export default {
  components: {
    NavBar
  },

  computed: {
    isLoggedIn: function () {
      return this.$store.getters.isLoggedIn
    }
  },

  created: function () {
    this.$http.interceptors.response.use(undefined, function (err) {
      return new Promise(function (resolve, reject) {
        if (err.status === 401 && err.config && !err.config.__isRetryRequest) {
          this.$store.dispatch(logout)
        }
        throw err;
      });
    });
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}

a{
 color: #393330;
}
a:hover {
  color: #ff941a;
  text-decoration: underline;
}

#nav a {
  /*font-weight: bold;*/
  /*cursor: pointer;*/
}

#nav a:hover {
  color: #ff941a;
  text-decoration: underline;
}

/*#nav a.router-link-exact-active {*/
/*  color: #42b983;*/
/*}*/


h1{
  margin: 10px 0 20px;
}



</style>
