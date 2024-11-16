import { createRouter, createWebHistory } from 'vue-router'
import Home from '../renderer/components/Home.vue'
import HelloWorld from '../renderer/components/HelloWorld.vue'

const routes = [
  { path: '/', component: Home },
  { path: '/hello', component: HelloWorld }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router