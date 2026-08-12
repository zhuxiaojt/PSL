import { createRouter, createWebHashHistory } from "vue-router";
import Home from '../views/HomeView.vue'
import Security from '../views/SecurityView.vue'
import More from '../views/MoreView.vue'
import Settings from '../views/SettingsView.vue'

const routes = [
    {
        path: '/',
        component: Home
    },
    {
        path: '/security',
        component: Security
    },
    {
        path: '/more',
        component: More
    },
    {
        path: '/settings',
        component: Settings
    }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

export default router;