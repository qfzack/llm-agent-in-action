# 项目架构说明

## 📁 新的项目结构

项目已重新组织为模块化架构，便于维护、扩展和迁移。

```
agent_demo/
├── src/                        # 源代码目录
│   ├── __init__.py
│   ├── core/                   # 核心功能模块
│   │   ├── __init__.py
│   │   ├── config.py          # 配置管理
│   │   └── agent.py           # AI Agent 核心逻辑
│   ├── services/               # 服务层
│   │   ├── __init__.py
│   │   ├── vector_store.py    # 向量数据库服务
│   │   └── document_loader.py # 文档加载服务
│   ├── api/                    # API 接口层
│   │   ├── __init__.py
│   │   └── main.py            # FastAPI 应用
│   └── cli/                    # 命令行工具
│       ├── __init__.py
│       └── cli.py             # CLI 实现
│
├── tests/                      # 测试目录
│   ├── __init__.py
│   └── test_api.py            # API 测试
│
├── scripts/                    # 脚本和工具
│   ├── start.sh               # Linux/Mac 启动脚本
│   ├── start.bat              # Windows 启动脚本
│   └── example_client.py      # 客户端示例
│
├── docs/                       # 📚 项目文档
│   ├── README.md              # 文档导航
│   ├── QUICKSTART.md          # 快速入门
│   ├── UV_GUIDE.md            # uv 指南
│   ├── UV_MIGRATION.md        # 迁移说明
│   ├── PROJECT_SUMMARY.md     # 项目总结
│   └── ARCHITECTURE.md        # 架构说明（本文件）
│
├── knowledge_base/             # 知识库文档目录
│   └── README.md              # 示例文档
│
├── data/                       # 运行时数据（自动生成）
│   └── chroma_db/             # 向量数据库
│
├── run.py                      # CLI 入口
├── server.py                   # 服务器入口
├── pyproject.toml             # 项目配置
├── requirements.txt           # 依赖列表
├── .env.example               # 环境变量示例
├── .gitignore                 # Git 忽略
├── LICENSE                    # 许可证
└── README.md                  # 主文档
```

## 🏗️ 架构设计

### 分层架构

项目采用经典的分层架构模式：

```
┌─────────────────────────────────────┐
│      入口层 (Entry Points)          │
│  run.py / server.py / scripts/      │
└─────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────┐
│      接口层 (Interface Layer)       │
│  src/api/    │    src/cli/          │
│  (FastAPI)   │    (Argparse)        │
└─────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────┐
│      核心层 (Core Layer)            │
│  src/core/agent.py                  │
│  src/core/config.py                 │
└─────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────┐
│      服务层 (Service Layer)         │
│  src/services/vector_store.py      │
│  src/services/document_loader.py   │
└─────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────┐
│      数据层 (Data Layer)            │
│  knowledge_base/  │  data/          │
└─────────────────────────────────────┘
```

### 模块职责

#### 1. Core (核心层)
- **config.py**: 统一的配置管理
- **agent.py**: AI Agent 核心逻辑，RAG 实现

#### 2. Services (服务层)
- **vector_store.py**: 向量数据库的封装
- **document_loader.py**: 文档加载和处理服务

#### 3. API (接口层)
- **main.py**: FastAPI 应用，提供 RESTful API

#### 4. CLI (命令行层)
- **cli.py**: 命令行工具实现

#### 5. Tests (测试层)
- **test_api.py**: API 接口测试

## 🔄 数据流

### 文档加载流程

```
knowledge_base/*.pdf,docx,md,txt
         ↓
DocumentLoader.load_all_documents()
         ↓
TextSplitter.split_documents()
         ↓
VectorStore.add_documents()
         ↓
ChromaDB (data/chroma_db/)
```

### 查询流程

```
User Query
    ↓
API/CLI Interface
    ↓
AIAgent.chat()
    ↓
VectorStore.query()  →  检索相关文档
    ↓
AIAgent.build_context()  →  构建上下文
    ↓
AIAgent.generate_prompt()  →  生成提示词
    ↓
OpenAI API  →  生成回答
    ↓
Return Response
```

## 🎯 设计原则

### 1. 单一职责原则 (SRP)
每个模块只负责一个功能领域：
- `config.py` 只管配置
- `vector_store.py` 只管向量存储
- `agent.py` 只管 AI 逻辑

### 2. 依赖倒置原则 (DIP)
高层模块不依赖低层模块，都依赖抽象：
- Core 层不直接依赖具体实现
- 通过接口和配置解耦

### 3. 开闭原则 (OCP)
对扩展开放，对修改关闭：
- 可以轻松添加新的文档类型
- 可以替换不同的向量数据库
- 可以切换不同的 LLM

### 4. 接口隔离原则 (ISP)
不同的接口服务不同的客户端：
- API 接口服务 Web 客户端
- CLI 接口服务命令行用户

## 🚀 使用方式

### 1. 命令行方式

```bash
# 加载文档
uv run python run.py load

# 交互式查询
uv run python run.py query

# 查看状态
uv run python run.py status
```

### 2. API 服务方式

```bash
# 启动服务器
uv run python server.py

# 或使用 uvicorn 直接运行
uv run uvicorn src.api.main:app --reload
```

### 3. 脚本方式

```bash
# 使用启动脚本
./scripts/start.sh        # Linux/Mac
scripts\start.bat         # Windows
```

### 4. Python 模块方式

```python
from src.core.agent import AIAgent
from src.core.config import settings
from src.services.vector_store import VectorStore

# 初始化
vector_store = VectorStore(settings.vector_db_path)
agent = AIAgent(vector_store)

# 使用
result = agent.chat("你的问题")
print(result['answer'])
```

## 📦 模块导入规则

### 相对导入
在 `src/` 目录内使用相对导入：

```python
# 在 src/core/agent.py 中
from ..services.vector_store import VectorStore
from .config import settings
```

### 绝对导入
在根目录脚本中使用绝对导入：

```python
# 在 run.py 中
from src.cli.cli import main
```

## 🔧 扩展指南

### 添加新的文档类型

在 `src/services/document_loader.py` 中：

```python
def load_new_format(self, file_path: Path) -> str:
    # 实现新格式加载
    pass

# 注册到 loaders 字典
loaders = {
    '.pdf': self.load_pdf,
    '.newformat': self.load_new_format,  # 新增
}
```

### 切换向量数据库

创建新的向量存储实现：

```python
# src/services/new_vector_store.py
class NewVectorStore:
    def __init__(self, db_path: str):
        # 实现新的向量存储
        pass
```

修改配置和初始化代码即可。

### 添加新的 API 端点

在 `src/api/main.py` 中：

```python
@app.post("/new-endpoint")
async def new_endpoint():
    # 实现新端点
    pass
```

### 添加新的 CLI 命令

在 `src/cli/cli.py` 中：

```python
def new_command():
    # 实现新命令
    pass

# 在 main() 中注册
subparsers.add_parser('new', help='新命令')
```

## 🧪 测试策略

### 单元测试
测试各个模块的独立功能：

```python
# tests/test_vector_store.py
def test_vector_store():
    store = VectorStore("./test_data")
    # 测试...
```

### 集成测试
测试模块间的协作：

```python
# tests/test_integration.py
def test_full_workflow():
    # 测试完整流程
    pass
```

### API 测试
测试 HTTP 接口：

```python
# tests/test_api.py
def test_query_endpoint():
    response = requests.post("/query", json={"query": "测试"})
    assert response.status_code == 200
```

## 📝 开发规范

### 1. 代码风格
- 遵循 PEP 8
- 使用类型注解
- 添加文档字符串

### 2. 提交规范
- `feat:` 新功能
- `fix:` 修复
- `docs:` 文档
- `refactor:` 重构
- `test:` 测试

### 3. 分支管理
- `main`: 稳定版本
- `dev`: 开发版本
- `feature/*`: 功能分支

## 🔄 迁移和部署

### 1. 开发环境

```bash
uv sync
uv run python run.py status
```

### 2. 生产环境

```bash
# 使用 Docker
docker build -t ai-agent .
docker run -p 8000:8000 ai-agent

# 或使用 gunicorn
gunicorn src.api.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### 3. 云部署
- 支持部署到任何支持 Python 的云平台
- 环境变量通过 `.env` 文件配置
- 数据目录需要持久化存储

## 📊 性能优化建议

1. **向量检索优化**: 调整 `top_k` 参数
2. **文档分块优化**: 调整 `chunk_size` 和 `chunk_overlap`
3. **缓存策略**: 添加查询结果缓存
4. **并发处理**: 使用异步处理提高吞吐量

## 🛠️ 故障排查

### 导入错误
确保从项目根目录运行：
```bash
cd /path/to/agent_demo
uv run python run.py
```

### 路径问题
所有路径使用相对于项目根目录的路径。

### 模块未找到
检查 `__init__.py` 文件是否存在。

## 📚 相关文档

- [快速入门](QUICKSTART.md)
- [项目总结](PROJECT_SUMMARY.md)
- [uv 使用指南](UV_GUIDE.md)
- [主文档](../README.md)

---

**架构持续演进中，欢迎贡献改进建议！** 🚀
