<template>
  <div class="login">
    <h1>登录</h1>
    <LoginForm @submit="handleLogin" />
    <p v-if="error" class="error">{{ error }}</p>
    <router-link to="/register">没有账号？立即注册</router-link>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import LoginForm from '@/components/LoginForm.vue'

export default {
  components: { LoginForm },
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    const error = ref('')

    const handleLogin = async (credentials) => {
      try {
        await authStore.login(credentials)
        router.push('/')
      } catch (err) {
        error.value = '登录失败，请检查用户名和密码'
      }
    }

    return {
      handleLogin,
      error
    }
  }
}
</script>

<style>
.error {
  color: red;
}
</style>