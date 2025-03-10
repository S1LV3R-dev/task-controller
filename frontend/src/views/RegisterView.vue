<script lang="ts" setup>
import { register } from '@/utils/functions'
import { ref } from 'vue'
import { RouterLink } from 'vue-router'

const username = ref('')
const email = ref('')
const password = ref('')
</script>

<template>
  <div class="container d-flex align-items-center justify-content-center min-vh-100">
    <div class="card shadow" style="width: 100%; max-width: 400px">
      <div class="card-body">
        <h3 class="card-title text-center mb-4">Create an Account</h3>
        <div class="mb-3 text-center">
          <RouterLink to="/login" class="btn btn-outline-secondary" active-class="active">
            Login
          </RouterLink>
          <RouterLink to="/register" class="btn btn-outline-primary ms-2" active-class="active">
            Register
          </RouterLink>
        </div>
        <div class="mb-3">
          <label for="username" class="form-label">Username</label>
          <input
            id="username"
            type="text"
            class="form-control"
            placeholder="Enter username"
            v-model="username"
          />
        </div>
        <div class="mb-3">
          <label for="email" class="form-label">Email</label>
          <input
            id="email"
            type="email"
            class="form-control"
            placeholder="Enter email"
            v-model="email"
          />
        </div>
        <div class="mb-3">
          <label for="password" class="form-label">Password</label>
          <input
            id="password"
            type="password"
            class="form-control"
            placeholder="Enter password"
            v-model="password"
          />
        </div>
        <button @click="register(username, email, password)" class="btn btn-primary w-100">
          Register
        </button>
      </div>
    </div>
  </div>
</template>
