<script lang="ts" setup>
import { onBeforeMount, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import Vue3DatePicker from 'vue3-datepicker';
import { get_task_by_id, update_task, delete_task, create_task } from '@/utils/functions';

const route = useRoute();
const router = useRouter();

const taskTitle = ref('');
const taskDescription = ref('');
const taskDeadline = ref(new Date());
const taskStatus = ref(0);
const taskCreatedBy = ref(0);
const taskId = ref(route.params.task_id as string);

const isEditMode = ref(false);

async function createTask() {
  try {
    const taskData = await create_task(taskTitle.value, taskDescription.value, taskDeadline.value, 0);
    isEditMode.value = true;
    taskId.value = taskData.id;
    router.push(`/tasks/${taskData.id}`);
  } catch (error) {
    console.error('Error creating task:', error);
  }
}

onBeforeMount(async () => {
  if (taskId.value && taskId.value !== 'new') {
    try {
      const task = await get_task_by_id(taskId.value);
      if (task) {
        isEditMode.value = true;
        taskTitle.value = task.name;
        taskDescription.value = task.description;
        taskDeadline.value = new Date(task.deadline);
        taskStatus.value = task.status;
        taskCreatedBy.value = task.created_by;
      }
    } catch (error) {
      console.error('Error fetching task by ID:', error);
    }
  }
});
</script>


<template>
  <div class="container my-5">
    <div class="d-flex justify-content-between mb-3">
      <button @click="$router.push('/')" class="btn btn-outline-secondary">
        ← Back
      </button>
    </div>
    <div class="card shadow">
      <div class="card-header">
        <h3 class="mb-0">{{ isEditMode ? 'Edit Task' : 'Create Task' }}</h3>
      </div>
      <div class="card-body">
        <form>
          <div class="mb-3">
            <label for="title" class="form-label">Title</label>
            <input
              id="title"
              type="text"
              class="form-control"
              v-model="taskTitle"
              placeholder="Enter task title"
            />
          </div>
          <div class="mb-3">
            <label for="description" class="form-label">Description</label>
            <textarea
              id="description"
              class="form-control"
              v-model="taskDescription"
              placeholder="Enter task description"
              rows="3"
            ></textarea>
          </div>
          <div class="mb-3">
            <label for="deadline" class="form-label">Deadline</label>
            <Vue3DatePicker
              id="deadline"
              v-model="taskDeadline"
              :typeable="false"
              class="form-control"
            />
          </div>
          <div class="d-flex justify-content-end">
            <div v-if="isEditMode">
              <button
                type="button"
                @click="update_task(taskId, taskTitle, taskDescription, taskDeadline, taskStatus)"
                class="btn btn-primary me-2"
              >
                Update Task
              </button>
              <button
                type="button"
                @click="delete_task(taskId)"
                class="btn btn-danger"
              >
                Delete Task
              </button>
            </div>
            <div v-else>
              <button type="button" @click="createTask" class="btn btn-success">
                Create Task
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>
