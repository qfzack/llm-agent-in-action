# 测试指南

## 概述

本项目的测试系统已经优化，支持**自动服务器管理**，无需手动启动服务器即可运行测试。

## 快速开始

### 方式 1: 直接运行测试脚本（推荐）

```bash
# 自动启动服务器并运行所有测试
uv run python tests/test_api.py
```

**特点：**
- ✓ 自动检测服务器状态
- ✓ 服务器未运行时自动启动
- ✓ 测试完成后自动停止服务器
- ✓ 服务器已运行时复用现有服务器

### 方式 2: 使用启动脚本

```bash
bash scripts/start.sh
# 选择选项 5
```

**或者直接：**
```bash
echo "5" | bash scripts/start.sh
```

## 测试模式

### 1. 完整测试套件（自动管理服务器）

```bash
uv run python tests/test_api.py
```

**测试内容包括：**
1. 健康检查
2. 系统状态查询
3. 文档重新加载
4. 基础查询测试
5. 带对话历史的查询测试

### 2. 单独查询测试

```bash
# 需要服务器已在运行
uv run python tests/test_api.py query "你的问题"
```

### 3. 上传文件测试

```bash
# 需要服务器已在运行
uv run python tests/test_api.py upload /path/to/file.md
```

## 测试流程

### 自动服务器管理流程

```
开始测试
   ↓
检测服务器状态
   ↓
[未运行] ────→ 启动临时服务器
   ↓              ↓
[已运行] ←────── 等待就绪
   ↓
运行测试套件
   ↓
测试完成
   ↓
[临时服务器] → 自动停止服务器
   ↓
[现有服务器] → 保持运行
   ↓
退出
```

### 测试输出示例

```
============================================================
AI Agent 系统测试
============================================================

ℹ️  服务器未运行，将自动启动临时服务器
🚀 启动测试服务器...
⏳ 等待服务器就绪.... ✓
✓ 服务器已启动 (PID: 12345)

1. 测试健康检查...
   状态码: 200
   响应: {'message': 'AI Agent 知识库问答系统正在运行', ...}

2. 测试获取系统状态...
   状态码: 200
   文档数量: 95
   系统状态: running

...

============================================================
✓ 所有测试通过！
============================================================

🛑 停止测试服务器...
✓ 服务器已停止
```

## 技术实现

### 核心功能

1. **服务器检测** (`check_server_running()`)
   - 尝试连接 `http://localhost:8000/`
   - 2 秒超时检测
   - 返回服务器运行状态

2. **服务器启动** (`start_server()`)
   - 使用 `uv run python server.py` 启动
   - 后台进程运行
   - 最多等待 30 秒
   - 实时显示启动进度

3. **服务器停止** (`stop_server()`)
   - 优雅终止进程 (SIGTERM)
   - 5 秒超时后强制终止 (SIGKILL)
   - 清理进程资源

4. **智能服务器管理**
   - 检测现有服务器则复用
   - 未检测到则启动临时服务器
   - 临时服务器测试后自动清理
   - 现有服务器测试后保持运行

### 代码关键点

```python
# 检查服务器
server_was_running = check_server_running()

# 智能启动
if not server_was_running:
    server_process = start_server()
    
# 运行测试
try:
    run_tests()
finally:
    # 只停止我们启动的服务器
    if server_process:
        stop_server(server_process)
```

## 故障排除

### 问题 1: 服务器启动超时

**症状：**
```
⏳ 等待服务器就绪............................ ✗
❌ 服务器启动超时
```

**可能原因：**
- 端口 8000 被占用
- 依赖未安装
- Python 环境问题

**解决方案：**
```bash
# 检查端口占用
lsof -i :8000

# 同步依赖
uv sync

# 手动测试启动
uv run python server.py
```

### 问题 2: 测试连接失败

**症状：**
```
❌ 错误: 无法连接到服务器
```

**可能原因：**
- 服务器启动失败
- 防火墙阻止
- 网络配置问题

**解决方案：**
```bash
# 检查服务器日志
tail -f /tmp/ai-agent-server.log

# 测试本地连接
curl http://localhost:8000/
```

### 问题 3: 服务器未正确停止

**症状：**
测试后服务器进程仍在运行

**解决方案：**
```bash
# 查找并停止进程
lsof -ti:8000 | xargs kill -9

# 或使用脚本
pkill -f "python server.py"
```

## 最佳实践

### 1. 开发测试

```bash
# 方式 1: 完全自动化（推荐新手）
uv run python tests/test_api.py

# 方式 2: 手动控制（推荐开发调试）
# 终端 1
uv run python server.py

# 终端 2
uv run python tests/test_api.py query "测试问题"
```

### 2. CI/CD 集成

```yaml
# GitHub Actions 示例
- name: Run Tests
  run: |
    uv sync
    uv run python tests/test_api.py
```

### 3. 持续开发

如果需要频繁测试：
1. 保持服务器运行在一个终端
2. 在另一个终端运行单独的测试命令
3. 避免重复启动/停止服务器的开销

## 进阶用法

### 自定义测试

你可以直接导入测试函数使用：

```python
from tests.test_api import check_server_running, test_query

# 检查服务器
if check_server_running():
    test_query("自定义查询")
```

### 并行测试

目前测试是串行的，如需并行可考虑：
- 使用不同端口的多个服务器实例
- 引入 pytest-xdist 进行并行测试
- 使用 Docker 容器隔离

## 更新日志

### v1.1 (2025-10-24)

**新增功能：**
- ✓ 自动服务器启动/停止
- ✓ 服务器状态智能检测
- ✓ 优雅的进度显示
- ✓ 完善的错误处理
- ✓ 退出代码支持（CI/CD 友好）

**优化改进：**
- ✓ 测试输出更清晰（emoji + 格式化）
- ✓ 服务器启动超时从无限等待改为 30 秒
- ✓ 添加 KeyboardInterrupt 处理
- ✓ start.sh 选项 5 简化说明

### v1.0 (原始版本)

- 基础测试功能
- 需要手动启动服务器

## 相关文档

- [快速开始](./QUICKSTART.md)
- [项目架构](./ARCHITECTURE.md)
- [API 文档](../src/api/main.py)

## 支持

如有问题，请：
1. 查看本文档的故障排除部分
2. 检查项目 Issues
3. 提交新的 Issue

---

**贡献者欢迎！** 如果你有改进建议，欢迎提交 PR。
