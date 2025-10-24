# 使用 uv 管理项目

本项目使用 [uv](https://github.com/astral-sh/uv) 作为 Python 包管理器，提供更快速、更可靠的依赖管理。

## 为什么使用 uv？

- ⚡ **超快速度**: 比 pip 快 10-100 倍
- 🔒 **可靠性**: 使用 lock 文件确保依赖一致性
- 🎯 **简单易用**: 自动管理虚拟环境
- 🆕 **现代化**: 支持最新的 Python 打包标准

## 安装 uv

### Linux/Mac

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Windows

```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 使用 pip（备选方案）

```bash
pip install uv
```

## 快速开始

### 1. 克隆或进入项目目录

```bash
cd agent_demo
```

### 2. 同步依赖（首次运行）

```bash
uv sync
```

这个命令会：
- 自动创建 `.venv` 虚拟环境
- 安装 `pyproject.toml` 中的所有依赖
- 生成 `uv.lock` 锁文件

### 3. 运行命令

使用 `uv run` 运行 Python 命令，无需手动激活虚拟环境：

```bash
# 加载文档
uv run python cli.py load

# 启动服务
uv run python main.py

# 交互式查询
uv run python cli.py query
```

## 常用 uv 命令

### 依赖管理

```bash
# 同步依赖（安装/更新）
uv sync

# 添加新依赖
uv add package-name

# 添加开发依赖
uv add --dev package-name

# 移除依赖
uv remove package-name

# 更新所有依赖
uv sync --upgrade
```

### 虚拟环境

```bash
# 创建虚拟环境
uv venv

# 创建指定 Python 版本的虚拟环境
uv venv --python 3.11

# 删除虚拟环境
rm -rf .venv
```

### 运行命令

```bash
# 运行 Python 脚本
uv run python script.py

# 运行项目中定义的脚本
uv run ai-agent status
uv run ai-agent-server

# 运行任意命令
uv run <command>
```

### 查看信息

```bash
# 查看已安装的包
uv pip list

# 查看依赖树
uv pip show package-name
```

## 项目配置

项目的依赖和配置在 `pyproject.toml` 中定义：

```toml
[project]
name = "ai-agent-kb"
version = "1.0.0"
dependencies = [
    "fastapi>=0.104.1",
    "openai>=1.3.0",
    # ... 其他依赖
]

[project.scripts]
ai-agent = "cli:main"
ai-agent-server = "main:start_server"
```

## 与传统方式对比

### 传统方式（pip + venv）

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 安装依赖
pip install -r requirements.txt

# 运行命令
python cli.py load
```

### uv 方式

```bash
# 一步搞定：创建环境 + 安装依赖
uv sync

# 运行命令（无需激活）
uv run python cli.py load
```

## 兼容性

项目同时提供了 `requirements.txt` 和 `pyproject.toml`，你可以选择：

### 使用 uv（推荐）

```bash
uv sync
uv run python cli.py load
```

### 使用传统 pip

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python cli.py load
```

## 常见问题

### Q: 如何在 CI/CD 中使用 uv？

```yaml
# GitHub Actions 示例
- name: Install uv
  run: curl -LsSf https://astral.sh/uv/install.sh | sh

- name: Install dependencies
  run: uv sync

- name: Run tests
  run: uv run pytest
```

### Q: uv.lock 文件要提交到 Git 吗？

是的，`uv.lock` 应该提交到版本控制，它确保所有人使用相同的依赖版本。

### Q: 如何在不同 Python 版本下测试？

```bash
# 创建 Python 3.11 环境
uv venv --python 3.11

# 同步依赖
uv sync

# 运行测试
uv run python cli.py status
```

### Q: 如何将现有项目迁移到 uv？

1. 安装 uv
2. 创建 `pyproject.toml`（或使用本项目的）
3. 运行 `uv sync`
4. 将命令改为 `uv run python ...`

## 更多资源

- [uv 官方文档](https://github.com/astral-sh/uv)
- [Python 打包指南](https://packaging.python.org/)
- [pyproject.toml 规范](https://packaging.python.org/en/latest/specifications/pyproject-toml/)

## 📚 相关文档

- **[项目 README](../README.md)** - 完整项目文档
- **[快速入门](QUICKSTART.md)** - 快速开始指南
- **[迁移说明](UV_MIGRATION.md)** - 从 pip 迁移到 uv
- **[项目总结](PROJECT_SUMMARY.md)** - 项目架构概览

## 快捷启动

我们提供了启动脚本，自动检查并使用 uv：

```bash
# Linux/Mac
./start.sh

# Windows
start.bat
```

启动脚本会：
1. 检查 uv 是否安装
2. 创建虚拟环境（如果不存在）
3. 同步依赖
4. 提供交互式菜单

尽情享受 uv 带来的速度提升吧！🚀
