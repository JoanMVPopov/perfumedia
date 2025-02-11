import { createRouter, createWebHistory } from 'vue-router'
// import HomeView from '../views/HomeView.vue'
import HomePage from '../views/HomePage.vue';
import PlaceholderPage from '../views/PlaceholderPage.vue';
import EDAPage from "@/views/EDAPage.vue";
import PerfumeFinderPage from "@/views/PerfumeFinderPage.vue";
import ClustersPage from "@/views/ClustersPage.vue";

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
  { path: '/', name: 'Home', component: HomePage, meta: { title: "Perfumedia | Home" }  },
  { path: '/clusters', name: 'Clusters', component: ClustersPage, meta: { title: "Perfumedia | Clusters" }  },
  { path: '/etl', name: 'ETL', component: PlaceholderPage, meta: { title: "Perfumedia | ETL" }  },
  { path: '/eda', name: 'EDA', component: EDAPage, meta: { title: "Perfumedia | EDA" } },
  { path: '/finder', name: 'Perfume Finder', component: PerfumeFinderPage, meta: { title: "Perfumedia | Finder" }  },
  { path: '/about', name: 'About', component: PlaceholderPage, meta: { title: "Perfumedia | About" }  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
