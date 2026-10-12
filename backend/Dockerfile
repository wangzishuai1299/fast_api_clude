```dockerfile
# 使用 Python 3.11 作为基础镜像
FROM python:3.11-slim

# 设置容器内的工作目录
WORKDIR /app

# 复制依赖清单
COPY requirements.txt .

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制后端代码
COPY app8/ ./app8/
COPY main8.py .

# 暴露后端端口
EXPOSE 8002

# 启动 FastAPI
CMD ["uvicorn", "main8:app", "--host", "0.0.0.0", "--port", "8002"]
```
