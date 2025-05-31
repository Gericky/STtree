<template>
  <div class="teacher-detail">
    <div v-if="loading">加载中...</div>
    <div v-else-if="teacher">
      <h1>{{ teacher.name }}</h1>
      <img v-if="teacher.avatar" :src="teacher.avatar" :alt="teacher.name" class="avatar">
      <h2>{{ teacher.school }}</h2>
      <p>{{ teacher.details }}</p>
      <router-link to="/">返回首页</router-link>
    </div>
    <div v-else>
      <p>找不到该教师信息</p>
      <router-link to="/">返回首页</router-link>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import api from '@/api'

export default {
  props: ['name'],
  setup(props) {
    const route = useRoute()
    const teacher = ref(null)
    const loading = ref(true)

    const fetchTeacher = async () => {
      try {
        const name = props.name || route.params.name
        const response = await api.getTeacher(name)
        teacher.value = response.data
      } catch (error) {
        console.error('获取教师详情失败:', error)
      } finally {
        loading.value = false
      }
    }

    onMounted(fetchTeacher)

    return {
      teacher,
      loading
    }
  }
}
</script>

<style>
.teacher-detail {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
}

.avatar {
  max-width: 200px;
  max-height: 200px;
  border-radius: 50%;
}
</style>