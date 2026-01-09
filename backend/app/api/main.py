"""主API应用"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import healthy_diet
from ..config import get_settings, validate_config, print_config

# 获取配置
settings = get_settings()

# 创建FastAPI应用
app = FastAPI(
    title="健康饮食推荐Agent API",
    description="基于AI的健康饮食推荐服务",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该限制为具体的前端域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(healthy_diet.router)

@app.get("/")
async def root():
    """根路径"""
    return {"message": "健康饮食推荐Agent API", "version": "1.0.0"}


@app.on_event("startup")
async def startup_event():
    """应用启动事件"""
    print("\n" + "="*60)
    print(f"🚀 {settings.app_name} v{settings.app_version}")
    print("="*60)
    
    # 打印配置信息
    print_config()
    
    # 验证配置
    try:
        validate_config()
        print("\n✅ 配置验证通过")
    except ValueError as e:
        print(f"\n❌ 配置验证失败:\n{e}")
        print("\n请检查.env文件并确保所有必要的配置项都已设置")
        raise
    
    print("\n")


@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭事件"""
    print("\n" + "="*60)
    print("👋 应用正在关闭...")
    print("="*60 + "\n")
