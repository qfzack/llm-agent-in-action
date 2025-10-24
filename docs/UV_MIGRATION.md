# 🎉 项目已升级为 uv 管理！

## ✅ 完成的更新

### 1. 添加了 pyproject.toml
- 现代化的 Python 项目配置
- 定义了所有项目依赖
- 包含项目元数据和脚本命令

### 2. 更新了启动脚本
- `start.sh` (Linux/Mac)
- `start.bat` (Windows)
- 自动检测 uv 是否安装
- 自动创建虚拟环境和同步依赖

### 3. 更新了文档
- `README.md` - 添加了 uv 使用说明
- `QUICKSTART.md` - 更新了安装步骤
- `UV_GUIDE.md` - 全新的 uv 详细指南

### 4. 更新了 .gitignore
- 添加 `.venv/` 忽略规则
- 添加 `uv.lock` 和 `.python-version`

## 🚀 如何开始使用

### 方式 1: 使用启动脚本（推荐）

```bash
# Linux/Mac
./start.sh

# Windows
start.bat
```

启动脚本会自动：
- 检查 uv 是否安装（未安装会提示）
- 创建虚拟环境
- 同步所有依赖
- 提供交互式菜单

### 方式 2: 手动使用 uv

```bash
# 1. 安装 uv（如果未安装）
curl -LsSf https://astral.sh/uv/install.sh | sh  # Linux/Mac
# 或
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"  # Windows

# 2. 同步依赖
uv sync

# 3. 运行命令
uv run python cli.py load
uv run python main.py
```

## 📋 常用命令对比

| 操作 | 旧方式 (pip) | 新方式 (uv) |
|------|-------------|------------|
| 创建环境 | `python -m venv venv` | `uv venv` (自动) |
| 激活环境 | `source venv/bin/activate` | 不需要 |
| 安装依赖 | `pip install -r requirements.txt` | `uv sync` |
| 运行脚本 | `python cli.py load` | `uv run python cli.py load` |
| 添加依赖 | 手动编辑 requirements.txt + `pip install` | `uv add package-name` |

## 🎯 uv 的优势

- ⚡ **速度**: 比 pip 快 10-100 倍
- 🔒 **可靠**: lock 文件确保依赖一致性
- 🎯 **简单**: 无需手动激活虚拟环境
- 🆕 **现代**: 支持最新 Python 打包标准

## 📚 相关文档

- **完整文档**: `README.md`
- **快速入门**: `QUICKSTART.md`
- **uv 指南**: `UV_GUIDE.md`
- **项目总结**: `PROJECT_SUMMARY.md`

## 🔄 向后兼容

项目仍然保留了 `requirements.txt`，你仍然可以使用传统方式：

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python cli.py load
```

但我们强烈推荐使用 uv，享受更快的速度和更好的体验！

## 📚 更多文档

- **[完整文档](../README.md)** - 项目完整说明
- **[快速入门](QUICKSTART.md)** - 5分钟快速开始
- **[uv 指南](UV_GUIDE.md)** - uv 详细使用说明
- **[项目总结](PROJECT_SUMMARY.md)** - 架构和功能概览

## 📝 使用示例

### 加载文档并启动服务

```bash
# 使用 uv（推荐）
uv sync
uv run python cli.py load
uv run python main.py

# 或使用启动脚本
./start.sh
```

### 交互式问答

```bash
uv run python cli.py query
```

### 测试 API

```bash
# 终端 1: 启动服务
uv run python main.py

# 终端 2: 运行测试
uv run python test_api.py
```

## 🛠️ 开发工作流

```bash
# 1. 添加新依赖
uv add requests

# 2. 开发依赖
uv add --dev pytest

# 3. 运行脚本
uv run python your_script.py

# 4. 更新依赖
uv sync --upgrade
```

## 💡 提示

1. **首次使用**: 运行 `./start.sh` 或 `start.bat` 最简单
2. **日常开发**: 使用 `uv run python ...` 运行命令
3. **添加依赖**: 使用 `uv add package-name` 而不是手动编辑文件
4. **CI/CD**: 在 CI 中使用 `uv sync` 安装依赖更快

## 🎊 升级完成！

项目现在使用现代化的 uv 包管理器，享受更快、更可靠的开发体验！

有任何问题请查看 `UV_GUIDE.md` 或项目文档。

---

**Happy Coding with uv! 🚀**
