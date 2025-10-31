# BAML 集成说明

## 📋 概述

本项目现已准备好集成 **BAML** (Basically A Made-up Language)，这是一个专门为 LLM 交互设计的领域特定语言（DSL）。

## 🎯 为什么选择 BAML？

### 核心优势

| 特性 | 当前实现 | 使用 BAML 后 |
|------|----------|--------------|
| **类型安全** | ❌ 字典返回，运行时错误 | ✅ 强类型，编译时检查 |
| **Prompt 管理** | ❌ 硬编码在 Python 代码 | ✅ 独立 .baml 文件管理 |
| **模型切换** | ❌ 需要实现适配器 | ✅ 一行配置切换 |
| **结构化输出** | ❌ 手动解析 JSON | ✅ 自动解析验证 |
| **测试** | ❌ 无系统测试机制 | ✅ 内置测试框架 |
| **监控** | ❌ 需自己实现 | ✅ 自动追踪和监控 |

### 代码对比示例

**当前方式：**
```python
# 返回字典，类型不安全
result = agent.chat(query)
answer = result["answer"]  # 可能 KeyError
confidence = result.get("confidence", 0)  # 没有类型提示
```

**BAML 方式：**
```python
# 类型安全的返回对象
result: ChatResponse = await baml_agent.chat(query)
print(result.answer)  # IDE 自动完成
print(result.confidence)  # 类型检查
print(result.category)  # 枚举类型
```

## 📂 项目结构

已创建的 BAML 相关文件：

```
llm-agent-in-action/
├── baml_src/                          # 🆕 BAML 配置目录
│   ├── clients.baml                   # LLM 客户端配置（OpenAI, Claude, Gemini）
│   ├── types.baml                     # 数据类型定义
│   └── functions/                     # Prompt 函数库
│       ├── rag.baml                   # RAG 问答函数
│       ├── analysis.baml              # 文档分析函数
│       └── reasoning.baml             # 推理函数
├── src/
│   └── core/
│       ├── agent.py                   # 原始 Agent（保持不变）
│       └── agent_baml.py              # 🆕 BAML Agent 实现
├── docs/
│   ├── BAML_INTEGRATION_PROPOSAL.md   # 🆕 详细集成方案（50+ 页）
│   ├── BAML_IMPLEMENTATION_GUIDE.md   # 🆕 实施指南
│   └── BAML_QUICK_REFERENCE.md        # 🆕 快速参考手册
└── README_BAML.md                     # 🆕 本文件
```

## 🚀 快速开始

### 1. 安装 BAML

```bash
pip install baml-py
```

### 2. 生成 Python 客户端

```bash
baml-cli generate
```

这会在项目根目录生成 `baml_client/` 目录，包含类型安全的 Python 代码。

### 3. 运行示例

```bash
# 运行 BAML Agent 示例
python -m src.core.agent_baml
```

### 4. 配置环境变量

确保 `.env` 文件包含：

```env
# OpenAI（必需）
OPENAI_API_KEY=your_key
OPENAI_API_BASE=https://api.openai.com/v1

# Anthropic Claude（可选）
ANTHROPIC_API_KEY=your_key

# Google Gemini（可选）
GEMINI_API_KEY=your_key
```

## 📖 文档导航

### 新手入门
👉 **[BAML_QUICK_REFERENCE.md](docs/BAML_QUICK_REFERENCE.md)** - 3 分钟快速上手

### 深入了解
👉 **[BAML_INTEGRATION_PROPOSAL.md](docs/BAML_INTEGRATION_PROPOSAL.md)** - 详细方案说明
   - BAML 简介和核心概念
   - 当前项目痛点分析
   - BAML 解决方案
   - 代码示例对比
   - 架构设计

### 实施指南
👉 **[BAML_IMPLEMENTATION_GUIDE.md](docs/BAML_IMPLEMENTATION_GUIDE.md)** - 分步实施
   - 安装和配置
   - 集成到现有项目
   - CLI 和 API 集成
   - 测试和监控
   - 常见问题

## 💡 主要特性

### 1. 类型安全的数据结构

```baml
// baml_src/types.baml
class ChatResponse {
  answer string @description("AI 的回答内容")
  confidence float @description("置信度，0-1之间")
  has_context bool @description("是否基于知识库回答")
  sources string[] @description("引用的文档来源")
  category QuestionCategory @description("问题分类")
}

enum QuestionCategory {
  Technical
  General
  Personal
  Unknown
}
```

### 2. 模块化的 Prompt 管理

```baml
// baml_src/functions/rag.baml
function RAGChat(
  query: string,
  context: string,
  has_context: bool
) -> ChatResponse {
  client GPT4
  prompt #"
    你是一个专业的AI助手。
    
    {% if has_context %}
    文档内容：{{ context }}
    {% endif %}
    
    用户问题：{{ query }}
    
    {{ ctx.output_format }}
  "#
}
```

### 3. 多 LLM 支持

```baml
// baml_src/clients.baml
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

// 切换模型只需改一行代码
function Chat(...) -> Answer {
  client Claude  // 改成 GPT4 或 Gemini
  prompt #"..."#
}
```

### 4. 内置测试框架

```baml
// 测试 Prompt 效果
test "Basic RAG with context" {
  functions [RAGChat]
  args {
    query "什么是机器学习？"
    context "机器学习是..."
    has_context true
  }
  assert {
    output.answer is string
    output.confidence >= 0.5
  }
}
```

运行测试：
```bash
baml test
```

## 🔧 使用示例

### 基础用法

```python
from baml_client import b
from baml_client.types import ChatResponse
import asyncio

async def main():
    # 调用 BAML 函数
    response: ChatResponse = await b.RAGChat(
        query="什么是人工智能？",
        context="人工智能是计算机科学的一个分支...",
        has_context=True
    )
    
    # 类型安全的访问
    print(f"回答: {response.answer}")
    print(f"置信度: {response.confidence}")
    print(f"分类: {response.category}")
    
    for source in response.sources:
        print(f"来源: {source}")

asyncio.run(main())
```

### 集成到现有 Agent

```python
from src.core.agent_baml import BAMLAgent
from src.services.vector_store import VectorStore
from src.core.config import settings
import asyncio

async def main():
    vector_store = VectorStore(settings.vector_db_path)
    agent = BAMLAgent(vector_store)
    
    # 使用 BAML Agent
    result = await agent.chat("Python 的优势是什么？")
    print(result)

asyncio.run(main())
```

## 🎨 BAML 功能展示

### 已实现的函数

1. **RAG 问答**
   - `RAGChat` - 基于知识库的问答
   - `SimpleRAGQuery` - 简化版问答
   - `MultiTurnChat` - 多轮对话

2. **文档分析**
   - `AnalyzeDocument` - 深度文档分析（摘要、实体、情感）
   - `SummarizeDocument` - 文档摘要
   - `ExtractKeywords` - 关键词提取

3. **推理功能**
   - `StepByStepReasoning` - 逐步推理
   - `DecomposeQuestion` - 问题分解
   - `VerifyAnswer` - 答案验证

## 🔍 监控和调试

### BAML Studio

```bash
# 启动可视化调试界面
baml studio
```

在浏览器中查看：
- 所有 LLM 调用记录
- 完整的 Prompt 和响应
- Token 使用量统计
- 响应时间分析
- 成本估算

### 日志记录

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# BAML 会自动记录所有调用详情
response = await b.RAGChat(query, context, True)
```

## 🚦 集成策略

### 阶段 1：并行运行（当前）
- ✅ BAML 文件已创建
- ✅ BAML Agent 已实现
- ⬜ 两个系统并行运行
- ⬜ 对比测试效果

### 阶段 2：部分迁移
- ⬜ 新功能优先使用 BAML
- ⬜ 核心功能逐步迁移
- ⬜ 保持向后兼容

### 阶段 3：完全迁移
- ⬜ 所有功能使用 BAML
- ⬜ 移除旧的适配器代码
- ⬜ 优化和性能调优

## 📊 性能对比

| 指标 | 当前实现 | BAML 实现 |
|------|----------|-----------|
| 类型检查 | 运行时 | 编译时 |
| Prompt 修改 | 改代码+重启 | 改配置+重新生成 |
| 模型切换 | 修改多处代码 | 一行配置 |
| 错误定位 | 困难 | 精确 |
| 开发效率 | 中 | 高 |
| 维护成本 | 高 | 低 |

## 🛠️ 常用命令

```bash
# 生成 Python 客户端
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

## 📚 学习资源

- 📖 [BAML 官方文档](https://docs.boundaryml.com)
- 🎮 [在线 Playground](https://playground.boundaryml.com)
- 💻 [GitHub 仓库](https://github.com/BoundaryML/baml)
- 💬 [Discord 社区](https://discord.gg/boundaryml)
- 📹 [视频教程](https://youtube.com/@boundaryml)

## ❓ 常见问题

### Q: BAML 会影响现有功能吗？
**A:** 不会。BAML 是一个独立的新模块，与现有代码并行运行。

### Q: 需要重写所有代码吗？
**A:** 不需要。可以渐进式迁移，先用于新功能，逐步替换旧代码。

### Q: BAML 有性能开销吗？
**A:** 几乎没有。BAML 只做类型转换和验证，开销 < 1ms。

### Q: 支持哪些 LLM？
**A:** OpenAI、Anthropic、Google、Ollama 等主流提供商。

### Q: 如何调试 Prompt？
**A:** 使用 `baml studio` 查看完整的 Prompt 和响应。

## 🎯 下一步行动

1. **阅读文档**
   ```bash
   # 3分钟快速入门
   cat docs/BAML_QUICK_REFERENCE.md
   ```

2. **安装 BAML**
   ```bash
   pip install baml-py
   ```

3. **生成客户端**
   ```bash
   baml-cli generate
   ```

4. **运行示例**
   ```bash
   python -m src.core.agent_baml
   ```

5. **查看调试界面**
   ```bash
   baml studio
   ```

## 🤝 贡献

欢迎提交 PR 和 Issue！如果你在集成过程中遇到问题，请：

1. 查看 `docs/BAML_IMPLEMENTATION_GUIDE.md` 中的常见问题
2. 使用 `baml-cli --help` 查看帮助
3. 在项目中提 Issue

## 📄 许可证

本项目采用 MIT 许可证。BAML 本身也是开源的。

---

**准备好体验类型安全的 LLM 编程了吗？开始使用 BAML！** 🚀

更多信息请查看：
- [详细集成方案](docs/BAML_INTEGRATION_PROPOSAL.md)
- [实施指南](docs/BAML_IMPLEMENTATION_GUIDE.md)
- [快速参考](docs/BAML_QUICK_REFERENCE.md)
