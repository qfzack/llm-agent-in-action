#!/bin/bash
# BAML 安装和配置脚本

set -e

echo "================================"
echo "  BAML 集成设置脚本"
echo "================================"
echo ""

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 检查是否在项目根目录
if [ ! -f "pyproject.toml" ] && [ ! -f "requirements.txt" ]; then
    echo -e "${RED}错误: 请在项目根目录运行此脚本${NC}"
    exit 1
fi

echo "步骤 1/4: 检查 Python 环境..."
if ! command -v python &> /dev/null; then
    echo -e "${RED}错误: 未找到 Python${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Python 已安装: $(python --version)${NC}"
echo ""

echo "步骤 2/4: 安装 BAML..."
if pip show baml-py &> /dev/null; then
    echo -e "${YELLOW}BAML 已安装，跳过${NC}"
else
    echo "正在安装 baml-py..."
    pip install baml-py
    echo -e "${GREEN}✓ BAML 安装完成${NC}"
fi
echo ""

echo "步骤 3/4: 验证 BAML CLI..."
if command -v baml-cli &> /dev/null; then
    echo -e "${GREEN}✓ BAML CLI 可用: $(baml-cli --version)${NC}"
else
    echo -e "${RED}错误: BAML CLI 未找到${NC}"
    echo "请尝试重新安装: pip install --upgrade baml-py"
    exit 1
fi
echo ""

echo "步骤 4/4: 生成 Python 客户端..."
if [ -d "baml_client" ]; then
    echo -e "${YELLOW}baml_client/ 目录已存在${NC}"
    read -p "是否重新生成? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf baml_client
        echo "正在生成客户端代码..."
        baml-cli generate
        echo -e "${GREEN}✓ 客户端代码已重新生成${NC}"
    else
        echo "跳过生成"
    fi
else
    echo "正在生成客户端代码..."
    baml-cli generate
    echo -e "${GREEN}✓ 客户端代码生成完成${NC}"
fi
echo ""

echo "================================"
echo -e "${GREEN}✓ BAML 设置完成！${NC}"
echo "================================"
echo ""
echo "下一步："
echo "1. 查看生成的代码: ls -la baml_client/"
echo "2. 运行示例: python -m src.core.agent_baml"
echo "3. 启动调试界面: baml studio"
echo ""
echo "文档："
echo "- 快速参考: docs/BAML_QUICK_REFERENCE.md"
echo "- 实施指南: docs/BAML_IMPLEMENTATION_GUIDE.md"
echo "- 详细方案: docs/BAML_INTEGRATION_PROPOSAL.md"
echo ""
