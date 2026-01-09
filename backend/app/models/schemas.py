"""健康饮食推荐数据模型定义"""

from typing import List, Optional, Union
from enum import Enum
from pydantic import BaseModel, Field, field_validator


# ============ 食材推荐模式 ============

class IngredientRecommendationRequest(BaseModel):
    """食材推荐请求"""
    ingredients: List[str] = Field(..., description="现有食材列表", example=["鸡胸肉", "西兰花", "大米", "鸡蛋"])
    
    class Config:
        json_schema_extra = {
            "example": {
                "ingredients": ["鸡胸肉", "西兰花", "大米", "鸡蛋"]
            }
        }


class Recipe(BaseModel):
    """菜谱"""
    name: str = Field(..., description="菜名", example="宫保鸡丁")
    description: str = Field(..., description="简要做法", example="将鸡胸肉切丁，用料酒、淀粉腌制，炒香干辣椒和花椒，加入鸡丁翻炒...")
    estimated_calories: int = Field(..., description="热量估算(千卡)", ge=0, example=350)
    cooking_time: int = Field(..., description="烹饪时间(分钟)", ge=0, example=20)
    difficulty: str = Field(..., description="难度等级", example="简单")


class IngredientRecommendationResponse(BaseModel):
    """食材推荐响应"""
    recipes: List[Recipe] = Field(..., description="推荐的菜谱列表")
    message: str = Field(default="", description="额外信息或建议")


# ============ 饮食计划模式 ============

class ActivityLevel(str, Enum):
    """活动水平枚举"""
    SEDENTARY = "sedentary"
    LIGHT = "light"
    MODERATE = "moderate"
    ACTIVE = "active"


class GoalType(str, Enum):
    """目标类型枚举"""
    WEIGHT_LOSS = "减脂"
    MUSCLE_GAIN = "增肌"
    MAINTENANCE = "维持"


class DietPlanRequest(BaseModel):
    """饮食计划请求"""
    weight: float = Field(..., description="体重(kg)", gt=0, example=70.0)
    height: float = Field(..., description="身高(cm)", gt=0, example=175.0)
    age: int = Field(..., description="年龄", gt=0, lt=120, example=30)
    gender: str = Field(..., description="性别", example="男")
    goal: GoalType = Field(..., description="目标", example="减脂")
    activity_level: Optional[ActivityLevel] = Field(
        default=None, 
        description="活动水平",
        example="moderate"
    )
    daily_steps: Optional[int] = Field(
        default=None,
        description="日均步数",
        ge=0,
        example=8000
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "weight": 70.0,
                "height": 175.0,
                "age": 30,
                "gender": "男",
                "goal": "减脂",
                "activity_level": "moderate",
                "daily_steps": 8000
            }
        }


class MealPlan(BaseModel):
    """一餐计划"""
    type: str = Field(..., description="餐次类型", example="早餐")
    name: str = Field(..., description="餐名", example="燕麦牛奶配水果")
    description: str = Field(..., description="详细描述", example="50g燕麦片+200ml低脂牛奶+1个苹果+10颗杏仁")
    estimated_calories: int = Field(..., description="热量估算(千卡)", ge=0, example=400)


class DailyDietPlan(BaseModel):
    """每日饮食计划"""
    date: str = Field(..., description="日期 YYYY-MM-DD", example="2026-01-09")
    meals: List[MealPlan] = Field(..., description="三餐计划")
    total_calories: int = Field(..., description="总热量(千卡)", ge=0, example=2000)
    protein_ratio: float = Field(..., description="蛋白质比例(%)", ge=0, le=100, example=30.0)
    carb_ratio: float = Field(..., description="碳水化合物比例(%)", ge=0, le=100, example=40.0)
    fat_ratio: float = Field(..., description="脂肪比例(%)", ge=0, le=100, example=30.0)


class DietPlanResponse(BaseModel):
    """饮食计划响应"""
    weekly_plan: List[DailyDietPlan] = Field(..., description="一周饮食计划")
    daily_calorie_target: int = Field(..., description="每日热量目标(千卡)", ge=0, example=2000)
    macro_nutrients: dict = Field(..., description="宏量营养素建议", example={"protein": "150g", "carbs": "200g", "fat": "67g"})
    recommendations: str = Field(..., description="个性化建议", example="建议多喝水，保持充足睡眠，配合适量运动...")


# ============ 通用响应 ============

class ErrorResponse(BaseModel):
    """错误响应"""
    detail: str = Field(..., description="错误详情")