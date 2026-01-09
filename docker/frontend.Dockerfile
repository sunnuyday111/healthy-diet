# 前端Dockerfile
FROM node:18-alpine

# 设置工作目录
WORKDIR /app

# 复制package文件
COPY frontend/package*.json ./

# 安装依赖
RUN npm install

# 复制应用代码
COPY frontend/ .

# 暴露端口
EXPOSE 5173

# 启动vite开发服务器
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
