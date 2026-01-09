<template>
  <div id="app">
    <el-container>
      <el-header>
        <h1>健康饮食推荐智能体</h1>
      </el-header>
      
      <el-main>
        <el-card class="mode-selector">
          <template #header>
            <div class="card-header">
              <span>请选择模式</span>
            </div>
          </template>
          
          <el-row :gutter="20">
            <el-col :span="12">
              <el-button 
                type="primary" 
                size="large" 
                @click="currentView = 'ingredient'"
                :class="{ active: currentView === 'ingredient' }"
                style="width: 100%; height: 120px; font-size: 18px;"
              >
                <el-icon><Food /></el-icon>
                <div>根据现有食材推荐菜谱</div>
              </el-button>
            </el-col>
            <el-col :span="12">
              <el-button 
                type="success" 
                size="large" 
                @click="currentView = 'diet'"
                :class="{ active: currentView === 'diet' }"
                style="width: 100%; height: 120px; font-size: 18px;"
              >
                <el-icon><Calendar /></el-icon>
                <div>生成个性化一周饮食计划</div>
              </el-button>
            </el-col>
          </el-row>
        </el-card>
        
        <div class="view-container">
          <IngredientRecommendation v-if="currentView === 'ingredient'" />
          <DietPlan v-if="currentView === 'diet'" />
        </div>
      </el-main>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import IngredientRecommendation from './views/IngredientRecommendation.vue'
import DietPlan from './views/DietPlan.vue'
import { Food, Calendar } from '@element-plus/icons-vue'

const currentView = ref<'ingredient' | 'diet'>('ingredient')
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}

.el-header {
  background-color: #409eff;
  color: white;
  text-align: center;
  line-height: 60px;
}

.mode-selector {
  margin-bottom: 30px;
}

.active {
  transform: scale(1.05);
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.3);
}

.view-container {
  min-height: 500px;
}
</style>