import Vue from 'vue'
import Router from 'vue-router'

// Containers
const TheContainer = () => import('@/containers/TheContainer')

// Views
const Login = () => import('@/views/Login')

// Manage
const InjectionData = () => import('@/views/manager/injectiondata')
const CncosciData = () => import('@/views/manager/cncoscidata')
const CncpowerData = () => import('@/views/manager/cncpowerdata')
const Dashboard = () => import('@/views/manager/dashboard')
const Dashboard_Power = () => import('@/views/manager/dashboard_power')
const Users = () => import('@/views/manager/users')




Vue.use(Router)

export default new Router({
  mode: 'hash', // https://router.vuejs.org/api/#mode
  linkActiveClass: 'active',
  scrollBehavior: () => ({ y: 0 }),
  routes: configRoutes()
})

function configRoutes () {
  return [
    // {
    //   path: '/login',
    //   redirect: '/login',
    //   name: '로그인',
    //   component:Login,
    // },
    {
      path: '/',
      redirect: '/login',
      name: '메인',
      component: TheContainer,
      children: [
        {
          path: 'manager',
          name: '관리',
          component: {
            render (c) { return c('router-view') }
          },
          children: [
            {
              path: 'dashboard',
              name: '실시간 대시보드(진동)',
              component: Dashboard
            },
            {
              path: 'dashboard_power',
              name: '실시간 대시보드(전력)',
              component: Dashboard_Power
            },            
            {
              path: 'injectiondata',
              name: '사출기 데이터',
              component: InjectionData
            },
            {
              path: 'cncoscidata',
              name: '공작기계 진동 데이터',
              component: CncosciData
            },
            {
              path: 'cncpower',
              name: '공작기계 전력 데이터',
              component: CncpowerData
            },
            {
              path: 'users',
              name: '사용자관리',
              component: Users
            },
          ]
        },
     ]
    }
  ]
}

