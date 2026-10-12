import axios from 'axios'

const service = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL
})

// 🔑 请求拦截器
service.interceptors.request.use(
  (config) => {
 

    // 如果有 token，自动添加到请求头
    config.headers['x-token'] = 'abc123456'
  

    // 必须返回 config，否则请求发不出去
    return config
  },
  (error) => {
    // 请求发送失败
    console.error('请求拦截器错误：', error)
    return Promise.reject(error)
  }
)

export default service