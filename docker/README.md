# Docker 部署指南

## 文件说明

- `backend.Dockerfile` - 后端服务的Docker镜像构建文件
- `frontend.Dockerfile` - 前端服务的Docker镜像构建文件（多阶段构建）
- `docker-compose.yml` - Docker Compose编排文件
- `nginx.conf` - 前端Nginx配置文件
- `.env.example` - 环境变量配置示例
- `.dockerignore` - Docker构建忽略文件

## 快速开始

### 1. 配置环境变量

```bash
# 复制环境变量示例文件
cp .env.example .env

# 编辑.env文件，填入实际的配置值
# 特别是OPENAI_API_KEY
```

### 2. 构建并启动服务

```bash
# 在docker目录下执行
cd docker

# 构建并启动所有服务
docker-compose up -d --build

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

### 3. 访问应用

- 前端页面: http://localhost
- 后端API: http://localhost:8000
- API文档: http://localhost:8000/docs

### 4. 停止服务

```bash
# 停止所有服务
docker-compose down

# 停止并删除卷
docker-compose down -v
```

## 开发模式

如果需要在开发模式下运行（代码热重载）：

1. 在 `docker-compose.yml` 中确保后端服务已挂载了代码卷：
   ```yaml
   volumes:
     - ../backend:/app
   ```

2. 修改后端启动命令以启用热重载：
   ```yaml
   command: uvicorn app.api.main:app --host 0.0.0.0 --port 8000 --reload
   ```

## 生产部署建议

1. **环境变量安全**
   - 不要将 `.env` 文件提交到版本控制
   - 使用密钥管理服务（如 AWS Secrets Manager、Azure Key Vault）

2. **CORS配置**
   - 在 `docker-compose.yml` 中限制 `CORS_ORIGINS` 为实际的前端域名

3. **资源限制**
   ```yaml
   services:
     backend:
       deploy:
         resources:
           limits:
             cpus: '1'
             memory: 1G
   ```

4. **日志管理**
   ```yaml
   logging:
     driver: "json-file"
     options:
       max-size: "10m"
       max-file: "3"
   ```

5. **健康检查**
   - 已配置健康检查端点，确保后端实现 `/health` 路由

6. **HTTPS配置**
   - 使用反向代理（如 Nginx、Traefik）配置 SSL 证书
   - 推荐使用 Let's Encrypt 免费证书

## 故障排查

### 查看容器日志
```bash
# 查看后端日志
docker-compose logs -f backend

# 查看前端日志
docker-compose logs -f frontend
```

### 进入容器调试
```bash
# 进入后端容器
docker-compose exec backend /bin/bash

# 进入前端容器
docker-compose exec frontend /bin/sh
```

### 重建服务
```bash
# 重建特定服务
docker-compose up -d --build backend

# 重建所有服务
docker-compose up -d --build --force-recreate
```

## 网络配置

服务通过 `healthy-diet-network` 桥接网络相互通信。服务间可以通过服务名称互相访问：
- 后端服务名: `backend`
- 前端服务名: `frontend`

## 端口映射

- 前端: 主机 `80` → 容器 `80`
- 后端: 主机 `8000` → 容器 `8000`

如需修改端口，编辑 `docker-compose.yml` 中的 `ports` 配置。
