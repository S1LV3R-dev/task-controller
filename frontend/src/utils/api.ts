import axios from 'axios'
import router from '@/router'
import { createToastInterface } from 'vue-toastification'

axios.defaults.withCredentials = true

const toast = createToastInterface()

console.log('Registering Axios interceptor') // Debugging step

const api = axios.create({
  baseURL: 'http://localhost:8000', // ✅ Set base URL
})

api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.log('Axios Interceptor Triggered:', error.response) // Debugging

    if (error.response?.status === 403) {
      const requestUrl = error.config?.url
      if (!requestUrl?.includes('/login') && !requestUrl?.includes('/register')) {
        toast.error('Invalid authentication token. Please login again.')
        router.replace('/login')
      }
    }

    return Promise.reject(error)
  },
)

export default api
