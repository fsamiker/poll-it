<template>
    <div class="hero-body">
        <div class="container is-centered register-form mt-6">
            <div class="field">
                <label class="label">Email</label>
                <div class="control has-icons-left has-icons-right">
                    <input class="input" type="email" placeholder="Email input" v-model="email">
                    <span class="icon is-small is-left">
                    <i class="fas fa-envelope"></i>
                    </span>
                </div>
            </div>

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
                    <a class="button is-medium is-primary" @click="submitRegistration">Submit</a>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { createUser } from '@/api'

export default {
    name: 'Register',
    data: function() {
        return {
            name: '',
            email: '',
            username: '',
            password: '',
        }
    },
    methods: {
        submitRegistration: function() {
            let payload = {
                'name': this.name,
                'email': this.email,
                'username': this.username,
                'password': this.password
            }
            createUser(payload)
            .then(response => response.json())
            .then(data => {
                console.log(data);
                this.clearForm();
                this.$router.push('/login')
            })

        },
        clearForm: function() {
            this.name = '';
            this.email = '';
            this.username = '';
            this.password = '';
        }
    }
}
</script>

<style scoped>
.register-form {
    width: auto;
    max-width: 600px;
}
</style>