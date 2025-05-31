<template>
  <div class="layout">
    <!-- 左侧导航栏 -->
    <div class="sidebar">
      <div class="logo">LOGO</div>

      <div class="search-box">
        <input v-model="searchQuery" placeholder="搜索..." />
      </div>

      <nav class="nav-menu">
        <router-link
          v-for="item in navItems"
          :key="item.key"
          :to="item.path"
          class="nav-item"
          active-class="active"
        >
          {{ item.label }}
        </router-link>
      </nav>
    </div>

    <!-- 右侧主内容 -->
    <div class="main-content">
      <div class="top-bar">
        <router-link to="/login" class="login-btn">登录</router-link>
      </div>
      <div class="content-area">
        <router-view />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

// 搜索关键词（可拓展）
const searchQuery = ref('')

// 导航项配置，对应你的 router/index.js 中的路由
const navItems = [
  { key: 'home', label: '师承树', path: '/' },
  { key: 'detail', label: '详细信息', path: '/teacher/示例教师名' }
]
</script>

<style scoped>
.layout {
  display: flex;
  height: 100vh;
  font-family: Arial, sans-serif;
}

.sidebar {
  width: 220px;
  background-color: #2c3e50;
  color: white;
  display: flex;
  flex-direction: column;
  padding: 20px 0;
}

.logo {
  font-size: 24px;
  font-weight: bold;
  padding: 0 20px 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  margin-bottom: 10px;
}

.search-box {
  padding: 0 20px 20px;
}

.search-box input {
  width: 100%;
  padding: 6px 10px;
  border-radius: 4px;
  border: none;
}

.nav-menu {
  display: flex;
  flex-direction: column;
  padding: 0 10px;
}

.nav-item {
  padding: 12px 20px;
  color: white;
  text-decoration: none;
  border-radius: 4px;
}

.nav-item:hover {
  background-color: #34495e;
}

.nav-item.active {
  background-color: #42b983;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  background-color: #f5f5f5;
}

.top-bar {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  padding: 10px 20px;
  background-color: white;
  border-bottom: 1px solid #ddd;
}

.login-btn {
  background-color: #42b983;
  color: white;
  border: none;
  padding: 6px 12px;
  border-radius: 4px;
  cursor: pointer;
  text-decoration: none;
}

.content-area {
  padding: 20px;
  flex: 1;
}
</style>
