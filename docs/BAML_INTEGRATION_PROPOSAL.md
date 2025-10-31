# BAML 集成方案：为 LLM Agent 项目带来结构化 AI 编程

## 目录
- [BAML 简介](#baml-简介)
- [引入 BAML 的优势](#引入-baml-的优势)
- [当前项目痛点分析](#当前项目痛点分析)
- [BAML 解决方案](#baml-解决方案)
- [实现方案](#实现方案)
- [代码示例对比](#代码示例对比)
- [集成步骤](#集成步骤)
- [最佳实践](#最佳实践)

---

## BAML 简介

**BAML** (Basically A Made-up Language) 是一种专门为 LLM 交互设计的领域特定语言（DSL），由 BoundaryML 开发。它提供了：

- 📝 **类型安全的 Prompt 模板**：使用强类型定义输入输出
- 🎯 **结构化输出**：自动将 LLM 响应解析为结构化数据
- 🔄 **多模型支持**：统一的接口支持不同 LLM 提供商
- ✅ **测试和验证**：内置测试框架确保 prompt 质量
- 📊 **可观测性**：自动追踪和监控 LLM 调用

### 核心概念

```baml
// 1. 定义数据结构
class QueryResult {
  answer string
  confidence float
  sources string[]
  category string
}

// 2. 定义函数（Prompt模板）
function AnswerQuestion(query: string, context: string) -> QueryResult {
  client GPT4
  prompt #"
    Based on the following context, answer the question.
    
    Context: {{ context }}
    Question: {{ query }}
    
    Provide a detailed answer with confidence score and sources.
  "#
}
```

---

## 引入 BAML 的优势

### 1. **类型安全与数据验证** 🛡️

**当前问题**：
```python
# 当前代码中，返回的是字典，类型不明确
result = agent.chat(query)
answer = result["answer"]  # 可能 KeyError
docs = result["retrieved_docs"]  # 类型未知
```

**BAML 解决方案**：
```baml
class ChatResponse {
  answer string
  retrieved_docs DocumentReference[]
  has_context bool
  confidence float?
}

function ChatWithRAG(query: string, context: string) -> ChatResponse {
  // 自动类型验证和解析
}
```

```python
# 使用 BAML 后，类型安全
result = baml.ChatWithRAG(query, context)
print(result.answer)  # IDE 自动完成
print(result.confidence)  # 类型检查
```

### 2. **Prompt 版本管理和模块化** 📦

**当前问题**：
```python
# Prompt 分散在 Python 代码中，难以管理
def generate_prompt(self, query: str, context: str) -> str:
    if context:
        prompt = f"""你是一个专业的AI助手...
        
文档内容：
{context}

用户问题：{query}

请提供准确、详细的回答："""
    else:
        prompt = f"""你是一个专业的AI助手..."""
    return prompt
```

**BAML 解决方案**：
```baml
// prompts/rag.baml
function RAGQuery(query: string, context: string) -> Answer {
  client GPT4
  prompt #"
    You are a professional AI assistant.
    
    {% if context %}
    Based on the following documents, answer the question.
    
    Documents:
    {{ context }}
    {% endif %}
    
    Question: {{ query }}
    
    Provide an accurate and detailed answer.
  "#
}

// prompts/general.baml
function GeneralQuery(query: string) -> Answer {
  client GPT4
  prompt #"
    You are a helpful AI assistant.
    
    Question: {{ query }}
    
    Note: This answer is based on general knowledge, not specific documents.
  "#
}
```

### 3. **多模型无缝切换** 🔄

**当前问题**：
```python
# 需要手动实现适配器模式
class OpenAIAdapter(LLMAdapter):
    def chat(self, messages, **kwargs):
        # OpenAI 特定实现
        
class GeminiAdapter(LLMAdapter):
    def chat(self, messages, **kwargs):
        # Gemini 特定实现
        # 需要转换消息格式
```

**BAML 解决方案**：
```baml
// 定义多个客户端
client GPT4 {
  provider openai
  options {
    model "gpt-4"
    api_key env.OPENAI_API_KEY
  }
}

client Claude {
  provider anthropic
  options {
    model "claude-3-sonnet"
    api_key env.ANTHROPIC_API_KEY
  }
}

client Gemini {
  provider google
  options {
    model "gemini-pro"
    api_key env.GEMINI_API_KEY
  }
}

// 一键切换模型
function AnswerQuestion(query: string) -> Answer {
  client GPT4  // 改成 Claude 或 Gemini 即可
  prompt #"..."#
}
```

### 4. **结构化输出与解析** 📊

**当前问题**：
```python
# LLM 返回自由文本，需要手动解析
answer = self.llm_adapter.chat(messages, ...)
# 如果需要结构化数据，需要用 JSON 解析或正则表达式
```

**BAML 解决方案**：
```baml
class AnalysisResult {
  summary string
  key_points string[]
  sentiment enum {
    Positive
    Negative
    Neutral
  }
  confidence float
  entities Entity[]
}

class Entity {
  name string
  type enum {
    Person
    Organization
    Location
  }
}

function AnalyzeDocument(text: string) -> AnalysisResult {
  client GPT4
  prompt #"
    Analyze the following text and extract structured information.
    
    Text: {{ text }}
  "#
}
```

```python
# 自动解析为结构化对象
result = baml.AnalyzeDocument(document_text)
print(result.summary)
print(f"Sentiment: {result.sentiment}")
for point in result.key_points:
    print(f"- {point}")
for entity in result.entities:
    print(f"{entity.name} ({entity.type})")
```

### 5. **内置测试和验证** ✅

**当前问题**：
- 没有系统的 Prompt 测试机制
- 修改 Prompt 后难以验证效果
- 无法进行 A/B 测试

**BAML 解决方案**：
```baml
// tests/rag_test.baml
test "Basic RAG Query" {
  functions [RAGQuery]
  args {
    query "什么是机器学习？"
    context "机器学习是人工智能的一个分支..."
  }
  assert {
    // 验证输出结构
    output.answer is string
    output.confidence > 0.7
    output.sources.length > 0
  }
}

test "Empty Context Handling" {
  functions [RAGQuery]
  args {
    query "天气怎么样？"
    context ""
  }
  assert {
    output.has_context == false
  }
}
```

### 6. **可观测性和调试** 🔍

**BAML 优势**：
- 自动记录所有 LLM 调用
- 追踪 Prompt 和响应
- 性能监控和分析
- 成本追踪

```python
# BAML 自动记录调用链路
import baml_client as baml

result = baml.ChatWithRAG(query, context)
# 可在 BAML Studio 中查看：
# - 完整的 Prompt
# - LLM 响应
# - Token 使用量
# - 响应时间
```

---

## 当前项目痛点分析

### 问题 1：Prompt 管理混乱
```python
# src/core/agent.py
def generate_prompt(self, query: str, context: str) -> str:
    if context:
        prompt = f"""你是一个专业的AI助手...{context}..."""
    else:
        prompt = f"""你是一个专业的AI助手..."""
    return prompt
```
❌ **痛点**：
- Prompt 硬编码在 Python 代码中
- 修改 Prompt 需要改代码
- 无法版本控制 Prompt
- 难以进行 A/B 测试

### 问题 2：类型不安全
```python
# src/core/agent.py
def chat(self, query: str, conversation_history: List[Dict[str, str]] = None) -> Dict[str, str]:
    return {
        "answer": answer,
        "retrieved_docs": retrieved_docs,
        "has_context": bool(context)
    }
```
❌ **痛点**：
- 返回值是字典，类型不明确
- 容易拼错键名
- IDE 无法提供自动完成
- 运行时才能发现错误

### 问题 3：LLM 切换困难
```python
# src/core/llm_adapter.py
# 需要为每个 LLM 实现适配器
class OpenAIAdapter(LLMAdapter):
    def chat(self, messages, **kwargs):
        # 40+ 行代码
        
class GeminiAdapter(LLMAdapter):
    def chat(self, messages, **kwargs):
        # 需要手动转换消息格式
```
❌ **痛点**：
- 大量重复代码
- 消息格式转换繁琐
- 添加新 LLM 需要写大量代码

### 问题 4：缺乏结构化输出
```python
# 如果需要更复杂的输出结构
answer = self.llm_adapter.chat(messages, ...)
# 只能得到文本，需要手动解析
```
❌ **痛点**：
- 无法强制 LLM 返回特定格式
- 解析失败率高
- 代码冗余

---

## BAML 解决方案

### 架构对比

#### 当前架构
```
┌─────────────┐
│   CLI/API   │
└──────┬──────┘
       │
┌──────▼──────┐      ┌──────────────┐
│   Agent     │─────▶│ LLM Adapter  │
└──────┬──────┘      │ (OpenAI/     │
       │             │  Gemini/...)  │
┌──────▼──────┐      └──────────────┘
│ VectorStore │
└─────────────┘
```

#### BAML 架构
```
┌─────────────┐
│   CLI/API   │
└──────┬──────┘
       │
┌──────▼──────┐      ┌──────────────┐
│   Agent     │─────▶│ BAML Client  │
└──────┬──────┘      │ (统一接口)   │
       │             └───────┬──────┘
┌──────▼──────┐              │
│ VectorStore │      ┌───────▼──────────┐
└─────────────┘      │ BAML Functions   │
                     │ (Prompt模板)     │
                     └───────┬──────────┘
                             │
                     ┌───────▼──────────┐
                     │ Multi-Provider   │
                     │ (OpenAI/Claude/  │
                     │  Gemini/...)     │
                     └──────────────────┘
```

---

## 实现方案

### 方案概述

1. **保持现有功能**：不破坏现有代码
2. **渐进式集成**：可以同时使用旧代码和 BAML
3. **模块化设计**：BAML 作为一个新的模块

### 目录结构

```
llm-agent-in-action/
├── baml_src/                    # 新增：BAML 配置目录
│   ├── clients.baml             # LLM 客户端配置
│   ├── types.baml               # 数据类型定义
│   ├── functions/               # Prompt 函数
│   │   ├── rag.baml            # RAG 相关 Prompts
│   │   ├── analysis.baml       # 分析类 Prompts
│   │   └── chat.baml           # 对话类 Prompts
│   └── tests/                   # BAML 测试
│       └── rag_test.baml
├── baml_client/                 # 生成的 Python 客户端
│   └── ...
├── src/
│   ├── core/
│   │   ├── agent.py            # 保持原有
│   │   ├── agent_baml.py       # 新增：使用 BAML 的 Agent
│   │   ├── llm_adapter.py      # 保持原有
│   │   └── ...
│   └── ...
├── pyproject.toml
└── requirements.txt
```

---

## 代码示例对比

### 示例 1：基本问答

#### 当前实现（~80 行）
```python
# src/core/agent.py
class AIAgent:
    def chat(self, query: str, conversation_history: List[Dict[str, str]] = None) -> Dict[str, str]:
        context = self.build_context(query)
        prompt = self.generate_prompt(query, context)
        
        messages = []
        if conversation_history:
            messages.extend(conversation_history[-10:])
        messages.append({"role": "user", "content": prompt})
        
        try:
            answer = self.llm_adapter.chat(
                messages=messages,
                temperature=0.7,
                max_tokens=2000
            )
            retrieved_docs = self.vector_store.query(query, top_k=self.top_k)
            return {
                "answer": answer,
                "retrieved_docs": retrieved_docs,
                "has_context": bool(context)
            }
        except Exception as e:
            return {
                "answer": f"抱歉，处理您的问题时发生错误: {str(e)}",
                "retrieved_docs": [],
                "has_context": False,
                "error": str(e)
            }
```

#### BAML 实现（~30 行）

**1. 定义类型** (`baml_src/types.baml`):
```baml
class ChatResponse {
  answer string
  confidence float
  has_context bool
  sources string[]
  category enum {
    Technical
    General
    Personal
    Unknown
  }
}

class DocumentChunk {
  content string
  filename string
  score float
}
```

**2. 定义函数** (`baml_src/functions/rag.baml`):
```baml
function RAGChat(
  query: string,
  context: string,
  has_context: bool
) -> ChatResponse {
  client GPT4
  prompt #"
    You are a professional AI assistant specialized in question answering.
    
    {% if has_context %}
    Please answer the question based on the following documents.
    If the documents don't contain relevant information, state that clearly.
    
    Documents:
    {{ context }}
    {% else %}
    Note: No specific documents found in the knowledge base.
    Please answer based on general knowledge and inform the user.
    {% endif %}
    
    Question: {{ query }}
    
    Provide a detailed answer with:
    - Confidence level (0-1)
    - Source references (if applicable)
    - Category of the question
    
    {{ ctx.output_format }}
  "#
}
```

**3. Python 代码** (`src/core/agent_baml.py`):
```python
from baml_client import b
from baml_client.types import ChatResponse

class BAMLAgent:
    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store
        self.top_k = settings.top_k
    
    async def chat(self, query: str) -> ChatResponse:
        # 检索上下文
        docs = self.vector_store.query(query, top_k=self.top_k)
        context = self._build_context(docs)
        
        # 调用 BAML 函数
        response = await b.RAGChat(
            query=query,
            context=context,
            has_context=bool(docs)
        )
        
        return response  # 类型安全的对象
    
    def _build_context(self, docs: List) -> str:
        return "\n\n".join([
            f"[{doc['metadata']['filename']}]\n{doc['content']}"
            for doc in docs
        ])
```

**使用对比**:

```python
# 旧方式
result = agent.chat(query)
print(result["answer"])  # 字典，可能 KeyError

# BAML 方式
result = await baml_agent.chat(query)
print(result.answer)  # 类型安全，IDE 自动完成
print(f"Confidence: {result.confidence}")
print(f"Category: {result.category}")
for source in result.sources:
    print(f"Source: {source}")
```

### 示例 2：文档分析

#### BAML 实现

**定义** (`baml_src/functions/analysis.baml`):
```baml
class DocumentAnalysis {
  summary string @description("简短摘要，不超过200字")
  key_points string[] @description("3-5个关键要点")
  topics string[] @description("主要主题标签")
  sentiment enum {
    Positive
    Negative  
    Neutral
  }
  entities Entity[]
  complexity enum {
    Easy
    Medium
    Hard
  }
}

class Entity {
  name string
  type enum {
    Person
    Organization
    Location
    Technology
    Concept
  }
  mentions int
}

function AnalyzeDocument(text: string) -> DocumentAnalysis {
  client GPT4
  prompt #"
    Analyze the following document and extract structured information.
    
    Document:
    {{ text }}
    
    Provide a comprehensive analysis including:
    - A concise summary
    - Key points (3-5 items)
    - Topic tags
    - Overall sentiment
    - Named entities with their types
    - Complexity level
    
    {{ ctx.output_format }}
  "#
}
```

**使用**:
```python
from baml_client import b

async def analyze_uploaded_document(file_content: str):
    analysis = await b.AnalyzeDocument(text=file_content)
    
    print(f"摘要: {analysis.summary}")
    print(f"复杂度: {analysis.complexity}")
    print(f"情感: {analysis.sentiment}")
    
    print("\n关键要点:")
    for i, point in enumerate(analysis.key_points, 1):
        print(f"{i}. {point}")
    
    print("\n实体:")
    for entity in analysis.entities:
        print(f"- {entity.name} ({entity.type}) - 提及 {entity.mentions} 次")
    
    return analysis
```

### 示例 3：多步骤推理

**定义** (`baml_src/functions/reasoning.baml`):
```baml
class ReasoningStep {
  step_number int
  description string
  conclusion string
}

class ReasoningResult {
  steps ReasoningStep[]
  final_answer string
  confidence float
}

function StepByStepReasoning(
  question: string,
  context: string
) -> ReasoningResult {
  client GPT4
  prompt #"
    Answer the following question using step-by-step reasoning.
    
    Context:
    {{ context }}
    
    Question: {{ question }}
    
    Break down your reasoning into clear steps:
    1. First, identify what information is needed
    2. Then, extract relevant facts from the context
    3. Apply logical reasoning
    4. Reach a conclusion
    
    Provide your reasoning process and final answer.
    
    {{ ctx.output_format }}
  "#
}
```

---

## 集成步骤

### 步骤 1：安装 BAML

```bash
# 安装 BAML CLI
pip install baml-py

# 初始化 BAML 项目
baml init
```

### 步骤 2：配置 BAML 客户端

创建 `baml_src/clients.baml`:
```baml
client GPT4 {
  provider openai
  options {
    model "gpt-4"
    api_key env.OPENAI_API_KEY
    base_url env.OPENAI_API_BASE
  }
}

client GPT35Turbo {
  provider openai
  options {
    model "gpt-3.5-turbo"
    api_key env.OPENAI_API_KEY
    base_url env.OPENAI_API_BASE
  }
}

client Claude {
  provider anthropic
  options {
    model "claude-3-sonnet-20240229"
    api_key env.ANTHROPIC_API_KEY
  }
}

client Gemini {
  provider google
  options {
    model "gemini-pro"
    api_key env.GEMINI_API_KEY
  }
}
```

### 步骤 3：定义数据类型

创建 `baml_src/types.baml`:
```baml
class ChatResponse {
  answer string
  confidence float
  has_context bool
  sources string[]
  category QuestionCategory
}

enum QuestionCategory {
  Technical
  General
  Personal
  Unknown
}

class DocumentReference {
  filename string
  content string
  score float
}
```

### 步骤 4：创建 Prompt 函数

创建 `baml_src/functions/rag.baml`:
```baml
function RAGChat(
  query: string,
  context: string,
  has_context: bool
) -> ChatResponse {
  client GPT4
  prompt #"
    // Prompt 内容
  "#
}
```

### 步骤 5：生成 Python 客户端

```bash
# 生成类型安全的 Python 客户端
baml-cli generate

# 这会在 baml_client/ 目录生成代码
```

### 步骤 6：集成到现有代码

创建 `src/core/agent_baml.py`:
```python
from baml_client import b
from baml_client.types import ChatResponse
from ..services.vector_store import VectorStore
from ..core.config import settings

class BAMLAgent:
    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store
        self.top_k = settings.top_k
    
    async def chat(self, query: str) -> ChatResponse:
        # 检索文档
        docs = self.vector_store.query(query, top_k=self.top_k)
        context = self._build_context(docs)
        
        # 调用 BAML 函数
        response = await b.RAGChat(
            query=query,
            context=context,
            has_context=bool(docs)
        )
        
        return response
    
    def _build_context(self, docs: List) -> str:
        if not docs:
            return ""
        
        context_parts = []
        for i, doc in enumerate(docs, 1):
            filename = doc['metadata'].get('filename', '未知')
            content = doc['content']
            context_parts.append(f"[文档{i}: {filename}]\n{content}")
        
        return "\n\n".join(context_parts)
```

### 步骤 7：更新 CLI 和 API

**CLI** (`src/cli/cli_baml.py`):
```python
import asyncio
from ..core.agent_baml import BAMLAgent
from ..services.vector_store import VectorStore
from ..core.config import settings

async def query_with_baml():
    vector_store = VectorStore(settings.vector_db_path)
    agent = BAMLAgent(vector_store)
    
    while True:
        query = input("您: ").strip()
        if query.lower() in ['quit', 'exit']:
            break
        
        result = await agent.chat(query)
        
        print(f"\nAI: {result.answer}")
        print(f"置信度: {result.confidence:.2f}")
        print(f"类别: {result.category}")
        
        if result.sources:
            print("\n来源:")
            for source in result.sources:
                print(f"- {source}")

if __name__ == "__main__":
    asyncio.run(query_with_baml())
```

**API** (`src/api/main_baml.py`):
```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from ..core.agent_baml import BAMLAgent
from ..services.vector_store import VectorStore
from ..core.config import settings

app = FastAPI()
vector_store = VectorStore(settings.vector_db_path)
agent = BAMLAgent(vector_store)

class QueryRequest(BaseModel):
    query: str

@app.post("/query")
async def query(request: QueryRequest):
    try:
        result = await agent.chat(request.query)
        return {
            "answer": result.answer,
            "confidence": result.confidence,
            "has_context": result.has_context,
            "sources": result.sources,
            "category": result.category
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

---

## 最佳实践

### 1. Prompt 组织

```
baml_src/
├── clients.baml          # 客户端配置
├── types.baml            # 通用类型
└── functions/
    ├── rag/
    │   ├── basic.baml    # 基础问答
    │   ├── analysis.baml # 文档分析
    │   └── summary.baml  # 摘要生成
    ├── chat/
    │   ├── casual.baml   # 闲聊
    │   └── support.baml  # 客服
    └── advanced/
        ├── reasoning.baml # 推理
        └── planning.baml  # 规划
```

### 2. 测试驱动开发

```baml
// tests/rag_test.baml
test "Basic RAG with context" {
  functions [RAGChat]
  args {
    query "什么是机器学习？"
    context "机器学习是人工智能的一个分支..."
    has_context true
  }
  assert {
    output.answer is string
    output.confidence >= 0.5
    output.has_context == true
    output.category != QuestionCategory.Unknown
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
```

运行测试:
```bash
baml test
```

### 3. 版本控制

```baml
// 使用版本标注
function RAGChat_v2(query: string, context: string) -> ChatResponse {
  client GPT4
  prompt #"
    // 改进的 Prompt
  "#
}

// A/B 测试
function RAGChat_experimental(query: string, context: string) -> ChatResponse {
  client Claude  // 测试不同模型
  prompt #"
    // 实验性 Prompt
  "#
}
```

### 4. 错误处理

```python
from baml_client import b
from baml_client.errors import BAMLError

async def safe_chat(query: str) -> dict:
    try:
        result = await b.RAGChat(
            query=query,
            context=context,
            has_context=bool(context)
        )
        return {
            "success": True,
            "data": result
        }
    except BAMLError as e:
        return {
            "success": False,
            "error": str(e),
            "fallback": "使用默认回答"
        }
```

### 5. 监控和日志

```python
import baml_client as baml

# BAML 自动追踪所有调用
result = await baml.RAGChat(query, context, has_context)

# 可在 BAML Studio 查看:
# - 完整的 Prompt
# - LLM 响应
# - Token 使用
# - 响应时间
# - 成本估算
```

---

## 总结

### 核心优势

| 特性 | 当前方案 | BAML 方案 |
|------|---------|-----------|
| 类型安全 | ❌ 字典，运行时错误 | ✅ 强类型，编译时检查 |
| Prompt 管理 | ❌ 硬编码在代码中 | ✅ 独立文件，版本控制 |
| 模型切换 | ❌ 需要写适配器 | ✅ 一行配置切换 |
| 结构化输出 | ❌ 手动解析 | ✅ 自动解析验证 |
| 测试 | ❌ 无系统测试 | ✅ 内置测试框架 |
| 可观测性 | ❌ 需自己实现 | ✅ 自动追踪监控 |
| 开发体验 | ⚠️ 一般 | ✅ IDE 支持，自动完成 |

### 实施建议

1. **阶段 1（1-2 天）**：安装 BAML，创建基础配置
2. **阶段 2（2-3 天）**：迁移核心 Prompt 到 BAML
3. **阶段 3（2-3 天）**：集成到 Agent 和 API
4. **阶段 4（1-2 天）**：添加测试和监控
5. **阶段 5（持续）**：优化 Prompt，添加新功能

### 资源链接

- [BAML 官方文档](https://docs.boundaryml.com)
- [BAML GitHub](https://github.com/BoundaryML/baml)
- [BAML Playground](https://playground.boundaryml.com)
- [示例项目](https://github.com/BoundaryML/baml-examples)

---

**准备好开始了吗？让我知道是否需要帮助实施！** 🚀
