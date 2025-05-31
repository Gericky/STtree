<template>
  <form @submit.prevent="submit">
    <div>
      <label for="username">用户名:</label>
      <input id="username" v-model="form.username" type="text" required>
    </div>
    <div>
      <label for="password">密码:</label>
      <input id="password" v-model="form.password" type="password" required>
    </div>
    <div>
      <label for="confirmPassword">确认密码:</label>
      <input id="confirmPassword" v-model="form.confirmPassword" type="password" required>
    </div>
    <button type="submit" :disabled="isSubmitting">
      {{ isSubmitting ? '注册中...' : '注册' }}
    </button>
  </form>
</template>

<script>
import { ref } from 'vue'

export default {
  emits: ['submit'],
  setup(props, { emit }) {
    const form = ref({
      username: '',
      password: '',
      confirmPassword: ''
    })
    const isSubmitting = ref(false)

    const submit = () => {
      if (form.value.password !== form.value.confirmPassword) {
        alert('两次输入的密码不一致')
        return
      }
      
      isSubmitting.value = true
      emit('submit', {
        username: form.value.username,
        password: form.value.password
      })
      isSubmitting.value = false
    }

    return {
      form,
      isSubmitting,
      submit
    }
  }
}
</script>