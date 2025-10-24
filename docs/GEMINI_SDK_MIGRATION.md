# 迁移到新的 google-genai SDK

## 概述

本项目已从旧的 `google-generativeai` SDK 迁移到新的 `google-genai` SDK。新SDK提供了更好的开发体验和更统一的API设计。

## 主要变化

### 1. 依赖更新

**之前 (旧SDK):**
```toml
"google-generativeai>=0.8.5"
```

**现在 (新SDK):**
```toml
"google-genai>=1.0.0"
```

### 2. 导入方式

**之前:**
```python
import google.generativeai as genai
genai.configure(api_key=api_key)
```

**现在:**
```python
from google import genai
from google.genai import types

client = genai.Client(api_key=api_key)
```

### 3. 单条消息生成

**之前:**
```python
model = genai.GenerativeModel('gemini-1.5-flash')
response = model.generate_content("Hello")
```

**现在:**
```python
client = genai.Client(api_key=api_key)
response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents="Hello"
)
```

### 4. 多轮对话

**之前:**
```python
model = genai.GenerativeModel('gemini-1.5-flash')
chat = model.start_chat(history=[...])
response = chat.send_message("Hi")
```

**现在:**
```python
client = genai.Client(api_key=api_key)
chat = client.chats.create(model='gemini-2.5-flash')
response = chat.send_message("Hi")
```

### 5. System Instruction

**之前:**
```python
model = genai.GenerativeModel(
    'gemini-1.5-flash',
    system_instruction="You are a helpful assistant"
)
```

**现在:**
```python
config = types.GenerateContentConfig(
    system_instruction="You are a helpful assistant"
)
client.models.generate_content(
    model='gemini-2.5-flash',
    contents="Hello",
    config=config
)
```

### 6. 配置参数

**之前:**
```python
generation_config = genai.types.GenerationConfig(
    temperature=0.7,
    max_output_tokens=2000
)
```

**现在:**
```python
config = types.GenerateContentConfig(
    temperature=0.7,
    max_output_tokens=2000
)
```

## 新SDK的优势

### ✅ 统一的客户端架构
- 所有操作通过中央 `Client` 对象
- 更好的凭据和配置管理
- 清晰的API命名空间 (`models`, `chats`, `files` 等)

### ✅ 更简洁的多轮对话API
- 自动管理对话历史
- 无需手动构建历史记录数组
- 更直观的 `chats.create()` API

### ✅ 更好的类型提示
- 使用 `types.GenerateContentConfig`
- 更清晰的参数定义
- 更好的IDE支持

### ✅ 最新模型支持
- `gemini-2.5-flash` (最新推荐)
- 更好的性能和质量

## 可用模型

| 模型 | 特点 | 推荐用途 |
|------|------|----------|
| `gemini-2.5-flash` ⭐ | 最新最快 | **默认推荐** |
| `gemini-1.5-flash` | 快速经济 | 日常任务 |
| `gemini-1.5-flash-8b` | 轻量级 | 简单任务 |
| `gemini-1.5-pro` | 最强大 | 复杂任务、长文档 |

## 迁移步骤

### 1. 更新依赖
```bash
# 使用 uv
uv sync

# 或使用 pip
pip install --upgrade google-genai
pip uninstall google-generativeai
```

### 2. 更新代码
代码已自动迁移到新SDK，主要变化在 `src/core/llm_adapter.py`

### 3. 测试
```bash
# 设置API Key
export GEMINI_API_KEY="your-api-key"

# 运行测试
uv run python test_gemini_new_sdk.py
```

## 使用示例

### 基本用法
```python
from src.core.llm_adapter import GeminiAdapter

adapter = GeminiAdapter(
    api_key="your-api-key",
    model="gemini-2.5-flash"
)

messages = [
    {"role": "user", "content": "你好"}
]

response = adapter.chat(messages)
print(response)
```

### 带 System Instruction
```python
messages = [
    {"role": "system", "content": "你是一个Python专家。"},
    {"role": "user", "content": "什么是装饰器?"}
]

response = adapter.chat(messages)
```

### 多轮对话
```python
messages = [
    {"role": "user", "content": "我叫张三。"},
    {"role": "assistant", "content": "你好，张三！"},
    {"role": "user", "content": "我叫什么名字?"}
]

response = adapter.chat(messages)
# 输出: "你叫张三。"
```

### 自定义参数
```python
response = adapter.chat(
    messages,
    temperature=0.9,      # 更有创意
    max_tokens=1000       # 限制长度
)
```

## 常见问题

### Q: 旧的 API 还能用吗?
A: 旧的 `google-generativeai` 仍然可用，但建议迁移到新SDK以获得最佳体验和最新功能。

### Q: 需要修改现有代码吗?
A: 如果你使用的是 `LLMAdapter`，不需要修改。适配器已经处理了所有兼容性问题。

### Q: 新SDK的性能如何?
A: 新SDK性能更好，尤其是 `gemini-2.5-flash` 模型，速度更快、质量更高。

### Q: 如何获取API Key?
A: 访问 [Google AI Studio](https://aistudio.google.com/app/apikey) 免费获取。

## 参考资源

- [官方快速入门](https://ai.google.dev/gemini-api/docs/quickstart?hl=zh-cn)
- [迁移指南](https://ai.google.dev/gemini-api/docs/migrate?hl=zh-cn)
- [API参考](https://ai.google.dev/api)
- [GitHub Cookbook](https://github.com/google-gemini/cookbook)

## 更新日志

### 2025-10-24
- ✅ 迁移到 `google-genai` 1.0.0+
- ✅ 更新 `GeminiAdapter` 实现
- ✅ 默认模型改为 `gemini-2.5-flash`
- ✅ 采用新的 Client 架构
- ✅ 简化多轮对话实现
- ✅ 添加完整测试套件
