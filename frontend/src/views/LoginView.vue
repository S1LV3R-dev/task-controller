<script lang="ts" setup>
import { login } from "@/utils/functions"
import { ref } from "vue";
import { RouterLink } from "vue-router";

const login_str = ref('')
const password = ref('')

</script>

<template>
    <div class="container d-flex align-items-center justify-content-center min-vh-100">
      <div class="card shadow" style="width: 100%; max-width: 400px;">
        <div class="card-body">
          <h3 class="card-title text-center mb-4">Welcome Back</h3>
          <div class="mb-3 text-center">
            <RouterLink to="/login" class="btn btn-outline-primary" active-class="active">Login</RouterLink>
            <RouterLink to="/register" class="btn btn-outline-secondary ms-2" active-class="active">Register</RouterLink>
          </div>
          <div class="mb-3">
            <label for="login_str" class="form-label">Username or Email</label>
            <input
              id="login_str"
              type="text"
              class="form-control"
              placeholder="Enter username or email"
              v-model="login_str"
            >
          </div>
          <div class="mb-3">
            <label for="password" class="form-label">Password</label>
            <input
              id="password"
              type="password"
              class="form-control"
              placeholder="Enter password"
              v-model="password"
            >
          </div>
          <button @click="login(login_str, password)" class="btn btn-primary w-100">
            Login
          </button>
        </div>
      </div>
    </div>
  </template>
