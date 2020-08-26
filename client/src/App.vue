<template>
  <div id="app">
    <section class="hero is-primary">
      <div class="hero-head">
        <div id="nav" class="navbar" role="navigation" aria-label="main navigation">
          <div class="navbar-brand">
            <router-link class="navbar-item is-size-3" to="/"><strong>POLL IT</strong></router-link>
            <a role="button" class="navbar-burger burger" aria-label="menu" aria-expanded="false" data-target="navbarBasicExample">
              <span aria-hidden="true"></span>
              <span aria-hidden="true"></span>
              <span aria-hidden="true"></span>
            </a>
          </div>
          <div class="navbar-menu">
            <div class="navbar-item">
              <router-link class="button is-primary" to="/polls">Polls</router-link>
              <a class="button is-primary" @click="openForm" v-show="!!username">
                <strong>Create Poll</strong>
              </a>
            </div>
            <div class="navbar-end" v-show="!username">
              <div class="navbar-item">
                <div class="buttons">
                  <a class="button is-primary" @click="register">
                    <strong>Sign up</strong>
                  </a>
                  <router-link class="button is-light" to="/login">Log In</router-link>
                </div>
              </div>
            </div>
            <div class="navbar-end" v-show="!!username">
              <a class="navbar-item" :href="userLink">
                <strong>{{ username }}</strong>
              </a>
              <div class="navbar-item">
                <div class="buttons">
                  <logoutButton />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="hero-body" v-show="showGeneralHeader">
        <div class="container has-text-centered">
          <h1 class="title">{{ currentRouteName }}</h1>
        </div>
      </div>
    </section>
    <CreatePollForm
      @close="closeForm" 
      :class="{'is-active': showCreatePollForm}">
    </CreatePollForm>
    <router-view />
  </div>
</template>

<script>
import logoutButton from '@/components/Logout'
import CreatePollForm from '@/components/CreatePollForm'
import { fetchUserVotedPolls } from '@/api'

export default {
  name: 'App',
  components: {
    logoutButton,
    CreatePollForm
  },
  data: function() {
    return  {
      loadedVotedPolls: false ,
      showCreatePollForm: false
      }
  },
  computed: {
    username() {
      if (!this.$store.state.user) {
        return null
      }
      return this.$store.state.user.username
    },
    currentRouteName() {
      return this.$route.name
    },
    userLink() {
      if(this.$store.getters.loggedIn){
        return 'user/' + this.$store.state.user.id
      }
      return ''
    },
    showGeneralHeader() {
      if (['Polls'].includes(this.$route.name)) {
        return true
      }
      return false
    }
  },
  watch: {
    username: function() {
      if (this.username && !this.loadedVotedPolls) {
        fetchUserVotedPolls(this.$store.getters.getAuthHeader, this.$store.state.user.id)
        .then(response => response.json())
        .then(data => {
          console.log(data);
          this.$store.commit('updateVotedPolls', data);
          this.loadedVotedPolls = true;          
        })
      }
    }
  },
  methods: {
    register() {
      this.$router.push('/register')
    },
    openForm: function() {
      this.showCreatePollForm = true;
    },
    closeForm: function() {
      this.showCreatePollForm = false;
    },
  }
}
</script>

<style lang="scss">
    @import '~bulma/bulma.sass';
</style>
