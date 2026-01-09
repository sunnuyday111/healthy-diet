# 健康饮食推荐 Agent

这是一个基于 `hello_agents` 库的健康饮食推荐系统，支持两种模式：

1. **食材推荐模式**：根据用户现有的食材推荐可制作的菜谱
2. **饮食计划模式**：根据用户的个人信息生成个性化的一周饮食计划

## 项目结构

```
helloagents-healthy-diet/
├── backend/          # 后端服务
│   ├── app/          # FastAPI 应用
│   │   ├── agents/   # Agent 实现
│   │   ├── api/      # API 路由
│   │   ├── models/   # 数据模型
│   │   ├── services/ # 服务层
│   │   └── config.py # 配置文件
│   ├── requirements.txt
│   └── run.py        # 启动脚本
└── frontend/         # 前端界面
    ├── src/          # Vue 3 源码
    ├── package.json
    └── vite.config.ts
```

## 快速开始

### 后端启动

```bash
cd backend
pip install -r requirements.txt
python run.py
```

后端服务将运行在 `http://127.0.0.1:8000`

### 前端启动

```bash
cd frontend
npm install
npm run dev
```

前端服务将运行在 `http://localhost:3000`

## API 接口

### 食材推荐

- **POST** `/healthy-diet/recommend-by-ingredients`
- **请求体**: `{ "ingredients": ["鸡胸肉", "西兰花", "大米"] }`
- **响应**: 推荐的菜谱列表

### 饮食计划

- **POST** `/healthy-diet/generate-diet-plan`
- **请求体**: 
  ```json
  {
    "weight": 70,
    "height": 175,
    "age": 30,
    "gender": "男",
    "goal": "减脂",
    "activity_level": "moderate"
  }
  ```
- **响应**: 一周饮食计划

## 技术栈

- **后端**: Python 3.10+, FastAPI, hello_agents
- **前端**: Vue 3, TypeScript, Element Plus
- **部署**: 前后端分离架构

## 功能特点

- ✅ 基于现有食材智能推荐菜谱
- ✅ 个性化一周饮食计划生成
- ✅ 科学的热量和营养素计算
- ✅ 响应式Web界面
- ✅ 完整的错误处理和备用方案