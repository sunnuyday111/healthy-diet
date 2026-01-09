<template>
  <div class="diet-plan">
    <h2>生成个性化一周饮食计划</h2>
    <el-form :model="form" label-width="150px" :rules="rules" ref="dietPlanForm">
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="体重 (kg)" prop="weight">
            <el-input v-model.number="form.weight" type="number" />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="身高 (cm)" prop="height">
            <el-input v-model.number="form.height" type="number" />
          </el-form-item>
        </el-col>
      </el-row>
      
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="年龄" prop="age">
            <el-input v-model.number="form.age" type="number" />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="性别" prop="gender">
            <el-select v-model="form.gender" placeholder="请选择性别">
              <el-option label="男" value="男" />
              <el-option label="女" value="女" />
            </el-select>
          </el-form-item>
        </el-col>
      </el-row>
      
      <el-form-item label="目标" prop="goal">
        <el-radio-group v-model="form.goal">
          <el-radio label="减脂">减脂</el-radio>
          <el-radio label="增肌">增肌</el-radio>
          <el-radio label="维持">维持</el-radio>
        </el-radio-group>
      </el-form-item>
      
      <el-form-item label="活动水平" prop="activity_level">
        <el-radio-group v-model="form.activity_level">
          <el-radio value="sedentary">久坐 (很少运动)</el-radio>
          <el-radio value="light">轻度活动 (每周1-3天运动)</el-radio>
          <el-radio value="moderate">中度活动 (每周3-5天运动)</el-radio>
          <el-radio value="active">重度活动 (每周6-7天运动)</el-radio>
        </el-radio-group>
      </el-form-item>
      
      <el-form-item label="日均步数 (可选)">
        <el-input v-model.number="form.daily_steps" type="number" placeholder="如果知道日均步数可以填写" />
      </el-form-item>
      
      <el-form-item>
        <el-button type="primary" @click="generatePlan" :loading="loading">
          生成饮食计划
        </el-button>
        <el-button @click="resetForm" style="margin-left: 10px;">重置</el-button>
      </el-form-item>
    </el-form>

    <div v-if="dietPlan.weekly_plan && dietPlan.weekly_plan.length > 0" class="results">
      <h3>一周饮食计划</h3>
      <el-alert :title="`每日热量目标: ${dietPlan.daily_calorie_target} 千卡`" type="success" style="margin-bottom: 20px;" />
      <el-alert :title="dietPlan.recommendations" type="info" style="margin-bottom: 20px;" />
      
      <el-tabs type="card">
        <el-tab-pane 
          v-for="(day, index) in dietPlan.weekly_plan" 
          :key="index" 
          :label="`第${index + 1}天 (${day.date})`"
        >
          <el-card>
            <p><strong>总热量:</strong> {{ day.total_calories }} 千卡</p>
            <p><strong>营养比例:</strong> 蛋白质 {{ day.protein_ratio }}% | 碳水 {{ day.carb_ratio }}% | 脂肪 {{ day.fat_ratio }}%</p>
            
            <el-divider />
            
            <div v-for="meal in day.meals" :key="meal.type">
              <h4>{{ meal.type }}</h4>
              <p><strong>{{ meal.name }}</strong></p>
              <p>{{ meal.description }}</p>
              <p><em>热量: {{ meal.estimated_calories }} 千卡</em></p>
              <el-divider />
            </div>
          </el-card>
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { generateDietPlan } from '@/services/api'
import type { FormInstance } from 'element-plus'

interface DietPlanResponse {
  weekly_plan: any[]
  daily_calorie_target: number
  macro_nutrients: any
  recommendations: string
}

const dietPlanForm = ref<FormInstance>()
const form = reactive({
  weight: 70,
  height: 175,
  age: 30,
  gender: '男',
  goal: '减脂',
  activity_level: 'moderate',
  daily_steps: null as number | null
})

const rules = {
  weight: [{ required: true, message: '请输入体重', trigger: 'blur' }],
  height: [{ required: true, message: '请输入身高', trigger: 'blur' }],
  age: [{ required: true, message: '请输入年龄', trigger: 'blur' }],
  gender: [{ required: true, message: '请选择性别', trigger: 'change' }],
  goal: [{ required: true, message: '请选择目标', trigger: 'change' }],
  activity_level: [{ required: true, message: '请选择活动水平', trigger: 'change' }]
}

const loading = ref(false)
const dietPlan = ref<DietPlanResponse>({
  weekly_plan: [],
  daily_calorie_target: 0,
  macro_nutrients: {},
  recommendations: ''
})

const generatePlan = async () => {
  if (!dietPlanForm.value) return
  
  dietPlanForm.value.validate(async (valid) => {
    if (valid) {
      loading.value = true
      try {
        const requestData = { ...form }
        if (requestData.daily_steps === null) {
          delete requestData.daily_steps
        }
        
        const response = await generateDietPlan(requestData)
        dietPlan.value = response.data
      } catch (error) {
        console.error('生成计划失败:', error)
        alert('生成计划失败，请稍后重试')
      } finally {
        loading.value = false
      }
    }
  })
}

const resetForm = () => {
  if (dietPlanForm.value) {
    dietPlanForm.value.resetFields()
  }
  dietPlan.value = {
    weekly_plan: [],
    daily_calorie_target: 0,
    macro_nutrients: {},
    recommendations: ''
  }
}
</script>

<style scoped>
.diet-plan {
  padding: 20px;
}

.results {
  margin-top: 30px;
}
</style>