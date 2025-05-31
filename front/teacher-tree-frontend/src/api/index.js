import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:5000',
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器（添加 JWT）
api.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers['x-access-token'] = token
  }
  return config
})

export default {
  // 认证相关
  async register(user) {
    return api.post('/register', user)
  },
  async login(credentials) {
    return api.post('/login', {}, {
      auth: credentials
    })
  },

  // 数据相关
  async getTree() {
    return api.get('/tree')
  },
  async getTeacher(name) {
    return api.get(`/teachers/${name}`)
  },
  // async addNode(nodeData) {
  //   const formData = new FormData()
  //   for (const key in nodeData) {
  //     if (nodeData[key] !== undefined) {
  //       formData.append(key, nodeData[key])
  //     }
  //   }
  //   return api.post('/nodes', formData)
  // }
  // async addNode(nodeData) {
  //   return api.post('/nodes', nodeData) // 直接发送 JSON
  // }
  async addNode(nodeData) {
    const formData = new FormData()
    // formData.append('name', nodeData.name)
    // formData.append('school', nodeData.school || '')
    // formData.append('details', nodeData.details || '')
    // formData.append('parent_id', nodeData.parentId)
    
    console.log('FormData 内容:')
    for (let [key, value] of nodeData.entries()) {
      console.log(`${key}:`, value)
      formData.append(key, value)
    }
    // if (nodeData.avatar) {
    //   formData.append('avatar', nodeData.avatar)
    // }
    
    return api.post('/nodes', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  }
}