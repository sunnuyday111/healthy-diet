"""健康饮食推荐Agent"""

import json
from typing import Dict, Any, List, Optional
from hello_agents import SimpleAgent
from ..services.llm_service import get_llm
from ..models.schemas import (
    IngredientRecommendationRequest,
    DietPlanRequest,
    Recipe,
    MealPlan,
    DailyDietPlan,
    IngredientRecommendationResponse,
    DietPlanResponse
)
from ..config import get_settings


# ============ Agent提示词 ============

INGREDIENT_RECOMMENDATION_PROMPT = """你是一位专业的营养师和厨师，擅长根据现有食材推荐健康美味的菜谱。

**任务要求:**
1. 根据用户提供的食材列表，推荐3-5个可以制作的菜谱
2. 每个菜谱必须包含：
   - 菜名（中文）
   - 详细的做法描述，给出步骤和主要调料
   - 热量估算（千卡，整数）
   - 烹饪时间（分钟，整数）
   - 难度等级（简单/中等/困难）

**输出格式:**
请严格按照以下JSON格式返回结果：
```json
{
  "recipes": [
    {
      "name": "菜名",
      "description": "详细的做法描述",
      "estimated_calories": 350,
      "cooking_time": 20,
      "difficulty": "简单"
    }
  ],
  "message": "额外建议或说明"
}
```

**注意事项:**
1. 只使用用户提供的食材，不要添加太多额外食材
2. 菜谱要实用、健康、符合中式烹饪习惯
3. 热量估算要合理（主食类300-600千卡，肉类200-400千卡，蔬菜类100-200千卡）
4. 如果食材太少无法做完整菜谱，也要给出创意建议
"""


DIET_PLAN_PROMPT = """你是一位专业的营养师，擅长制定个性化的健康饮食计划。

**任务要求:**
根据用户的个人信息（体重、身高、年龄、性别、目标、活动水平），生成一份科学的一周饮食计划。

**计算基础代谢率(BMR)和每日热量需求:**
- 男性BMR = 88.362 + (13.397 × 体重kg) + (4.799 × 身高cm) - (5.677 × 年龄)
- 女性BMR = 447.593 + (9.247 × 体重kg) + (3.098 × 身高cm) - (4.330 × 年龄)
- 每日热量需求 = BMR × 活动系数
  - sedentary (久坐): 1.2
  - light (轻度活动): 1.375  
  - moderate (中度活动): 1.55
  - active (重度活动): 1.725

**目标调整:**
- 减脂: 每日热量 = 目标热量 - 500千卡
- 增肌: 每日热量 = 目标热量 + 300千卡  
- 维持: 每日热量 = 目标热量

**宏量营养素分配:**
- 减脂: 蛋白质30%, 碳水40%, 脂肪30%
- 增肌: 蛋白质35%, 碳水45%, 脂肪20%  
- 维持: 蛋白质25%, 碳水50%, 脂肪25%

**输出格式:**
请严格按照以下JSON格式返回结果：
```json
{
  "weekly_plan": [
    {
      "date": "2026-01-09",
      "meals": [
        {
          "type": "早餐",
          "name": "餐名",
          "description": "详细描述",
          "estimated_calories": 400
        }
      ],
      "total_calories": 2000,
      "protein_ratio": 30.0,
      "carb_ratio": 40.0,
      "fat_ratio": 30.0
    }
  ],
  "daily_calorie_target": 2000,
  "macro_nutrients": {
    "protein": "150g",
    "carbs": "200g", 
    "fat": "67g"
  },
  "recommendations": "个性化建议"
}
```

**注意事项:**
1. 每日三餐都要包含，可以适当添加加餐
2. 餐食要多样化、营养均衡、符合中式饮食习惯
3. 考虑用户的实际可操作性
4. 提供实用的健康建议
"""


class HealthyDietAgent:
    """健康饮食推荐Agent"""

    def __init__(self):
        """初始化健康饮食Agent"""
        print("🔄 开始初始化健康饮食推荐Agent...")
        
        try:
            settings = get_settings()
            self.llm = get_llm()
            
            # 创建食材推荐Agent
            print("  - 创建食材推荐Agent...")
            self.ingredient_agent = SimpleAgent(
                name="食材推荐专家",
                llm=self.llm,
                system_prompt=INGREDIENT_RECOMMENDATION_PROMPT
            )
            
            # 创建饮食计划Agent
            print("  - 创建饮食计划Agent...")
            self.diet_plan_agent = SimpleAgent(
                name="饮食计划专家", 
                llm=self.llm,
                system_prompt=DIET_PLAN_PROMPT
            )
            
            print("✅ 健康饮食推荐Agent初始化成功")
            
        except Exception as e:
            print(f"❌ 健康饮食推荐Agent初始化失败: {str(e)}")
            import traceback
            traceback.print_exc()
            raise
    
    def recommend_recipes_by_ingredients(self, request: IngredientRecommendationRequest) -> IngredientRecommendationResponse:
        """
        根据现有食材推荐菜谱
        
        Args:
            request: 食材推荐请求
            
        Returns:
            食材推荐响应
        """
        try:
            print(f"\n{'='*60}")
            print(f"🍳 开始食材推荐...")
            print(f"现有食材: {', '.join(request.ingredients)}")
            print(f"{'='*60}\n")
            
            # 构建查询
            query = f"我有以下食材：{', '.join(request.ingredients)}。请根据这些食材推荐3-5个可以制作的健康菜谱。"
            
            # 获取推荐
            response = self.ingredient_agent.run(query, extra_body={"chat_template_kwargs": {"enable_thinking": False}})
            print(f"食材推荐结果: {response[:300]}...\n")
            
            # 解析响应
            recommendation = self._parse_ingredient_response(response)
            
            print(f"✅ 食材推荐完成!")
            return recommendation
            
        except Exception as e:
            print(f"❌ 食材推荐失败: {str(e)}")
            import traceback
            traceback.print_exc()
            # 返回默认响应
            return IngredientRecommendationResponse(
                recipes=[
                    Recipe(
                        name=f"简易{ingredient}料理",
                        description=f"使用{ingredient}制作的简单健康料理",
                        estimated_calories=300,
                        cooking_time=15,
                        difficulty="简单"
                    )
                    for ingredient in request.ingredients[:3]
                ],
                message="抱歉，推荐服务暂时不可用，以下是基于您食材的简单建议。"
            )
    
    def generate_diet_plan(self, request: DietPlanRequest) -> DietPlanResponse:
        """
        生成个性化一周饮食计划
        
        Args:
            request: 饮食计划请求
            
        Returns:
            饮食计划响应
        """
        try:
            print(f"\n{'='*60}")
            print(f"🥗 开始生成饮食计划...")
            print(f"用户信息: {request.weight}kg, {request.height}cm, {request.age}岁, {request.gender}")
            print(f"目标: {request.goal}, 活动水平: {request.activity_level or '未指定'}")
            print(f"{'='*60}\n")
            
            # 构建查询
            activity_info = ""
            if request.daily_steps is not None:
                activity_info += f"日均步数: {request.daily_steps}步"
            elif request.activity_level:
                activity_info += f"活动水平: {request.activity_level}"
            else:
                activity_info = "活动水平: moderate (默认)"
            
            query = f"""请为以下用户生成一周饮食计划：
- 体重: {request.weight}kg
- 身高: {request.height}cm  
- 年龄: {request.age}岁
- 性别: {request.gender}
- 目标: {request.goal}
- {activity_info}

请严格按照要求的JSON格式返回完整的饮食计划。"""
            
            # 获取饮食计划
            response = self.diet_plan_agent.run(query, extra_body={"chat_template_kwargs": {"enable_thinking": False}})
            print(f"饮食计划结果: {response[:300]}...\n")
            
            # 解析响应
            diet_plan = self._parse_diet_plan_response(response)
            
            print(f"✅ 饮食计划生成完成!")
            return diet_plan
            
        except Exception as e:
            print(f"❌ 饮食计划生成失败: {str(e)}")
            import traceback
            traceback.print_exc()
            # 返回默认响应
            from datetime import datetime, timedelta
            today = datetime.now()
            
            daily_plan = DailyDietPlan(
                date=today.strftime("%Y-%m-%d"),
                meals=[
                    MealPlan(type="早餐", name="燕麦牛奶", description="50g燕麦+200ml牛奶", estimated_calories=300),
                    MealPlan(type="午餐", name="鸡胸肉沙拉", description="150g鸡胸肉+混合蔬菜", estimated_calories=400),
                    MealPlan(type="晚餐", name="清蒸鱼", description="200g清蒸鱼+蔬菜", estimated_calories=350)
                ],
                total_calories=1050,
                protein_ratio=30.0,
                carb_ratio=40.0,
                fat_ratio=30.0
            )
            
            return DietPlanResponse(
                weekly_plan=[daily_plan] * 7,
                daily_calorie_target=1050,
                macro_nutrients={"protein": "80g", "carbs": "105g", "fat": "35g"},
                recommendations="抱歉，饮食计划服务暂时不可用。建议咨询专业营养师获取个性化建议。"
            )
    
    def _parse_ingredient_response(self, response: str) -> IngredientRecommendationResponse:
        """解析食材推荐响应"""
        try:
            # 尝试从响应中提取JSON
            if "```json" in response:
                json_start = response.find("```json") + 7
                json_end = response.find("```", json_start)
                json_str = response[json_start:json_end].strip()
            elif "```" in response:
                json_start = response.find("```") + 3
                json_end = response.find("```", json_start)
                json_str = response[json_start:json_end].strip()
            elif "{" in response and "}" in response:
                json_start = response.find("{")
                json_end = response.rfind("}") + 1
                json_str = response[json_start:json_end]
            else:
                raise ValueError("响应中未找到JSON数据")
            
            data = json.loads(json_str)
            return IngredientRecommendationResponse(**data)
            
        except Exception as e:
            print(f"⚠️  解析食材推荐响应失败: {str(e)}")
            # 返回简化版本
            return IngredientRecommendationResponse(
                recipes=[
                    Recipe(
                        name="通用健康菜谱",
                        description="基于您提供的食材制作的健康料理",
                        estimated_calories=350,
                        cooking_time=20,
                        difficulty="简单"
                    )
                ],
                message="解析响应时遇到问题，提供简化建议。"
            )
    
    def _parse_diet_plan_response(self, response: str) -> DietPlanResponse:
        """解析饮食计划响应"""
        try:
            # 尝试从响应中提取JSON
            if "```json" in response:
                json_start = response.find("```json") + 7
                json_end = response.find("```", json_start)
                json_str = response[json_start:json_end].strip()
            elif "```" in response:
                json_start = response.find("```") + 3
                json_end = response.find("```", json_start)
                json_str = response[json_start:json_end].strip()
            elif "{" in response and "}" in response:
                json_start = response.find("{")
                json_end = response.rfind("}") + 1
                json_str = response[json_start:json_end]
            else:
                raise ValueError("响应中未找到JSON数据")
            
            data = json.loads(json_str)
            return DietPlanResponse(**data)
            
        except Exception as e:
            print(f"⚠️  解析饮食计划响应失败: {str(e)}")
            # 返回简化版本
            from datetime import datetime, timedelta
            today = datetime.now()
            
            daily_plan = DailyDietPlan(
                date=today.strftime("%Y-%m-%d"),
                meals=[
                    MealPlan(type="早餐", name="健康早餐", description="均衡营养早餐", estimated_calories=400),
                    MealPlan(type="午餐", name="健康午餐", description="均衡营养午餐", estimated_calories=600),
                    MealPlan(type="晚餐", name="健康晚餐", description="均衡营养晚餐", estimated_calories=500)
                ],
                total_calories=1500,
                protein_ratio=25.0,
                carb_ratio=50.0,
                fat_ratio=25.0
            )
            
            return DietPlanResponse(
                weekly_plan=[daily_plan] * 7,
                daily_calorie_target=1500,
                macro_nutrients={"protein": "94g", "carbs": "188g", "fat": "42g"},
                recommendations="解析响应时遇到问题，提供简化建议。"
            )


# 全局健康饮食Agent实例
_healthy_diet_agent = None


def get_healthy_diet_agent() -> HealthyDietAgent:
    """获取健康饮食推荐Agent实例(单例模式)"""
    global _healthy_diet_agent

    if _healthy_diet_agent is None:
        _healthy_diet_agent = HealthyDietAgent()

    return _healthy_diet_agent