import Vue from 'vue'
import Router from 'vue-router'
import store from './store.js'
import Home from './views/Home.vue'
import Login from './components/Login.vue'
import Department from "@/views/Department";
import Categories from "@/views/Categories";
import axios from 'axios'

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

// проверка жадого ответа на вторизацию
axios.interceptors.response.use(
    // Обработчик для успешного случая; просто пропускаем ответ дальше
    res => {
        return res;
    },
    // Обработчик для ошибки
    error => {
        if (error.response.status === 401) {
            store.dispatch('logout')
                .then(() => {
                    router.push('/login')
                })
        }
        return Promise.reject(error);
    }
);


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