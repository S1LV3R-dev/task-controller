import { createRouter, createWebHistory } from 'vue-router'
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'Login',
      component: () => import('@/views/LoginView.vue'),
    },
    {
      path: '/register',
      name: 'Register',
      component: () => import('@/views/RegisterView.vue'),
    },
    {
      path: '/',
      name: 'Tasks',
      component: () => import('@/views/TasksView.vue'),
    },
    {
      path: '/tasks/:task_id?',
      name: 'Task Form',
      component: () => import('@/views/TaskForm.vue'),
    },
  ],
})

export default router
