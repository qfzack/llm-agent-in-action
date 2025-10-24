# LLM 切换指南

这个项目现在支持多种 LLM 提供商，包括 OpenAI、Google Gemini 和 GitHub Copilot。

## 🚀 快速开始

### 1. 安装新依赖

```bash
# 安装 Google Gemini 支持
uv add google-generativeai
```

### 2. 配置 API 密钥

编辑 `.env` 文件，添加你需要的 API 密钥：

```bash
# LLM提供商配置
LLM_PROVIDER=openai  # 或 gemini, copilot

# OpenAI 配置
OPENAI_API_KEY=your_openai_api_key

# Google Gemini 配置  
GEMINI_API_KEY=your_gemini_api_key

# GitHub Token (用于 Copilot)
GITHUB_TOKEN=your_github_token

# 模型配置
MODEL_NAME=gpt-3.5-turbo
```

## 📋 支持的 LLM 提供商

### 1. OpenAI
- **模型**: `gpt-3.5-turbo`, `gpt-4`, `gpt-4-turbo`
- **API 密钥**: 从 [OpenAI Platform](https://platform.openai.com/) 获取
- **配置**:
  ```bash
  LLM_PROVIDER=openai
  MODEL_NAME=gpt-3.5-turbo
  OPENAI_API_KEY=sk-...
  ```

### 2. Google Gemini
- **模型**: `gemini-pro`, `gemini-pro-vision`
- **API 密钥**: 从 [Google AI Studio](https://aistudio.google.com/) 获取
- **配置**:
  ```bash
  LLM_PROVIDER=gemini
  MODEL_NAME=gemini-pro
  GEMINI_API_KEY=your_api_key
  ```

### 3. GitHub Copilot
- **说明**: 目前主要通过 VS Code 扩展提供，REST API 有限
- **配置**:
  ```bash
  LLM_PROVIDER=copilot
  GITHUB_TOKEN=ghp_...
  ```

## 🛠️ 使用 LLM 切换工具

我们提供了一个便捷的命令行工具来管理 LLM 配置：

### 查看当前配置
```bash
uv run python scripts/switch_llm.py status
```

### 列出可用提供商
```bash
uv run python scripts/switch_llm.py list
```

### 切换到不同的 LLM
```bash
# 切换到 Gemini
uv run python scripts/switch_llm.py switch gemini

# 切换到 OpenAI 并指定模型
uv run python scripts/switch_llm.py switch openai --model gpt-4

# 切换到 Copilot
uv run python scripts/switch_llm.py switch copilot
```

### 测试 LLM 连接
```bash
uv run python scripts/switch_llm.py test
```

## 🔧 手动配置

你也可以直接修改 `.env` 文件来切换 LLM：

1. **切换到 Gemini**:
   ```bash
   LLM_PROVIDER=gemini
   MODEL_NAME=gemini-pro
   GEMINI_API_KEY=your_gemini_api_key
   ```

2. **切换回 OpenAI**:
   ```bash
   LLM_PROVIDER=openai
   MODEL_NAME=gpt-3.5-turbo
   OPENAI_API_KEY=your_openai_api_key
   ```

## 📝 使用示例

### 1. 使用 OpenAI GPT-4
```bash
# 切换到 GPT-4
uv run python scripts/switch_llm.py switch openai --model gpt-4

# 启动问答系统
uv run python run.py query
```

### 2. 使用 Google Gemini
```bash
# 切换到 Gemini
uv run python scripts/switch_llm.py switch gemini

# 测试连接
uv run python scripts/switch_llm.py test

# 启动 API 服务
uv run python server.py
```

## 🚨 获取 API 密钥

### OpenAI API 密钥
1. 访问 [OpenAI Platform](https://platform.openai.com/)
2. 登录并进入 "API Keys" 页面
3. 点击 "Create new secret key"
4. 复制密钥并添加到 `.env` 文件

### Google Gemini API 密钥
1. 访问 [Google AI Studio](https://aistudio.google.com/)
2. 使用 Google 账户登录
3. 进入 "Get API key" 页面
4. 创建新的 API 密钥
5. 复制密钥并添加到 `.env` 文件

### GitHub Token
1. 访问 [GitHub Settings](https://github.com/settings/tokens)
2. 点击 "Generate new token (classic)"
3. 选择适当的权限范围
4. 生成并复制 token

## ⚠️ 注意事项

1. **API 费用**: 不同提供商的定价不同，使用前请检查相关费用
2. **速率限制**: 每个提供商都有不同的速率限制
3. **模型能力**: 不同模型在性能和功能上可能有差异
4. **网络连接**: 确保能够访问相应的 API 端点

## 🔍 故障排查

### 问题: API 密钥无效
**解决方案**:
```bash
# 检查配置
uv run python scripts/switch_llm.py status

# 测试连接
uv run python scripts/switch_llm.py test
```

### 问题: 切换后不生效
**解决方案**:
1. 重启应用程序
2. 检查 `.env` 文件是否正确保存
3. 确认 API 密钥格式正确

### 问题: Gemini API 不可用
**解决方案**:
```bash
# 安装 Gemini 依赖
uv add google-generativeai

# 检查 API 密钥
uv run python scripts/switch_llm.py status
```

## 🎯 最佳实践

1. **开发环境**: 使用 `gpt-3.5-turbo` 或 `gemini-pro` (成本较低)
2. **生产环境**: 根据需求选择 `gpt-4` 或其他高性能模型
3. **备份方案**: 配置多个提供商的 API 密钥，以便快速切换
4. **监控使用**: 定期检查 API 使用量和费用

现在你可以轻松地在不同的 LLM 提供商之间切换，享受各种 AI 模型的强大功能！