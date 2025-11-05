import { createRouter, createWebHistory } from 'vue-router'
import Login from './components/Login.vue'
import Dashboard from './components/Dashboard.vue'
import BookView from './components/BookView.vue'
const routes = [
  { path: '/', component: Login },
  { path: '/dashboard', component: Dashboard },
  { path: '/books/:name', component: BookView }
]
export default createRouter({ history: createWebHistory(), routes })
