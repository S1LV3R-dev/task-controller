import api from '@/utils/api'
import router from '@/router'
import { createToastInterface } from 'vue-toastification'

const toast = createToastInterface()

export async function login(login_str: string, password: string) {
  return api
    .post('/login', { login_str, password }) // ✅ Base URL is now handled in api.ts
    .then(() => router.push('/'))
    .catch((error) => {
      if (error.response?.status === 401) toast.error('Invalid credentials')
    })
}

export async function register(username: string, email: string, password: string) {
  return api
    .post('/register', { username, email, password })
    .then(() => router.push('/'))
    .catch((error) => {
      if (error.response?.status === 409) toast.error('Email already in use')
    })
}

export async function get_tasks() {
  return api.get('/tasks').then((response) => response.data)
}

export async function get_task_by_id(task_id: string) {
  return api.get(`/tasks/${task_id}`).then((response) => response.data)
}

export async function update_task(
  task_id: string,
  taskTitle: string,
  taskDescription: string,
  deadline: Date,
  status: number,
) {
  return api
    .put(
      `/tasks/${task_id}`,
      { name: taskTitle, description: taskDescription, deadline, status },
      { headers: { 'Content-Type': 'application/json' } },
    )
    .then((response) => response.data)
}

export async function delete_task(task_id: string) {
  return api.delete(`/tasks/${task_id}`).then((response) => response.data)
}

export async function create_task(
  taskTitle: string,
  taskDescription: string,
  deadline: Date,
  status: number,
) {
  return api
    .post('/tasks', { name: taskTitle, description: taskDescription, deadline, status })
    .then((response) => response.data[0])
}

export async function change_status(task_id: number, status: number) {
  return api.patch(`/tasks/${task_id}?status=${status}`).then((response) => response.data)
}

export async function logout() {
  return api
    .post('/logout')
    .then(() => {
      router.replace('/login') // ✅ Redirect to login after logout
    })
    .catch((error) => {
      console.error('Logout Error:', error)
      toast.error('Failed to logout')
    })
}
