# AI Agent 知识库问答系统

基于 RAG (Retrieval-Augmented Generation) 的 AI 知识库问答系统，可以将您的文档知识库通过 AI 提供给用户使用。

## 功能特点

- 📚 **多格式支持**: 支持 PDF、Word、Markdown、TXT 等多种文档格式
- 🔍 **智能检索**: 使用向量数据库实现语义搜索
- 🤖 **AI 对话**: 基于 OpenAI GPT 模型的智能问答
- 🚀 **RESTful API**: 提供完整的 HTTP API 接口
- 💻 **命令行工具**: 支持命令行交互式问答
- 🔄 **实时更新**: 支持动态上传和重新加载文档

## 技术架构

- **Web 框架**: FastAPI
- **LLM**: OpenAI GPT
- **向量数据库**: ChromaDB
- **嵌入模型**: sentence-transformers (all-MiniLM-L6-v2)
- **文档处理**: pypdf, python-docx, markdown

## 📚 文档导航

- **[快速入门指南](docs/QUICKSTART.md)** - 5分钟快速上手
- **[架构说明](docs/ARCHITECTURE.md)** - 项目架构和设计原则
- **[uv 使用指南](docs/UV_GUIDE.md)** - uv 包管理器详细说明
- **[uv 迁移说明](docs/UV_MIGRATION.md)** - 从 pip 迁移到 uv
- **[项目总结](docs/PROJECT_SUMMARY.md)** - 项目功能概览

## 快速开始

### 1. 安装 uv（如果还没有）

```bash
# Linux/Mac
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. 安装依赖

```bash
# uv 会自动创建虚拟环境并安装所有依赖
uv sync
```

### 3. 配置环境变量

复制 `.env.example` 为 `.env` 并配置：

```bash
cp .env.example .env
```

编辑 `.env` 文件，填入您的 OpenAI API Key：

```env
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_API_BASE=https://api.openai.com/v1
MODEL_NAME=gpt-3.5-turbo
```

### 4. 准备文档

将您的文档放入 `knowledge_base` 目录（会自动创建）：

```bash
knowledge_base/
  ├── document1.pdf
  ├── document2.docx
  ├── document3.md
  └── document4.txt
```

### 5. 加载文档

```bash
uv run python run.py load
```

### 6. 启动服务

#### 方式一：使用启动脚本（推荐）

```bash
./scripts/start.sh        # Linux/Mac
scripts\start.bat         # Windows
```

#### 方式二：API 服务

```bash
uv run python server.py
```

服务将在 `http://localhost:8000` 启动

访问 API 文档：`http://localhost:8000/docs`

#### 方式三：命令行交互

```bash
# 交互式问答
uv run python run.py query

# 单次查询
uv run python run.py query "你的问题"

# 查看状态
uv run python run.py status
```

## 使用 uv 的优势

- **快速**: uv 比 pip 快 10-100 倍
- **可靠**: 使用 lock 文件确保依赖一致性
- **简单**: 自动管理虚拟环境，无需手动激活
- **现代**: 支持最新的 Python 打包标准

## 运行命令

使用 `uv run` 前缀运行 Python 命令，无需手动激活虚拟环境：

```bash
# 加载文档
uv run python run.py load

# 启动服务
uv run python server.py

# 交互式查询
uv run python run.py query

# 运行测试
uv run python tests/test_api.py
```

或者使用启动脚本：

```bash
# 使用启动脚本（推荐）
./scripts/start.sh        # Linux/Mac
scripts\start.bat         # Windows
```

## API 使用示例

### 1. 查询知识库

```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "这是什么项目？"}'
```

### 2. 上传文档

```bash
curl -X POST "http://localhost:8000/upload" \
  -F "file=@/path/to/document.pdf"
```

### 3. 重新加载所有文档

```bash
curl -X POST "http://localhost:8000/reload"
```

### 4. 获取系统状态

```bash
curl "http://localhost:8000/status"
```

### 5. 清空知识库

```bash
curl -X DELETE "http://localhost:8000/clear"
```

## Python 客户端示例

```python
import requests

# 查询
response = requests.post(
    "http://localhost:8000/query",
    json={
        "query": "这个系统有什么功能？",
        "conversation_history": [
            {"role": "user", "content": "你好"},
            {"role": "assistant", "content": "你好！有什么可以帮助你的？"}
        ]
    }
)

result = response.json()
print(f"回答: {result['answer']}")
print(f"相关文档数: {len(result['retrieved_docs'])}")
```

## 项目结构

```
agent_demo/
├── src/                    # 源代码目录
│   ├── core/              # 核心功能模块
│   │   ├── config.py      # 配置管理
│   │   └── agent.py       # AI Agent 核心
│   ├── services/          # 服务层
│   │   ├── vector_store.py
│   │   └── document_loader.py
│   ├── api/               # API 接口
│   │   └── main.py        # FastAPI 应用
│   └── cli/               # 命令行工具
│       └── cli.py
├── tests/                 # 测试目录
│   └── test_api.py
├── scripts/               # 脚本工具
│   ├── start.sh           # Linux/Mac 启动脚本
│   ├── start.bat          # Windows 启动脚本
│   └── example_client.py  # Python 客户端示例
├── docs/                  # 📚 文档目录
│   ├── README.md          # 文档导航
│   ├── QUICKSTART.md      # 快速入门指南
│   ├── ARCHITECTURE.md    # 架构说明
│   ├── UV_GUIDE.md        # uv 使用指南
│   ├── UV_MIGRATION.md    # uv 迁移说明
│   └── PROJECT_SUMMARY.md # 项目总结
├── knowledge_base/        # 知识库文档目录
│   └── README.md          # 示例文档
├── data/                  # 数据目录（自动创建）
│   └── chroma_db/         # 向量数据库
├── run.py                 # CLI 入口
├── server.py              # 服务器入口
├── pyproject.toml         # 项目配置和依赖（uv）
├── requirements.txt       # 依赖列表（兼容性）
├── .env.example           # 环境变量示例
└── README.md              # 项目主文档
```

详细的架构说明请查看 [架构文档](docs/ARCHITECTURE.md)。

## 配置说明

在 `.env` 文件中可配置的参数：

| 参数 | 说明 | 默认值 |
|------|------|--------|
| OPENAI_API_KEY | OpenAI API 密钥 | - |
| OPENAI_API_BASE | OpenAI API 地址 | https://api.openai.com/v1 |
| MODEL_NAME | 使用的模型 | gpt-3.5-turbo |
| VECTOR_DB_PATH | 向量数据库路径 | ./data/chroma_db |
| DOCUMENTS_PATH | 文档存储路径 | ./knowledge_base |
| HOST | 服务监听地址 | 0.0.0.0 |
| PORT | 服务端口 | 8000 |

在 `config.py` 中还可以配置：

- `chunk_size`: 文档分块大小（默认 1000）
- `chunk_overlap`: 分块重叠大小（默认 200）
- `top_k`: 检索文档数量（默认 3）

## 常见问题

### 1. 如何使用其他 LLM？

修改 `agent.py` 中的 OpenAI 客户端初始化部分，替换为其他 LLM 的 API。

### 2. 如何支持更多文档格式？

在 `document_loader.py` 中添加新的文档加载函数，并在 `load_document` 方法中注册。

### 3. 如何优化检索效果？

- 调整 `chunk_size` 和 `chunk_overlap` 参数
- 调整 `top_k` 参数以检索更多文档
- 使用更好的嵌入模型（修改 `vector_store.py`）

### 4. 内存占用过大？

- 减少 `chunk_size`
- 使用更小的嵌入模型
- 考虑使用支持持久化的向量数据库

## 开发计划

- [ ] 支持更多 LLM（如 Claude、本地模型等）
- [ ] 添加 Web UI 界面
- [ ] 支持多知识库管理
- [ ] 添加用户认证和权限管理
- [ ] 支持对话历史持久化
- [ ] 添加文档版本管理

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！
