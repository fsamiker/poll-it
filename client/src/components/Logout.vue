<template>
  <a class="button is-light" @click="logout" id="logout">
    <strong>Log Out</strong>
  </a>
</template>

<script>
export default {
  name: 'logoutButton',
  methods: {
      logout: function() {
          this.$store.dispatch('logout');
          if (this.$router.name != 'Login') {
            this.$router.push('/login')
          }
      }
  }
}
</script>