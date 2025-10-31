# BAML 集成实施指南

## 快速开始

### 第一步：安装 BAML

```bash
# 1. 安装 BAML Python 包
pip install baml-py

# 2. 验证安装
baml-cli --version
```

### 第二步：初始化项目（可选）

如果你是全新项目：
```bash
baml init
```

如果已有项目（我们的情况），已经准备好了 `baml_src/` 目录，跳过此步。

### 第三步：生成 Python 客户端

```bash
# 在项目根目录运行
baml-cli generate

# 这会生成 baml_client/ 目录，包含类型安全的 Python 代码
```

### 第四步：配置环境变量

在 `.env` 文件中添加（如果还没有）：

```env
# OpenAI (必需)
OPENAI_API_KEY=your_openai_key
OPENAI_API_BASE=https://api.openai.com/v1

# Anthropic Claude (可选)
ANTHROPIC_API_KEY=your_anthropic_key

# Google Gemini (可选)
GEMINI_API_KEY=your_gemini_key
```

### 第五步：测试 BAML

```bash
# 运行 BAML 测试（如果有）
baml test

# 或者运行示例代码
python -m src.core.agent_baml
```

---

## 详细集成步骤

### 1. 项目结构

当前已创建的 BAML 文件：

```
baml_src/
├── clients.baml          # ✅ LLM 客户端配置
├── types.baml            # ✅ 数据类型定义
└── functions/
    ├── rag.baml          # ✅ RAG 问答函数
    ├── analysis.baml     # ✅ 文档分析函数
    └── reasoning.baml    # ✅ 推理函数
```

生成后会有：
```
baml_client/             # 自动生成的 Python 客户端
├── __init__.py
├── types.py            # 类型定义
└── ...
```

### 2. 使用 BAML Agent

#### 方式 1：直接使用（推荐用于新功能）

```python
from baml_client import b
from baml_client.types import ChatResponse
import asyncio

async def main():
    # 调用 BAML 函数
    response: ChatResponse = await b.RAGChat(
        query="什么是机器学习？",
        context="机器学习是...",
        has_context=True
    )
    
    # 类型安全的访问
    print(response.answer)
    print(response.confidence)
    print(response.category)
    for source in response.sources:
        print(source)

asyncio.run(main())
```

#### 方式 2：集成到现有 Agent

已创建 `src/core/agent_baml.py`，使用方式：

```python
from src.core.agent_baml import BAMLAgent
from src.services.vector_store import VectorStore
from src.core.config import settings
import asyncio

async def main():
    vector_store = VectorStore(settings.vector_db_path)
    agent = BAMLAgent(vector_store)
    
    response = await agent.chat("你的问题")
    print(response)

asyncio.run(main())
```

### 3. 创建 CLI 工具（BAML 版本）

创建 `src/cli/cli_baml.py`：

```python
"""使用 BAML 的命令行工具"""
import asyncio
from ..core.agent_baml import BAMLAgent
from ..services.vector_store import VectorStore
from ..core.config import settings

async def interactive_query():
    """交互式问答（BAML 版本）"""
    print("=== BAML Agent 交互式问答 ===")
    print("输入 'quit' 退出\n")
    
    vector_store = VectorStore(settings.vector_db_path)
    agent = BAMLAgent(vector_store)
    
    conversation_history = []
    
    while True:
        query = input("您: ").strip()
        if query.lower() in ['quit', 'exit']:
            break
        
        # 使用 BAML Agent
        result = await agent.chat(query, conversation_history)
        
        print(f"\nAI: {result['answer']}")
        print(f"置信度: {result['confidence']:.2f}")
        print(f"分类: {result['category']}")
        
        if result.get('sources'):
            print("\n来源:")
            for source in result['sources']:
                print(f"  - {source}")
        
        # 更新历史
        conversation_history.append({
            "role": "user",
            "content": query
        })
        conversation_history.append({
            "role": "assistant", 
            "content": result['answer']
        })
        
        print()

if __name__ == "__main__":
    asyncio.run(interactive_query())
```

运行：
```bash
python -m src.cli.cli_baml
```

### 4. 创建 API 端点（BAML 版本）

创建 `src/api/main_baml.py`：

```python
"""使用 BAML 的 FastAPI 服务"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict
import asyncio

from ..core.agent_baml import BAMLAgent
from ..services.vector_store import VectorStore
from ..core.config import settings

app = FastAPI(title="BAML Agent API")

# 初始化
vector_store = VectorStore(settings.vector_db_path)
agent = BAMLAgent(vector_store)

class QueryRequest(BaseModel):
    query: str
    conversation_history: Optional[List[Dict[str, str]]] = None

class QueryResponse(BaseModel):
    answer: str
    confidence: float
    has_context: bool
    sources: List[str]
    category: str

@app.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    """问答接口（使用 BAML）"""
    try:
        result = await agent.chat(
            request.query,
            request.conversation_history
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze")
async def analyze_document(text: str):
    """文档分析接口"""
    try:
        result = await agent.analyze_document(text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "healthy", "agent": "BAML"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
```

运行：
```bash
# 使用不同端口避免冲突
python -m src.api.main_baml
# 访问 http://localhost:8001/docs
```

---

## 测试 BAML

### 创建测试文件

创建 `baml_src/tests/rag_test.baml`：

```baml
test "Basic RAG with context" {
  functions [RAGChat]
  args {
    query "什么是机器学习？"
    context "机器学习是人工智能的一个分支，使计算机能够从数据中学习。"
    has_context true
  }
  assert {
    output.answer is string
    output.confidence >= 0.5
    output.has_context == true
  }
}

test "RAG without context" {
  functions [RAGChat]
  args {
    query "今天天气怎么样？"
    context ""
    has_context false
  }
  assert {
    output.has_context == false
  }
}

test "Document analysis" {
  functions [AnalyzeDocument]
  args {
    text "Python是一种流行的编程语言，广泛用于数据科学和机器学习。"
  }
  assert {
    output.summary is string
    output.key_points.length >= 1
    output.complexity in [Complexity.Easy, Complexity.Medium, Complexity.Hard]
  }
}
```

运行测试：
```bash
baml test
```

---

## 切换 LLM 模型

### 方法 1：修改函数定义

在 `baml_src/functions/rag.baml` 中：

```baml
function RAGChat(...) -> ChatResponse {
  client GPT4  // 改成 GPT35Turbo、Claude 或 Gemini
  prompt #"..."#
}
```

### 方法 2：运行时选择

```python
from baml_client import b

# 使用不同的客户端
response = await b.RAGChat.with_client("Claude")(
    query=query,
    context=context,
    has_context=True
)
```

---

## 对比：旧 vs 新

### 旧方式（原始代码）

```python
# 类型不安全，容易出错
result = agent.chat(query)
answer = result["answer"]  # 可能 KeyError
confidence = result.get("confidence", 0)  # 没有类型检查

# Prompt 在代码里
def generate_prompt(query, context):
    return f"""你是一个AI助手...
    {context}
    {query}
    """

# 切换模型需要改代码
self.llm_adapter = LLMFactory.create_adapter(
    provider="openai",  # 要改这里
    ...
)
```

### 新方式（BAML）

```python
# 类型安全
response: ChatResponse = await b.RAGChat(
    query=query,
    context=context,
    has_context=True
)
print(response.answer)  # IDE 自动完成
print(response.confidence)  # 类型检查

# Prompt 在 .baml 文件中管理
# 切换模型只需改配置文件中的 client 名称
```

---

## 性能优化

### 并行调用

```python
import asyncio

# 同时调用多个 BAML 函数
results = await asyncio.gather(
    b.RAGChat(query1, context1, True),
    b.RAGChat(query2, context2, True),
    b.AnalyzeDocument(text)
)
```

### 流式输出

```python
# BAML 支持流式响应
async for chunk in b.RAGChat.stream(query, context, True):
    print(chunk, end="", flush=True)
```

---

## 监控和调试

### BAML Studio

```bash
# 启动 BAML Studio（可视化界面）
baml studio
```

在浏览器中查看：
- 所有 LLM 调用记录
- Prompt 和响应
- Token 使用量
- 响应时间
- 成本统计

### 日志

```python
import logging
from baml_client import b

# 启用详细日志
logging.basicConfig(level=logging.DEBUG)

response = await b.RAGChat(query, context, True)
# 会自动记录调用详情
```

---

## 常见问题

### Q1: 如何保持向后兼容？

**A**: 同时保留两个 Agent：

```python
# 旧 Agent（保持不变）
from src.core.agent import AIAgent

# 新 BAML Agent
from src.core.agent_baml import BAMLAgent

# 在 API 中提供两个端点
@app.post("/query")  # 旧接口
async def query_old():
    agent = AIAgent(vector_store)
    return agent.chat(query)

@app.post("/query-baml")  # 新接口
async def query_new():
    agent = BAMLAgent(vector_store)
    return await agent.chat(query)
```

### Q2: BAML 支持哪些 LLM？

**A**: 支持主流 LLM：
- OpenAI (GPT-3.5, GPT-4, GPT-4o)
- Anthropic (Claude)
- Google (Gemini)
- Ollama (本地模型)
- Azure OpenAI
- 自定义 OpenAI 兼容 API

### Q3: BAML 会增加延迟吗？

**A**: 几乎没有。BAML 只是在调用前后做类型转换和验证，开销极小（< 1ms）。

### Q4: 如何调试 Prompt？

**A**: 
1. 使用 `baml studio` 查看实际发送的 Prompt
2. 在 `.baml` 文件中迭代修改
3. 使用 `baml test` 验证效果

### Q5: 生成的代码需要提交吗？

**A**: 
```bash
# 建议添加到 .gitignore
echo "baml_client/" >> .gitignore

# 在 CI/CD 中自动生成
baml-cli generate
```

---

## 更新 requirements.txt

```bash
# 添加 BAML 依赖
echo "baml-py>=0.40.0" >> requirements.txt

# 重新安装
pip install -r requirements.txt
```

---

## 下一步

### 立即尝试

1. **安装 BAML**
   ```bash
   pip install baml-py
   ```

2. **生成客户端**
   ```bash
   baml-cli generate
   ```

3. **运行示例**
   ```bash
   python -m src.core.agent_baml
   ```

### 渐进迁移

1. **Week 1**: 为新功能使用 BAML
2. **Week 2**: 迁移核心问答功能
3. **Week 3**: 迁移文档分析功能
4. **Week 4**: 完全迁移到 BAML

### 学习资源

- 📚 [BAML 官方文档](https://docs.boundaryml.com)
- 🎮 [交互式教程](https://playground.boundaryml.com)
- 💬 [Discord 社区](https://discord.gg/boundaryml)
- 📹 [视频教程](https://youtube.com/@boundaryml)

---

**准备好了吗？开始使用 BAML 让你的 LLM Agent 更强大！** 🚀
