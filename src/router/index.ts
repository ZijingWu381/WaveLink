import { createRouter, createWebHistory } from 'vue-router'
import Home from '../renderer/components/Home.vue'
import HelloWorld from '../renderer/components/HelloWorld.vue'
import Loader from '../renderer/components/Loader.vue'

const routes = [
  { path: '/', component: Home },
  { path: '/hello', component: HelloWorld },
  { path: '/loader', component: Loader},
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router