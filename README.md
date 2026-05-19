# AgentCraft

**对标 CodeX 的本地 AI Agent 伴侣** — 项目级代码生成、PPT 制作、长程任务编排、定时调度，Everything You Need。

## 功能演示

### 论文结论生成

只需提供文章 URL，自动提取内容并生成结论摘要。

![论文结论生成](docs/demo.gif)

### PPT 自动生成

一句话指令，自动生成完整 PPT 演示文稿。

![PPT 生成](docs/ppt生成.gif)

## 快速启动

```bash
# 1. 安装依赖 (自动创建 .venv)
uv sync

# 2. 配置环境变量
cp ".env copy" .env
# 编辑 .env 填入你的 API Key

# 3. 启动服务
uv run python run_app.py
```

服务将在 http://127.0.0.1:8000/canvas 启动。

## 环境变量

| 变量 | 说明 |
|------|------|
| `LLM_API_KEY` | LLM API 密钥 |
| `DEEPSEEK_API_KEY` | DeepSeek API 密钥 |
| `MLFLOW_TRACKING_URI` | MLflow 追踪地址 (默认 http://127.0.0.1:5050) |