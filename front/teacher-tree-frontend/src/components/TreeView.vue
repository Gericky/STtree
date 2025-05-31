<template>
  <div class="tree-container">
    <h2 class="tree-title">师承关系图谱</h2>
    <div class="tree-wrapper" ref="treeWrapper">
      <svg class="tree-connections" ref="svgElement"></svg>
      <div class="tree-nodes">
        <TreeNode 
          v-for="node in flattenedNodes" 
          :key="node.id"
          :node="node"
          :style="{
            left: `${node.x}px`,
            top: `${node.y}px`
          }"
          @node-click="onNodeClick"
        />
      </div>
    </div>

    <!-- 节点操作菜单 -->
    <el-dialog
      v-model="showMenu"
      title="节点操作"
      width="30%"
      :before-close="handleClose"
    >
      <div class="node-menu">
        <el-button type="primary" @click="showAddNodeDialog">添加关系</el-button>
        <el-button type="primary" @click="showAddNodeDialog">删除节点</el-button>
        <el-button @click="showDetail">查看详细信息</el-button>
        <el-button @click="showDetail">修改详细信息</el-button>
      </div>
    </el-dialog>

    <!-- 添加节点对话框 -->
    <el-dialog
      v-model="showAddDialog"
      title="添加子节点"
      width="50%"
    >
      <el-form :model="newNodeForm" label-width="80px">
        <el-form-item label="姓名" required>
          <el-input v-model="newNodeForm.name" placeholder="请输入姓名"></el-input>
        </el-form-item>
        <el-form-item label="学校">
          <el-input v-model="newNodeForm.school" placeholder="请输入学校"></el-input>
        </el-form-item>
        <el-form-item label="职称">
          <el-input v-model="newNodeForm.school1" placeholder="请输入职称"></el-input>
        </el-form-item>
        <el-form-item label="链接">
            <el-input v-model="newNodeForm.school2" placeholder="请输入链接"></el-input>
        </el-form-item>
        <el-form-item label="头像">
            <el-input v-model="newNodeForm.school3" placeholder="请输入头像"></el-input>
        </el-form-item>
        <el-form-item label="详情">
          <el-input 
            type="textarea" 
            v-model="newNodeForm.details" 
            placeholder="请输入详情"
            :rows="3"
          ></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showAddDialog = false">取消</el-button>
          <el-button type="primary" @click="addNewNode">确认添加</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import TreeNode from './TreeNode.vue'
import api from '@/api'
import { ElMessage } from 'element-plus'

// 按需引入 Element Plus 组件
import {
  ElDialog,
  ElButton,
  ElForm,
  ElFormItem,
  ElInput
} from 'element-plus'

export default {
  name: 'TreeView',
  components: { 
    TreeNode,
    ElDialog,
    ElButton,
    ElForm,
    ElFormItem,
    ElInput
  },
  props: {
    data: {
      type: Object,
      required: true
    }
  },
  setup(props) {
    const router = useRouter()
    const nodePositions = ref({})
    const svgElement = ref(null)
    const treeWrapper = ref(null)
    
    // 新增状态
    const showMenu = ref(false)
    const showAddDialog = ref(false)
    const selectedNode = ref(null)
    const newNodeForm = ref({
      name: '',
      school: '',
      details: ''
    })

    // 计算节点布局
    const flattenedNodes = computed(() => {
      const nodes = []
      const calculateLayout = (node, x = 0, y = 0, level = 0) => {
        const id = node.id
        const width = 120
        const height = 60
        const spacing = {
          x: 200,
          y: 100
        }
        
        // 计算位置
        const posX = x
        const posY = y + (level * spacing.y)
        
        nodePositions.value[id] = { x: posX, y: posY, width, height }
        
        nodes.push({
          ...node,
          x: posX,
          y: posY,
          level
        })
        
        // 计算子节点位置
        if (node.children && node.children.length) {
          const childrenWidth = (node.children.length - 1) * spacing.x
          const startX = x - (childrenWidth / 2)
          
          node.children.forEach((child, index) => {
            calculateLayout(child, startX + (index * spacing.x), y, level + 1)
          })
        }
      }
      
      // 从容器中心开始计算
      const startX = treeWrapper.value ? treeWrapper.value.clientWidth / 2 : 0
      calculateLayout(props.data, startX, 50)
      return nodes
    })
    
    // 绘制连接线
    const drawConnections = () => {
      if (!svgElement.value) return
      
      const svg = svgElement.value
      // 清空现有连接线
      while (svg.firstChild) {
        svg.removeChild(svg.firstChild)
      }
      
      // 设置SVG尺寸
      if (treeWrapper.value) {
        svg.setAttribute('width', treeWrapper.value.clientWidth)
        svg.setAttribute('height', treeWrapper.value.clientHeight)
      }
      
      // 绘制所有父子连接线
      const drawNodeConnections = (node) => {
        if (node.children && node.children.length) {
          const parentPos = nodePositions.value[node.id]
          
          node.children.forEach(child => {
            const childPos = nodePositions.value[child.id]
            
            if (parentPos && childPos) {
              // 创建SVG路径
              const path = document.createElementNS('http://www.w3.org/2000/svg', 'path')
              path.setAttribute('d', `M${parentPos.x + parentPos.width/2},${parentPos.y + parentPos.height} 
                                    L${childPos.x + childPos.width/2},${childPos.y}`)
              path.setAttribute('stroke', '#999')
              path.setAttribute('stroke-width', '1.5')
              path.setAttribute('fill', 'none')
              svg.appendChild(path)
              
              // 递归绘制子节点的连接
              drawNodeConnections(child)
            }
          })
        }
      }
      
      drawNodeConnections(props.data)
    }
    
    // 监听数据变化和窗口大小变化
    onMounted(() => {
      nextTick(() => {
        drawConnections()
      })
    })
    
    watch(flattenedNodes, () => {
      nextTick(() => {
        drawConnections()
      })
    }, { deep: true })
    
    // 修改后的点击事件处理
    const onNodeClick = (node) => {
      selectedNode.value = node
      showMenu.value = true
      console.log('节点点击:', node) // 调试用
    }

    // 显示详细信息
    const showDetail = () => {
      showMenu.value = false
      router.push({
        name: 'teacher',
        params: { name: selectedNode.value.name }
      })
    }

    // 显示添加节点对话框
    const showAddNodeDialog = () => {
      showMenu.value = false
      showAddDialog.value = true
      // 重置表单
      newNodeForm.value = {
        name: '',
        school: selectedNode.value.school || '', // 默认继承父节点的门派
        details: ''
      }
    }

    // 添加新节点
    const addNewNode = async () => {
      try {
        // 准备 FormData
        const formData = new FormData()
        formData.append('name', newNodeForm.value.name)
        formData.append('school', newNodeForm.value.school || '')
        formData.append('details', newNodeForm.value.details || '')
        formData.append('parent_id', selectedNode.value.id)
        
        // 如果有头像文件
        if (newNodeForm.value.avatar) {
          formData.append('avatar', newNodeForm.value.avatar)
        }
        // console.log(newNodeForm)
        console.log('FormData 内容:')
        for (let [key, value] of formData.entries()) {
          console.log(`${key}:`, value)
        }
        // 调用API添加节点
        const response = await api.addNode(formData)
        console.log(response.data)
        

        // 更健壮的判断方式
        if (response.status === 200 || response.status === 201) {
          // 处理成功情况
          // // 更新前端树结构
          if (!selectedNode.value.children) {
            selectedNode.value.children = []
          }
          
          // // 添加新节点到子节点列表
          selectedNode.value.children.push({
            id: response.data.node.id,
            name: response.data.node.name,
            school: response.data.node.school,
            details: response.data.node.details,
            parent_id: response.data.node.parent_id,
            is_root: response.data.node.is_root,
            // 如果有头像可以添加 avatar 字段
            avatar: response.data.node.avatar
          })
          
          // 关闭对话框
          showAddDialog.value = false
          
          // 重置表单
          newNodeForm.value = {
            name: '',
            school: '',
            details: '',
            avatar: null
          }
          
          // 显示成功消息
          ElMessage.success('节点添加成功')
        }
      } catch (error) {
        console.error('添加节点失败:', error)
        
        // 显示错误消息
        if (error.response) {
          // 从后端返回的错误消息
          ElMessage.error(error.response.data.message || '添加节点失败')
        } else {
          ElMessage.error('网络错误，请检查连接')
        }
      }
    }

    // 关闭菜单
    const handleClose = () => {
      showMenu.value = false
    }
    
    return {
      flattenedNodes,
      svgElement,
      treeWrapper,
      onNodeClick,
      showMenu,
      showAddDialog,
      newNodeForm,
      showDetail,
      showAddNodeDialog,
      addNewNode,
      handleClose
    }
  }
}
</script>

<style scoped>
.tree-container {
  font-family: 'Microsoft YaHei', sans-serif;
  width: 100%;
  height: 100vh;
  overflow: hidden;
  position: relative;
}

.tree-title {
  text-align: center;
  color: #333;
  margin: 20px 0;
  position: relative;
}

.tree-title::after {
  content: '';
  position: absolute;
  bottom: -10px;
  left: 50%;
  transform: translateX(-50%);
  width: 100px;
  height: 2px;
  background: linear-gradient(to right, transparent, #4a6fa5, transparent);
}

.tree-wrapper {
  position: relative;
  width: 100%;
  height: calc(100% - 80px);
}

.tree-connections {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1;
}

.tree-nodes {
  position: relative;
  z-index: 2;
  width: 100%;
  height: 100%;
}

.node-menu {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 20px;
}

.node-menu .el-button {
  width: 100%;
  margin-left: 0;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
}
</style>