const routes = [
  {
    path: '/',
    component: () => import('layouts/TaskMainLayout.vue'),
    children: [
      { path: '', component: () => import('pages/LoginPage.vue') },
      { path: '*', component: () => import('pages/LoginPage.vue') },
      { path: '/login', component: () => import('pages/LoginPage.vue') },
      { path: '/signup', component: () => import('src/pages/signup/IndexPage.vue') },
      { path: '/tasks', component: () => import('components/tasks/IndexPage'), meta: { requireLogin: true } },
      { path: '/admin', component: () => import('pages/admin/IndexPage'), meta: { requireLogin: true } }
    ]
  },
  {
    name: 'LoginIn',
    path: '/login',
    component: () => import('src/pages/LoginPage.vue')
  // },
  // {
  //   name: 'SignUp',
  //   path: '/signup',
  //   component: () => import('src/pages/signup/IndexPage.vue')
  // },
  // {
  //   name: 'Tasks',
  //   path: '/tasks',
  //   component: () => import('pages/tasks/IndexPage.vue')
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue')
  }
]

export default routes
