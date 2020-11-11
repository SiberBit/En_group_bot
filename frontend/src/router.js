import Vue from 'vue'
import Router from 'vue-router'
import store from './store.js'
import Home from './views/Home.vue'
import About from './views/About.vue'
import Login from './components/Login.vue'
import Department from "@/views/Department";
import Categories from "@/views/Categories";


Vue.use(Router)

let router = new Router({
    mode: 'history',
    routes: [

        {
            path: '/login',
            name: 'login',
            component: Login
        },
        {
            path: '/',
            name: 'home',
            component: Home,
            meta: {
                requiresAuth: true
            }
        },
        {
            path: '/api/v1/*',
            meta: {
                requiresAuth: true
            }
        },

        {
            path: '/categories',
            name: 'categories',
            component: Categories,
            meta: {
                requiresAuth: true
            }
        },
                {
            path: '/department',
            name: 'Department',
            component: Department,
            meta: {
                requiresAuth: true
            }
        },

    ]
})

router.beforeEach((to, from, next) => {
    if (to.matched.some(record => record.meta.requiresAuth)) {
        if (store.getters.isLoggedIn) {
            next()
            return
        }
        next('/login')
    } else {
        next()
    }
})

export default router