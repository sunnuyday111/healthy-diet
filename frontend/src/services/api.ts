import axios from 'axios'

// 创建axios实例
const api = axios.create({
  baseURL: '/api',
  timeout: 3000000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 食材推荐接口
export const recommendByIngredients = (ingredients: string[]) => {
  return api.post('/healthy-diet/recommend-by-ingredients', { ingredients })
}

// 饮食计划接口
export const generateDietPlan = (data: any) => {
  return api.post('/healthy-diet/generate-diet-plan', data)
}

export default api