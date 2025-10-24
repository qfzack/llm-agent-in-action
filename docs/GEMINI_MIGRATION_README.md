# ✅ 已迁移到 google-genai 新SDK

本项目已成功从 `google-generativeai` 迁移到新的 `google-genai` SDK！

## 🎯 主要变化

- ✅ 使用新的 `google-genai` 包 (v1.0.0+)
- ✅ 采用统一的 Client 架构
- ✅ 默认模型升级到 `gemini-2.5-flash`
- ✅ 简化的多轮对话API
- ✅ 更好的类型提示和IDE支持

## 🚀 快速开始

### 1. 安装依赖
```bash
uv sync
```

### 2. 使用示例
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

### 3. 运行测试
```bash
export GEMINI_API_KEY="your-api-key"
uv run python test_gemini_new_sdk.py
```

## 📚 文档

- [完整迁移指南](./GEMINI_SDK_MIGRATION.md)
- [新旧SDK对比](./GEMINI_SDK_COMPARISON.md)

## 💡 关键改进

### 之前 (旧SDK)
```python
import google.generativeai as genai
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')
response = model.generate_content("Hello")
```

### 现在 (新SDK) ✨
```python
from google import genai
client = genai.Client(api_key=api_key)
response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents="Hello"
)
```

更简洁、更统一、更强大！🎉
