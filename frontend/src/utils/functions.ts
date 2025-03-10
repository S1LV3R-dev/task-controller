import axios from 'axios'
import router from '@/router/index'
import { useToast } from 'vue-toastification'

axios.defaults.withCredentials = true
const toast = useToast()

// ✅ Global Axios Response Interceptor for 403 Errors
axios.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 403) {
      const requestUrl = error.config.url
      if (!requestUrl?.includes('/login') && !requestUrl?.includes('/register')) {
        toast.error('Invalid authentication token. Please login again.')
        router.replace('/login')
      }
    }
    return Promise.reject(error)
  },
)

export async function login(login_str: string, password: string) {
  return axios
    .post('http://localhost:8000/login', { login_str, password })
    .then(() => router.push('/'))
    .catch((error) => {
      if (error.response?.status === 401) toast.error('Invalid credentials')
    })
}

export async function register(username: string, email: string, password: string) {
  return axios
    .post('http://localhost:8000/register', { username, email, password })
    .then(() => router.push('/'))
    .catch((error) => {
      if (error.response?.status === 409) toast.error('Email already in use')
    })
}

export async function get_tasks() {
  return axios.get('http://localhost:8000/tasks').then((response) => response.data)
}

export async function get_task_by_id(task_id: number) {
  return axios.get(`http://localhost:8000/tasks/${task_id}`).then((response) => response.data)
}

export async function update_task(
  task_id: number,
  taskTitle: string,
  taskDescription: string,
  deadline: Date,
  status: number,
) {
  return axios
    .put(
      `http://localhost:8000/tasks/${task_id}`,
      {
        name: taskTitle,
        description: taskDescription,
        deadline,
        status,
      },
      {
        headers: { 'Content-Type': 'application/json' },
      },
    )
    .then((response) => response.data)
}

export async function delete_task(task_id: number) {
  return axios.delete(`http://localhost:8000/tasks/${task_id}`).then((response) => response.data)
}

export async function create_task(
  taskTitle: string,
  taskDescription: string,
  deadline: Date,
  status: number,
) {
  return axios
    .post('http://localhost:8000/tasks', {
      name: taskTitle,
      description: taskDescription,
      deadline,
      status,
    })
    .then((response) => response.data[0])
}

export async function change_status(task_id: number, status: number) {
  return axios
    .patch(`http://localhost:8000/tasks/${task_id}?status=${status}`)
    .then((response) => response.data)
}

export async function logout() {
  return axios.post('http://localhost:8000/logout')
}
