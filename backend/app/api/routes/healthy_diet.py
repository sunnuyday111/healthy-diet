"""健康饮食推荐API路由"""

from fastapi import APIRouter, HTTPException
from ...models.schemas import (
    IngredientRecommendationRequest,
    IngredientRecommendationResponse,
    DietPlanRequest,
    DietPlanResponse,
    ErrorResponse
)
from ...agents.healthy_diet_agent import get_healthy_diet_agent

router = APIRouter(prefix="/healthy-diet", tags=["健康饮食推荐"])


@router.post(
    "/recommend-by-ingredients",
    response_model=IngredientRecommendationResponse,
    summary="根据现有食材推荐菜谱",
    description="根据用户提供的现有食材列表，推荐3-5个可制作的健康菜谱"
)
async def recommend_by_ingredients(request: IngredientRecommendationRequest):
    """
    根据现有食材推荐菜谱
    
    Args:
        request: 食材列表请求
        
    Returns:
        推荐的菜谱列表
    """
    try:
        agent = get_healthy_diet_agent()
        return agent.recommend_recipes_by_ingredients(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"食材推荐失败: {str(e)}")


@router.post(
    "/generate-diet-plan",
    response_model=DietPlanResponse,
    summary="生成个性化一周饮食计划",
    description="根据用户的个人信息和目标，生成科学的一周饮食计划"
)
async def generate_diet_plan(request: DietPlanRequest):
    """
    生成个性化一周饮食计划
    
    Args:
        request: 饮食计划请求参数
        
    Returns:
        一周饮食计划
    """
    try:
        agent = get_healthy_diet_agent()
        return agent.generate_diet_plan(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"饮食计划生成失败: {str(e)}")