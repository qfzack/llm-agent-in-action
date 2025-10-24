@echo off
chcp 65001 >nul
REM AI Agent 快速启动脚本 (Windows)

echo ======================================
echo AI Agent 知识库问答系统
echo ======================================
echo.

REM 检查 uv 是否安装
where uv >nul 2>nul
if errorlevel 1 (
    echo ❌ 错误: 未安装 uv
    echo.
    echo 请先安装 uv:
    echo   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
    echo.
    echo 或者访问: https://github.com/astral-sh/uv
    pause
    exit /b 1
)

REM 检查并创建虚拟环境
if not exist ".venv" (
    echo 创建虚拟环境...
    uv venv
    echo ✓ 虚拟环境已创建
    echo.
)

REM 同步依赖
echo 检查并安装依赖...
uv sync
echo ✓ 依赖已同步
echo.

REM 检查配置文件
if not exist ".env" (
    echo 警告: .env 文件不存在
    echo 请复制 .env.example 为 .env 并配置 OpenAI API Key
    echo.
    echo copy .env.example .env
    echo.
    pause
    copy .env.example .env
)

REM 检查是否存在 knowledge_base 目录
if not exist "knowledge_base" (
    echo 警告: knowledge_base 目录不存在，正在创建...
    mkdir knowledge_base
    echo 请将文档放入 knowledge_base 目录后重新运行
)

REM 显示菜单
echo 请选择操作:
echo 1. 加载文档到向量数据库
echo 2. 启动 API 服务
echo 3. 启动命令行交互模式
echo 4. 查看系统状态
echo 5. 运行测试
echo 0. 退出
echo.

set /p choice="请输入选项 (0-5): "

if "%choice%"=="1" (
    echo.
    echo 加载文档...
    uv run python run.py load
    pause
)

if "%choice%"=="2" (
    echo.
    echo 启动 API 服务...
    echo 访问 http://localhost:8000/docs 查看 API 文档
    echo.
    uv run python server.py
)

if "%choice%"=="3" (
    echo.
    echo 启动命令行交互模式...
    echo 输入 'quit' 或 'exit' 退出
    echo.
    uv run python run.py query
)

if "%choice%"=="4" (
    echo.
    uv run python run.py status
    pause
)

if "%choice%"=="5" (
    echo.
    echo 运行测试...
    echo 注意: 请确保 API 服务正在运行
    echo.
    uv run python tests\test_api.py
    pause
)

if "%choice%"=="0" (
    echo 再见！
    exit /b 0
)
