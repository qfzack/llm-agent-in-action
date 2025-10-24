# 快速入门指南

## 5 分钟快速开始

### 步骤 1: 安装 uv

```bash
# Linux/Mac
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 步骤 2: 安装依赖

```bash
# uv 会自动创建虚拟环境并安装所有依赖
uv sync
```

### 步骤 3: 配置环境

```bash
# 复制配置文件
cp .env.example .env

# 编辑 .env 文件，填入你的 OpenAI API Key
# OPENAI_API_KEY=sk-your-api-key-here
```

### 步骤 4: 添加文档

将你的文档（PDF、Word、Markdown 或 TXT 文件）放入 `knowledge_base` 目录：

```bash
knowledge_base/
  ├── your-document1.pdf
  ├── your-document2.docx
  └── your-document3.md
```

### 步骤 5: 加载文档

```bash
uv run python cli.py load
```

### 步骤 6: 开始使用

#### 方式 1: 使用启动脚本（最简单）

```bash
./start.sh        # Linux/Mac
start.bat         # Windows
```

启动脚本会提供菜单，选择你需要的操作。

#### 方式 2: 命令行交互

```bash
uv run python cli.py query
```

然后输入你的问题，AI 会基于你的文档回答。

#### 方式 3: 启动 API 服务

```bash
uv run python main.py
```

访问 http://localhost:8000/docs 查看 API 文档。

#### 方式 4: 使用 Python 客户端

```python
from example_client import AIAgentClient

client = AIAgentClient()
result = client.query("我的问题是什么？")
print(result['answer'])
```

## 使用启动脚本

### Linux/Mac

```bash
./start.sh
```

### Windows

```cmd
start.bat
```

启动脚本提供了一个简单的菜单界面，可以：
1. 加载文档
2. 启动 API 服务
3. 启动命令行交互
4. 查看系统状态
5. 运行测试

## 常用命令

使用 `uv run` 运行命令（无需手动激活虚拟环境）：

```bash
# 查看系统状态
uv run python cli.py status

# 加载文档
uv run python cli.py load

# 单次查询
uv run python cli.py query "你的问题"

# 交互式查询
uv run python cli.py query

# 启动 API 服务
uv run python main.py

# 运行测试（需要先启动 API 服务）
uv run python test_api.py
```

或者使用快捷脚本命令：

```bash
# 使用 pyproject.toml 中定义的脚本
uv run ai-agent status
uv run ai-agent-server
```

## API 使用示例

### 查询

```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "这个系统有什么功能？"}'
```

### 上传文档

```bash
curl -X POST "http://localhost:8000/upload" \
  -F "file=@/path/to/document.pdf"
```

### 重新加载文档

```bash
curl -X POST "http://localhost:8000/reload"
```

### 获取状态

```bash
curl "http://localhost:8000/status"
```

## 故障排查

### 问题：找不到文档

**解决方案**：
- 确保文档放在 `knowledge_base` 目录下
- 运行 `uv run python run.py load` 加载文档
- 检查文档格式是否支持（PDF、DOCX、MD、TXT）

### 问题：API Key 错误

**解决方案**：
- 检查 `.env` 文件中的 `OPENAI_API_KEY` 是否正确
- 确保 API Key 有效且有余额

### 问题：导入模块错误

**解决方案**：
- 使用 `uv run` 运行命令
- 重新同步依赖：`uv sync`

### 问题：服务无法启动

**解决方案**：
- 检查端口 8000 是否被占用
- 可以在 `.env` 文件中修改 `PORT` 参数

## 下一步

- 阅读完整的 [README.md](../README.md) 了解更多功能
- 查看 [uv 使用指南](UV_GUIDE.md) 学习 uv 包管理器
- 查看 [example_client.py](../example_client.py) 学习如何集成到你的应用
- 运行 [test_api.py](../test_api.py) 测试所有功能
- 自定义配置文件以适应你的需求

## 获取帮助

如果遇到问题：
1. 检查日志输出
2. 查看 README.md 中的常见问题部分
3. 确保所有依赖正确安装
4. 验证 API Key 配置正确

祝使用愉快！🚀
