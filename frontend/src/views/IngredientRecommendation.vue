<template>
  <div class="ingredient-recommendation">
    <h2>根据现有食材推荐菜谱</h2>
    <el-form :model="form" label-width="120px">
      <el-form-item label="食材列表">
        <el-tag
          v-for="(ingredient, index) in form.ingredients"
          :key="index"
          closable
          @close="removeIngredient(index)"
          style="margin-right: 8px; margin-bottom: 8px;"
        >
          {{ ingredient }}
        </el-tag>
        <el-input
          v-model="newIngredient"
          placeholder="输入食材后按回车添加"
          @keyup.enter="addIngredient"
          style="width: 200px; margin-top: 8px;"
        />
        <el-button @click="addIngredient" style="margin-left: 10px;">添加</el-button>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="recommendRecipes" :loading="loading">
          推荐菜谱
        </el-button>
        <el-button @click="clearIngredients" style="margin-left: 10px;">清空</el-button>
      </el-form-item>
    </el-form>

    <div v-if="recommendations.recipes && recommendations.recipes.length > 0" class="results">
      <h3>推荐菜谱 ({{ recommendations.recipes.length }}个)</h3>
      <el-alert v-if="recommendations.message" :title="recommendations.message" type="info" style="margin-bottom: 20px;" />
      
      <el-card v-for="(recipe, index) in recommendations.recipes" :key="index" style="margin-bottom: 15px;">
        <template #header>
          <div class="card-header">
            <span>{{ recipe.name }}</span>
            <el-tag size="small" :type="getDifficultyType(recipe.difficulty)">
              {{ recipe.difficulty }}
            </el-tag>
          </div>
        </template>
        <p><strong>做法:</strong> {{ recipe.description }}</p>
        <p><strong>热量:</strong> {{ recipe.estimated_calories }} 千卡</p>
        <p><strong>时间:</strong> {{ recipe.cooking_time }} 分钟</p>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { recommendByIngredients } from '@/services/api'

interface Recipe {
  name: string
  description: string
  estimated_calories: number
  cooking_time: number
  difficulty: string
}

interface RecommendationResponse {
  recipes: Recipe[]
  message: string
}

const form = ref({
  ingredients: [] as string[]
})

const newIngredient = ref('')
const loading = ref(false)
const recommendations = ref<RecommendationResponse>({
  recipes: [],
  message: ''
})

const addIngredient = () => {
  if (newIngredient.value.trim() && !form.value.ingredients.includes(newIngredient.value.trim())) {
    form.value.ingredients.push(newIngredient.value.trim())
    newIngredient.value = ''
  }
}

const removeIngredient = (index: number) => {
  form.value.ingredients.splice(index, 1)
}

const clearIngredients = () => {
  form.value.ingredients = []
  recommendations.value = { recipes: [], message: '' }
}

const recommendRecipes = async () => {
  if (form.value.ingredients.length === 0) {
    alert('请至少输入一个食材')
    return
  }
  
  loading.value = true
  try {
    const response = await recommendByIngredients(form.value.ingredients)
    recommendations.value = response.data
  } catch (error) {
    console.error('推荐失败:', error)
    alert('推荐失败，请稍后重试')
  } finally {
    loading.value = false
  }
}

const getDifficultyType = (difficulty: string) => {
  switch (difficulty) {
    case '简单': return 'success'
    case '中等': return 'warning'
    case '困难': return 'danger'
    default: return 'info'
  }
}
</script>

<style scoped>
.ingredient-recommendation {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.results {
  margin-top: 30px;
}
</style>