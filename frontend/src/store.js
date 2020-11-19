import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'
import createPersistedState from "vuex-persistedstate";

Vue.use(Vuex)

console.log(location.hostname)
const host_url = location.hostname + '/';


export default new Vuex.Store({
    state: {
        status: '',
        token: localStorage.getItem('token') || '',
        user: {},
        auth_url: host_url + 'api/token/',
        api_url: host_url + 'api/v1/',
        user_url: host_url + 'user/',
        organization: {},
        department: {},
        departments_list: [],
    },
    plugins: [createPersistedState()],
    mutations: {
        auth_request(state) {
            state.status = 'loading'
        },
        auth_success(state, {token, user}) {
            state.status = 'success'
            state.token = token
            state.user = user
            state.organization = user.profile.organization[0]
        },
        auth_error(state) {
            state.status = 'error'
        },
        logout(state) {
            state.status = ''
            state.token = ''
            state.user = {}
        },
        set_organization(state, organization) {
            state.organization = organization
        },
        set_department(state, department) {
            state.department = department
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
                        const user = resp.data.user
                        localStorage.setItem('user', user)

                        commit('auth_success', {token, user})
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
            user: state => {
                return state.user
            },
            organization: state => {
                return state.organization
            },
            department: state => {
                return state.department
            },
        },


})
