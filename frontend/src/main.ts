import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import Toast from 'vue-toastification'
import VueGoodTablePlugin from 'vue-good-table-next'
import 'bootstrap'

const app = createApp(App)

// import the styles
import 'vue-good-table-next/dist/vue-good-table-next.css'
import 'vue-toastification/dist/index.css'
import 'vue-multiselect/dist/vue-multiselect.min.css'
import 'bootstrap/dist/css/bootstrap.min.css'

app.use(router)
app.use(Toast)
app.use(VueGoodTablePlugin)

app.mount('#app')
