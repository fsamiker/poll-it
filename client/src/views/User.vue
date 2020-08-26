<template>
    <div class="user">
        <section class="hero is-primary">
            <div class="hero-body">
            <div class="container has-text-centered">
                <h2 class="title"> {{ userData.username }}'s Polls </h2>
            </div>
            </div>
        </section>
        <Polls :user_id="user_id"></Polls>
    </div>
</template>

<script>
import Polls from './Polls'
import { fetchUser } from '@/api'

export default {
  name: "User",
  data: function() {
      return {
          userData: {}
      }
  },
  components: {
      Polls
  },
  computed: {
      user_id: function() {
          return this.$route.params.id
      }
  },
  created: function() {
      this.getUserData();
  },
  methods: {
      getUserData: function() {
          fetchUser(this.user_id)
          .then(response => response.json())
          .then(data => {
              this.userData = data;
          })
      }
  }
};
</script>

<style scoped>
</style>
