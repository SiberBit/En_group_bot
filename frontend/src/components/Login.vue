<template>
  <div>
    <form class="login-form" @submit.prevent="login">
      <h1>Авторизация</h1>
      <p class="error-message" v-if="error!=='form-control'">Неверные логин или пароль</p>
      <div class="form-group">
        <label for="login">Логин</label>
        <br>
        <input :class="error" id="login" required v-model="username" type="text" placeholder="Введите логин"/>
      </div>
      <div class="form-group">
        <label for="password">Пароль</label>
        <br>
        <input :class="error" id="password" required v-model="password" type="password" placeholder="Введите пароль"/>
      </div>
      <div class="btn-login">
        <button class="btn btn-outline">Вход</button>
      </div>
    </form>
  </div>
</template>
<script>
export default {
  data() {
    return {
      username: "",
      password: "",
      error: "form-control",
    }
  },
  methods: {
    login: function () {
      let username = this.username
      let password = this.password
      this.$store.dispatch('login', {username, password})
          .then(() => {
            this.error = "form-control"
            this.$router.push('/')
          })
          .catch(err => {
            this.error = "form-control"
            this.error = this.error + " error"
            console.log(err)
          })
    }
  }
}
</script>

<style scoped>
.login-form {

  border: 2px solid #ff941a;
  border-radius: .3rem;
  padding: 30px 80px;

  margin: 0;
  position: absolute;
  top: 50%;
  left: 50%;
  margin-right: -50%;
  transform: translate(-50%, -50%)
}

.error {
  border: 2px solid #ef7474;
}

.error-message {
  color: #ef7474;
}

/*Кнопки*/
.btn-login {
  text-align: center;
}

.btn-outline {
  color: #ff941a;
  border-color: #ff941a;
}

.btn-outline:hover,
.btn-outline:focus,
.btn-outline:visited,
.btn-outline:active {
  background-color: #ff941a;
  border-color: #ff941a;
  color: white;
}

h1 {
  text-align: center;
  margin: 10px 0 20px;
}
</style>