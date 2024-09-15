import { createRouter, createWebHistory } from 'vue-router'
// import HomeView from '../views/HomeView.vue'
import HomePage from '../views/HomePage.vue';
import PlaceholderPage from '../views/PlaceholderPage.vue';

const routes = [
  // {
  //   path: '/',
  //   name: 'home',
  //   component: HomeView
  // },
  // {
  //   path: '/about',
  //   name: 'about',
  //   // route level code-splitting
  //   // this generates a separate chunk (about.[hash].js) for this route
  //   // which is lazy-loaded when the route is visited.
  //   component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  // },
  { path: '/', name: 'Home', component: HomePage },
  { path: '/clusters', name: 'Clusters', component: PlaceholderPage },
  { path: '/eda', name: 'EDA', component: PlaceholderPage },
  { path: '/classification', name: 'Classification', component: PlaceholderPage },
  { path: '/about', name: 'About', component: PlaceholderPage },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
