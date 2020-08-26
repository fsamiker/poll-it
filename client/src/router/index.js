import Vue from 'vue'
import VueRouter from 'vue-router'
import Polls from '@/views/Polls.vue'
import Login from '@/views/Login.vue'
import Register from '@/views/Register.vue'
import PollDetailed from '@/views/PollDetailed'
import User from '@/views/User.vue'

Vue.use(VueRouter)

  const routes = [
  {
    path: '/polls',
    name: 'Polls',
    component: Polls,
    props: {user_id: null}
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/register',
    name: 'Register',
    component: Register
  },
  {
    path: '/poll/:id',
    name: 'Poll',
    component: PollDetailed
  },
  {
    path: '/user/:id',
    name: 'User',
    component: User
  },
  {
    path: '/',
    name: 'Home',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/Home.vue')
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
