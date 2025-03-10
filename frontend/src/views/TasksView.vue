<script lang="ts" setup>
import { ref, onBeforeUnmount, onBeforeMount } from 'vue'
import { useRouter } from 'vue-router'
import { get_tasks, delete_task, logout, change_status } from '@/utils/functions'
import { TASK_STATUS } from '@/utils/task_configs'

const router = useRouter()
const tasks = ref([])
const ws = ref<WebSocket | null>(null)

const columns = [
  { field: 'id', hidden: true },
  {
    label: 'Title',
    field: 'name',
    filterOptions: { enabled: true, placeholder: 'Search' },
  },
  {
    label: 'Description',
    field: 'description',
    filterOptions: { enabled: true, placeholder: 'Search' },
  },
  {
    label: 'Status',
    field: 'status',
    filterOptions: {
      enabled: true,
      filterDropdownItems: [
        { value: '0', text: 'new' },
        { value: '1', text: 'active' },
        { value: '2', text: 'finished' },
        { value: '-1', text: 'cancelled' },
      ],
    },
  },
  {
    label: 'Deadline',
    field: 'deadline',
    type: 'date',
    dateInputFormat: "yyyy-MM-dd'T'HH:mm:ss",
    dateOutputFormat: 'MMM do yy',
  },
  { label: 'Created by', field: 'username' },
  { label: 'Actions', field: 'actions', sortable: false, html: true },
]

const paginationOptions = {
  enabled: true,
  mode: 'records',
  perPage: 5,
  position: 'bottom',
  perPageDropdown: [10, 15, 20],
  dropdownAllowAll: false,
  nextLabel: 'Next',
  prevLabel: 'Prev',
  rowsPerPageLabel: 'Rows per page',
  ofLabel: 'of',
  pageLabel: 'page',
  allLabel: 'All',
}

async function fetchTasks() {
  try {
    const response = await get_tasks()
    tasks.value = response.map((task: { id: number; status: number; deadline: string }) => ({
      ...task,
      deadline: task.deadline.split('.')[0],
    }))
  } catch (error) {
    console.error('Error fetching tasks:', error)
  }
}

async function deleteTask(taskId: string) {
  try {
    await delete_task(taskId)
    tasks.value = tasks.value.filter((task: { id: string }) => task.id !== taskId)
  } catch (error) {
    console.error('Error deleting task:', error)
  }
}

function setupWebSocket() {
  ws.value = new WebSocket('ws://localhost:8000/ws/tasks')

  ws.value.onmessage = (event) => {
    const { task_id, status } = JSON.parse(event.data)
    const task = tasks.value.find((t: { id: string }) => t.id === task_id)
    if (task) {
      ;(task as { id: number; status: number }).status = status
    }
  }
}

async function logoutUser() {
  try {
    await logout()
    router.push('/login')
  } catch (error) {
    console.error('Error logging out:', error)
  }
}

onBeforeMount(async () => {
  await fetchTasks()
  setupWebSocket()
})

onBeforeUnmount(() => {
  ws.value?.close()
})
</script>

<template>
  <div class="container my-5">
    <div class="card shadow">
      <div class="card-header d-flex justify-content-between align-items-center">
        <h4 class="mb-0">Tasks</h4>
        <div>
          <RouterLink to="/tasks/new" class="btn btn-primary me-2"> Create Task </RouterLink>
          <button @click="logoutUser" class="btn btn-secondary">Logout</button>
        </div>
      </div>
      <div class="card-body p-0">
        <div class="table-responsive" style="overflow-x: auto">
          <vue-good-table
            :columns="columns"
            :rows="tasks"
            :pagination-options="paginationOptions"
            class="custom-table"
          >
            <template #table-row="props">
              <span v-if="props.column.field === 'actions'">
                <div class="d-none d-md-block">
                  <RouterLink
                    :to="`/tasks/${props.row.id}`"
                    class="btn btn-sm btn-outline-info me-2"
                  >
                    Edit
                  </RouterLink>
                  <button @click="deleteTask(props.row.id)" class="btn btn-sm btn-outline-danger">
                    Delete
                  </button>
                </div>
                <div class="d-block d-md-none">
                  <button
                    class="btn btn-sm btn-outline-secondary dropdown-toggle"
                    data-bs-toggle="dropdown"
                  >
                    Actions
                  </button>
                  <ul class="dropdown-menu form-select">
                    <li>
                      <RouterLink :to="`/tasks/${props.row.id}`" class="dropdown-item"
                        >Edit</RouterLink
                      >
                    </li>
                    <li>
                      <button @click="deleteTask(props.row.id)" class="dropdown-item text-danger">
                        Delete
                      </button>
                    </li>
                  </ul>
                </div>
              </span>

              <span v-else-if="props.column.field === 'status'">
                <select
                  class="form-select form-select-sm"
                  v-model="props.row.status"
                  @change="change_status(props.row.id, props.row.status)"
                >
                  <option v-for="(label, key) in TASK_STATUS.dict" :value="key" :key="key">
                    {{ label }}
                  </option>
                </select>
              </span>
              <span v-else>
                {{ props.formattedRow[props.column.field] }}
              </span>
            </template>
          </vue-good-table>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
@media (max-width: 768px) {
  .custom-table {
    font-size: 12px;
  }

  .form-select-sm {
    font-size: 12px;
  }
}

.custom-table select {
  appearance: none;
  -webkit-appearance: none;
  -moz-appearance: none;
  background-image: none;
}

.custom-table select:focus {
  outline: none;
  border: 1px solid #aaa;
}

.form-select {
  padding: 0.25rem !important;
}
</style>
