<template>
  <div class="home">
    <h1 style="text-align: center;">师承关系树</h1>
    <TreeView v-if="treeData" :data="treeData" />
    <p v-else>加载中...</p>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import TreeView from '@/components/TreeView.vue'
import api from '@/api'

export default {
  components: { TreeView },
  setup() {
    const treeData = ref(null)

    const fetchTree = async () => {
      try {
        const response = await api.getTree()
        treeData.value = response.data
        console.log(treeData.value)

      } catch (error) {
        console.error('获取师承树失败:', error)
      }
    }

    onMounted(fetchTree)

    return {
      treeData
    }
  }
}
</script>