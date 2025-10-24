#!/bin/bash

# AI Agent 快速启动脚本

echo "======================================"
echo "AI Agent 知识库问答系统"
echo "======================================"
echo

# 检查 uv 是否安装
if ! command -v uv &> /dev/null; then
    echo "❌ 错误: 未安装 uv"
    echo ""
    echo "请先安装 uv:"
    echo "  curl -LsSf https://astral.sh/uv/install.sh | sh"
    echo ""
    echo "或者访问: https://github.com/astral-sh/uv"
    exit 1
fi

# 检查并创建虚拟环境
if [ ! -d ".venv" ]; then
    echo "创建虚拟环境..."
    uv venv
    echo "✓ 虚拟环境已创建"
    echo
fi

# 同步依赖
echo "检查并安装依赖..."
uv sync
echo "✓ 依赖已同步"
echo

# 检查配置文件
if [ ! -f ".env" ]; then
    echo "警告: .env 文件不存在"
    echo "请复制 .env.example 为 .env 并配置 OpenAI API Key"
    echo
    echo "cp .env.example .env"
    echo
    read -p "按回车键继续（将使用示例配置）..."
    cp .env.example .env
fi

# 检查是否存在 knowledge_base 目录
if [ ! -d "knowledge_base" ]; then
    echo "警告: knowledge_base 目录不存在，正在创建..."
    mkdir knowledge_base
    echo "请将文档放入 knowledge_base 目录后重新运行"
fi

# 显示菜单
echo "请选择操作:"
echo "1. 加载文档到向量数据库"
echo "2. 启动 API 服务"
echo "3. 启动命令行交互模式"
echo "4. 查看系统状态"
echo "5. 运行测试"
echo "0. 退出"
echo

read -p "请输入选项 (0-5): " choice

case $choice in
    1)
        echo
        echo "加载文档..."
        uv run python run.py load
        ;;
    2)
        echo
        echo "启动 API 服务..."
        echo "访问 http://localhost:8000/docs 查看 API 文档"
        echo
        uv run python server.py
        ;;
    3)
        echo
        echo "启动命令行交互模式..."
        echo "输入 'quit' 或 'exit' 退出"
        echo
        uv run python run.py query
        ;;
    4)
        echo
        uv run python run.py status
        ;;
    5)
        echo
        echo "运行测试..."
        echo "注意: 请确保 API 服务正在运行"
        echo
        uv run python tests/test_api.py
        ;;
    0)
        echo "再见！"
        exit 0
        ;;
    *)
        echo "无效的选项"
        exit 1
        ;;
esac
