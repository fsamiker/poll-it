import Vue from 'vue'
import Vuex from 'vuex'
import { authenticate } from '@/api'
import createPersistedState from "vuex-persistedstate";

Vue.use(Vuex)
Vue.config.devtools = true

const store = new Vuex.Store({
    plugins: [createPersistedState()],
    state: {
        token: '',
        token_expire: '',
        user: null,
        votedPolls: {}
    },
    actions: {
        login ({ commit }, credentials) {
            return authenticate(credentials)
            .then(response => response.json())
            .then(data => {
                commit('setUser', data);
            })
        },
        logout ( { commit }) {
            window.localStorage.removeItem('vuex'); 
            commit('clearUser');
        }
    },
    mutations: {
        setUser(state, payload) {
            state.token = payload.token
            state.token_expire = payload.expires
            state.user = payload.user
        },
        clearUser(state) {
            state.token = ''
            state.token_expire = ''
            state.user = null
            state.votedPolls = {}
        },
        updateVotedPolls(state, newPolls) {
            state.votedPolls = Object.assign({}, state.votedPolls, newPolls)
        }
    },
    getters: {
        getAuthHeader (state) {
            return { 
                'Authorization': 'Bearer ' + state.token,
                'Content-Type': 'application/json'
            }
        },
        loggedIn (state) {
            if (state.user) {
                return true
            }
            return false
        }
    }
  })
  
  export default store