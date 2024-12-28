import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import './assets/tailwind.css';
import apiClient from './api'


createApp(App).use(store).use(router, apiClient).mount('#app')

router.beforeEach((to, from, next) => {
  if (to.meta.title) {
    document.title = to.meta.title; // Set the page title dynamically
  }
  next();
});