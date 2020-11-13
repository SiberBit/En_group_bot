import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import Axios from 'axios'
import BootstrapVue from "bootstrap-vue"
import "bootstrap/dist/css/bootstrap.min.css"
import "bootstrap-vue/dist/bootstrap-vue.css"


Vue.prototype.$http = Axios;

Vue.use(BootstrapVue)

const token = localStorage.getItem('token')
if (token) {
    Vue.prototype.$http.defaults.headers.common['Authorization'] = token
}

Vue.config.productionTip = false

window.Slug = require("slug")
Slug.defaults.mode = "rfc3986"

new Vue({
    router,
    store,
    render: h => h(App)
}).$mount('#app')
