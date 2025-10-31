# BAML 快速参考手册

## 一句话总结

**BAML 让你的 LLM 代码类型安全、Prompt 模块化、模型可切换。**

---

## 核心优势速览

| 特性 | 当前项目 | 使用 BAML 后 |
|------|---------|-------------|
| 🔒 **类型安全** | ❌ 字典，运行时错误 | ✅ 强类型，编译时检查 |
| 📝 **Prompt 管理** | ❌ 硬编码在代码中 | ✅ 独立 .baml 文件 |
| 🔄 **切换模型** | ❌ 需要写适配器 | ✅ 一行配置 |
| 📊 **结构化输出** | ❌ 手动解析 | ✅ 自动解析验证 |
| ✅ **测试** | ❌ 无系统测试 | ✅ 内置测试框架 |
| 🔍 **监控** | ❌ 需自己实现 | ✅ 自动追踪 |

---

## 3 分钟快速上手

### 1. 安装（30 秒）

```bash
pip install baml-py
```

### 2. 定义（1 分钟）

**类型** (`types.baml`):
```baml
class Answer {
  text string
  confidence float
}
```

**函数** (`functions/chat.baml`):
```baml
function AskQuestion(question: string) -> Answer {
  client GPT4
  prompt #"Answer: {{ question }}"#
}
```

### 3. 使用（1 分钟）

```bash
# 生成客户端
baml-cli generate
```

```python
from baml_client import b

# 调用
answer = await b.AskQuestion("什么是 AI？")
print(answer.text)
print(answer.confidence)
```

---

## 关键代码对比

### 定义响应结构

<table>
<tr>
<th>原始方式</th>
<th>BAML 方式</th>
</tr>
<tr>
<td>

```python
# 返回字典，类型不安全
def chat(query):
    return {
        "answer": "...",
        "confidence": 0.8
    }

# 使用时容易出错
result = chat("问题")
print(result["answer"])  # 可能 KeyError
```

</td>
<td>

```baml
// types.baml
class ChatResponse {
  answer string
  confidence float
}

function Chat(query: string) 
  -> ChatResponse {
  // ...
}
```

```python
# 类型安全
result = await b.Chat("问题")
print(result.answer)  # IDE 自动完成
```

</td>
</tr>
</table>

### Prompt 管理

<table>
<tr>
<th>原始方式</th>
<th>BAML 方式</th>
</tr>
<tr>
<td>

```python
# Prompt 硬编码在代码中
def generate_prompt(query, context):
    prompt = f"""
    你是AI助手。
    
    上下文：{context}
    问题：{query}
    """
    return prompt

# 修改 Prompt 需要改代码
```

</td>
<td>

```baml
// rag.baml
function RAGChat(
  query: string, 
  context: string
) -> Answer {
  client GPT4
  prompt #"
    你是AI助手。
    
    上下文：{{ context }}
    问题：{{ query }}
  "#
}

// 修改 Prompt 只需编辑 .baml 文件
```

</td>
</tr>
</table>

### 切换模型

<table>
<tr>
<th>原始方式</th>
<th>BAML 方式</th>
</tr>
<tr>
<td>

```python
# 需要实现适配器
class OpenAIAdapter:
    def chat(self, messages):
        # OpenAI 特定代码
        pass

class ClaudeAdapter:
    def chat(self, messages):
        # Claude 特定代码
        pass

# 切换模型需要改很多代码
adapter = OpenAIAdapter()  # 改这里
```

</td>
<td>

```baml
// clients.baml
client GPT4 { provider openai }
client Claude { provider anthropic }

// functions/chat.baml
function Chat(...) -> Answer {
  client GPT4  // 改成 Claude 即可
  prompt #"..."#
}

// 或运行时切换
await b.Chat.with_client("Claude")(...)
```

</td>
</tr>
</table>

---

## 常用模式

### 模式 1：RAG 问答

```baml
class RAGResponse {
  answer string
  sources string[]
  confidence float
}

function RAGQuery(
  query: string,
  context: string
) -> RAGResponse {
  client GPT4
  prompt #"
    Based on: {{ context }}
    Question: {{ query }}
    
    {{ ctx.output_format }}
  "#
}
```

### 模式 2：结构化提取

```baml
class Person {
  name string
  age int
  occupation string
}

function ExtractPerson(text: string) -> Person {
  client GPT4
  prompt #"
    Extract person info from: {{ text }}
    {{ ctx.output_format }}
  "#
}
```

### 模式 3：分类

```baml
enum Category {
  Technical
  General
  Personal
}

function Classify(text: string) -> Category {
  client GPT35Turbo
  prompt #"Classify: {{ text }}"#
}
```

### 模式 4：多步推理

```baml
class ReasoningStep {
  step int
  reasoning string
}

class Reasoning {
  steps ReasoningStep[]
  conclusion string
}

function Reason(question: string) -> Reasoning {
  client GPT4
  prompt #"
    Think step by step: {{ question }}
    {{ ctx.output_format }}
  "#
}
```

---

## 常用命令

```bash
# 生成客户端
baml-cli generate

# 运行测试
baml test

# 启动可视化界面
baml studio

# 验证语法
baml validate

# 格式化代码
baml format
```

---

## 项目集成清单

- [x] 创建 `baml_src/` 目录
- [x] 定义 `clients.baml`（LLM 配置）
- [x] 定义 `types.baml`（数据类型）
- [x] 创建 `functions/*.baml`（Prompt 函数）
- [ ] 运行 `baml-cli generate`
- [ ] 创建 `agent_baml.py`（BAML Agent）
- [ ] 更新 `requirements.txt`
- [ ] 编写测试
- [ ] 集成到 API

---

## 调试技巧

### 查看实际 Prompt

```bash
baml studio
# 浏览器打开，查看所有调用记录
```

### 启用详细日志

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### 单元测试

```baml
test "basic" {
  functions [Chat]
  args { query "Hi" }
  assert {
    output.text is string
    output.confidence > 0
  }
}
```

---

## 性能优化

### 并行调用

```python
import asyncio

results = await asyncio.gather(
    b.Chat("问题1"),
    b.Chat("问题2"),
    b.Analyze(text)
)
```

### 流式输出

```python
async for chunk in b.Chat.stream("问题"):
    print(chunk, end="")
```

### 缓存

```baml
function Chat(query: string) -> Answer {
  client GPT4
  options {
    cache true
  }
  prompt #"..."#
}
```

---

## 错误处理

```python
from baml_client import b
from baml_client.errors import BAMLError

try:
    result = await b.Chat("问题")
except BAMLError as e:
    print(f"BAML 错误: {e}")
    # 使用备用方案
```

---

## 最佳实践

### ✅ DO

```baml
// 使用描述性名称
class UserProfile { ... }

// 添加文档注释
/// 分析文档内容
function AnalyzeDocument(...) { ... }

// 使用枚举避免魔法字符串
enum Status { Active Inactive }

// 组织文件结构
functions/
  rag/
  analysis/
  chat/
```

### ❌ DON'T

```baml
// 避免过于宽泛的类型
class Data {
  stuff string
}

// 避免过长的 Prompt（拆分成多个函数）
function DoEverything(...) { ... }

// 避免硬编码（使用 env 变量）
client GPT4 {
  options {
    api_key "sk-..."  // ❌ 不要这样
  }
}
```

---

## 资源链接

| 资源 | 链接 |
|------|------|
| 📚 官方文档 | https://docs.boundaryml.com |
| 🎮 Playground | https://playground.boundaryml.com |
| 💻 GitHub | https://github.com/BoundaryML/baml |
| 💬 Discord | https://discord.gg/boundaryml |
| 📹 视频教程 | https://youtube.com/@boundaryml |

---

## 下一步行动

### 今天

1. `pip install baml-py`
2. 查看 `baml_src/` 中的示例
3. 运行 `baml-cli generate`

### 本周

1. 为一个新功能使用 BAML
2. 编写测试
3. 使用 `baml studio` 调试

### 本月

1. 迁移核心功能到 BAML
2. 优化 Prompt
3. 添加新的 LLM 提供商

---

## 需要帮助？

```bash
# 查看帮助
baml-cli --help

# 查看示例
baml-cli examples

# 检查版本
baml-cli --version
```

或查看项目文档：
- `docs/BAML_INTEGRATION_PROPOSAL.md` - 详细方案
- `docs/BAML_IMPLEMENTATION_GUIDE.md` - 实施指南
- `src/core/agent_baml.py` - 代码示例

---

**Happy coding with BAML! 🚀**
