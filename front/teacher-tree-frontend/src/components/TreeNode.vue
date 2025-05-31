<template>
  <div 
    class="tree-node"
    :class="{ 'has-children': hasChildren }"
    @click="$emit('node-click', node)"
  >
    <div class="node-content">
      <div class="node-name">{{ node.name }}</div>
      <div class="node-school">{{ node.school }}</div>
    </div>
  </div>
</template>

<script>
import { computed } from 'vue'

export default {
  name: 'TreeNode',
  props: {
    node: {
      type: Object,
      required: true
    }
  },
  emits: ['node-click'],
  setup(props) {
    const hasChildren = computed(() => {
      return props.node.children && props.node.children.length > 0
    })
    
    return {
      hasChildren
    }
  }
}
</script>

<style scoped>
.tree-node {
  position: absolute;
  width: 120px;
  height: 60px;
  background-color: white;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
  cursor: pointer;
  transition: all 0.2s;
  transform: translate(-50%, 0);
  z-index: 10;
}

.tree-node:hover {
  box-shadow: 0 2px 10px rgba(0,0,0,0.2);
  transform: translate(-50%, -2px);
}

.node-content {
  padding: 8px;
  text-align: center;
}

.node-name {
  font-weight: bold;
  color: #2c3e50;
  margin-bottom: 4px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.node-school {
  font-size: 0.8em;
  color: #7f8c8d;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.has-children .node-name {
  color: #4a6fa5;
}
</style>