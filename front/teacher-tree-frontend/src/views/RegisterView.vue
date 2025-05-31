<template>
  <div class="register">
    <h1>注册</h1>
    <RegisterForm @submit="handleRegister" />
    <p v-if="error" class="error">{{ error }}</p>
    <p v-if="success" class="success">注册成功！<router-link to="/login">立即登录</router-link></p>
    <router-link to="/login">已有账号？立即登录</router-link>
  </div>
</template>

<script>
import { ref } from 'vue'
import RegisterForm from '@/components/RegisterForm.vue'
import { useAuthStore } from '@/stores/auth'

export default {
  components: { RegisterForm },
  setup() {
    const authStore = useAuthStore()
    const error = ref('')
    const success = ref(false)

    const handleRegister = async (user) => {
      try {
        await authStore.register(user)
        success.value = true
        error.value = ''
      } catch (err) {
        error.value = '注册失败: ' + (err.response?.data?.message || err.message)
        success.value = false
      }
    }

    return {
      handleRegister,
      error,
      success
    }
  }
}
</script>

<style>
.error {
  color: red;
}
.success {
  color: green;
}
</style>