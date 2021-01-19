import Vue from 'vue'
import Router from 'vue-router'

import NotFound from '@/components/NotFound'
import DEMO from '@/components/DEMO'

Vue.use(Router)


const router = new Router({
    mode: 'history',
    routes: [
        {path: '/', name: 'index', component: DEMO},
        {path: '*', component: NotFound}
    ]
})

export default router