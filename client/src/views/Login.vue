<template>
    <div class="hero-body">
        <div class="container is-centered login-form mt-6">
            <div class="field">
                <label class="label">Username</label>
                <div class="control has-icons-left has-icons-right">
                    <input class="input" type="text" placeholder="Text input" value="bulma" v-model="username">
                    <span class="icon is-small is-left">
                        <i class="fas fa-user"></i>
                    </span>
                </div>
            </div>

            <div class="field">
                <label class="label">Password</label>
                <div class="control has-icons-left has-icons-right">
                    <input class="input" type="password" placeholder="Password Input" value="hello@" v-model="password">
                    <span class="icon is-small is-left">
                        <i class="fas fa-lock"></i>
                    </span>
                </div>
            </div>

            <div class="field is-grouped is-grouped-centered">
                <div class="control">
                    <a class="button is-large is-primary" @click="login">Login</a>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'Login',
    data: function() {
        return {
            username: '',
            password: ''
        }
    },
    methods: {
        login: function() {
            this.$store.dispatch('login', {username: this.username, password: this.password})
            .then(() => {
                this.username = '';
                this.password = '';
                this.$router.push('/polls');
                });
        }
    }
}
</script>

<style scoped>
.login-form {
    width: auto;
    max-width: 600px;
}
</style>