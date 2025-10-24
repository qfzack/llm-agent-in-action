# Gemini SDK 新旧对比

## 快速对比

| 特性 | 旧SDK (google-generativeai) | 新SDK (google-genai) |
|------|---------------------------|---------------------|
| 包名 | `google-generativeai` | `google-genai` |
| 导入 | `import google.generativeai as genai` | `from google import genai` |
| 初始化 | `genai.configure(api_key=...)` | `client = genai.Client(api_key=...)` |
| 单条消息 | `model.generate_content(...)` | `client.models.generate_content(...)` |
| 多轮对话 | `model.start_chat(history=...)` | `client.chats.create(...)` |
| 配置 | `genai.types.GenerationConfig(...)` | `types.GenerateContentConfig(...)` |
| 默认模型 | `gemini-1.5-flash` | `gemini-2.5-flash` |

## 代码示例对比

### 单条消息生成

#### 旧SDK
```python
import google.generativeai as genai

genai.configure(api_key="your-api-key")
model = genai.GenerativeModel('gemini-1.5-flash')
response = model.generate_content("Hello")
print(response.text)
```

#### 新SDK ✅
```python
from google import genai

client = genai.Client(api_key="your-api-key")
response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents="Hello"
)
print(response.text)
```

### 多轮对话

#### 旧SDK
```python
import google.generativeai as genai

genai.configure(api_key="your-api-key")
model = genai.GenerativeModel('gemini-1.5-flash')

history = [
    {'role': 'user', 'parts': ['你好']},
    {'role': 'model', 'parts': ['你好！']}
]

chat = model.start_chat(history=history)
response = chat.send_message("再见")
print(response.text)
```

#### 新SDK ✅
```python
from google import genai

client = genai.Client(api_key="your-api-key")
chat = client.chats.create(model='gemini-2.5-flash')

chat.send_message("你好")
response = chat.send_message("再见")
print(response.text)
```

### System Instruction

#### 旧SDK
```python
model = genai.GenerativeModel(
    'gemini-1.5-flash',
    system_instruction="你是一个Python专家"
)
response = model.generate_content("什么是装饰器?")
```

#### 新SDK ✅
```python
from google.genai import types

config = types.GenerateContentConfig(
    system_instruction="你是一个Python专家"
)

response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents="什么是装饰器?",
    config=config
)
```

## 迁移清单

- [x] 更新 pyproject.toml 依赖
  - 移除: `google-generativeai>=0.8.5`
  - 添加: `google-genai>=1.0.0`
  
- [x] 更新导入语句
  - 从 `import google.generativeai as genai` 
  - 改为 `from google import genai`
  
- [x] 更新初始化方式
  - 从 `genai.configure(api_key=...)`
  - 改为 `client = genai.Client(api_key=...)`
  
- [x] 更新 API 调用
  - 单条消息: `client.models.generate_content(...)`
  - 多轮对话: `client.chats.create(...)`
  
- [x] 更新配置对象
  - 从 `genai.types.GenerationConfig`
  - 改为 `types.GenerateContentConfig`
  
- [x] 更新默认模型
  - 从 `gemini-1.5-flash`
  - 改为 `gemini-2.5-flash`

## 测试验证

运行测试确保迁移成功:

```bash
# 设置环境变量
export GEMINI_API_KEY="your-api-key"

# 运行测试
uv run python test_gemini_new_sdk.py
```

## 新SDK优势

1. **更统一的架构**: 通过 Client 对象集中管理
2. **更简洁的API**: 减少样板代码
3. **更好的类型提示**: IDE支持更完善
4. **最新模型**: 支持 gemini-2.5-flash
5. **自动历史管理**: 多轮对话更简单

## 参考链接

- [官方迁移指南](https://ai.google.dev/gemini-api/docs/migrate?hl=zh-cn)
- [新SDK文档](https://ai.google.dev/gemini-api/docs/quickstart?hl=zh-cn)
- [完整迁移文档](./GEMINI_SDK_MIGRATION.md)
