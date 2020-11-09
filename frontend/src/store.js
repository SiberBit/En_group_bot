import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'

Vue.use(Vuex)

const host_url = 'http://127.0.0.1:8000/';


export default new Vuex.Store({
    state: {
        status: '',
        token: localStorage.getItem('token') || '',
        user: {},
        auth_url: host_url + 'api/token/',
        api_url: host_url + 'api/v1/',
        user_url: host_url + 'user/',
    },
    mutations: {
        auth_request(state) {
            state.status = 'loading'
        },
        auth_success(state, token) {
            state.status = 'success'
            state.token = token
            axios.get(host_url + 'user/').then((response) => {
                console.log(response.data);
                state.user = response.data
            }).catch(err => {
                state.status = 'error'
                localStorage.removeItem('token')
                reject(err)
            })
        },
        auth_error(state) {
            state.status = 'error'
        },
        logout(state) {
            state.status = ''
            state.token = ''
        },
    },
    actions: {
        login({commit}, user) {
            return new Promise((resolve, reject) => {
                commit('auth_request')
                axios({url: this.state.auth_url, data: user, method: 'POST'})
                    .then(resp => {
                        const token = 'Bearer ' + resp.data.access // приписываем к токену аторизации 'Bearer ' и сохраняем
                        localStorage.setItem('token', token)
                        // Add the following line:
                        axios.defaults.headers.common['Authorization'] = token // проставляем в заголовок токен для всех запросов
                        commit('auth_success', token)
                        resolve(resp)
                    })
                    .catch(err => {
                        commit('auth_error')
                        localStorage.removeItem('token')
                        reject(err)
                    })
            })
        },
        logout({commit}) {
            return new Promise((resolve, reject) => {
                commit('logout')
                localStorage.removeItem('token')
                delete axios.defaults.headers.common['Authorization']
                resolve()
            })
        }
    },
    getters:
        {
            isLoggedIn: state => !!state.token,
            authStatus:
                state => state.status,
        }
})
