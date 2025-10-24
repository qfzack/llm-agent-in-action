#!/usr/bin/env python3
"""LLM切换工具"""

import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.config import settings
from src.core.llm_adapter import LLMFactory
import os
import argparse


def show_current_llm():
    """显示当前LLM配置"""
    print("=== 当前LLM配置 ===")
    print(f"提供商: {settings.llm_provider}")
    print(f"模型: {settings.model_name}")
    
    try:
        adapter = LLMFactory.create_adapter(
            provider=settings.llm_provider,
            openai_api_key=settings.openai_api_key,
            openai_api_base=settings.openai_api_base,
            gemini_api_key=settings.gemini_api_key,
            github_token=settings.github_token,
            model_name=settings.model_name
        )
        print(f"状态: ✓ 配置正确")
        print(f"完整模型名: {adapter.get_model_name()}")
    except Exception as e:
        print(f"状态: ✗ 配置错误 - {e}")


def list_providers():
    """列出可用的LLM提供商"""
    print("=== 可用的LLM提供商 ===")
    providers = LLMFactory.get_available_providers()
    
    for provider in providers:
        status = "✓" if provider in providers else "✗"
        print(f"{status} {provider}")
    
    print("\n=== 模型建议 ===")
    print("OpenAI:")
    print("  - gpt-3.5-turbo (推荐，性价比高)")
    print("  - gpt-4 (更强性能)")
    print("  - gpt-4-turbo")
    
    print("\nGemini:")
    print("  - gemini-pro (推荐)")
    print("  - gemini-pro-vision (支持图像)")
    
    print("\nCopilot:")
    print("  - 目前通过VS Code扩展提供")


def switch_llm(provider: str, model: str = None):
    """切换LLM提供商"""
    provider = provider.lower()
    
    # 验证提供商
    available_providers = LLMFactory.get_available_providers()
    if provider not in available_providers:
        print(f"错误: 不支持的提供商 '{provider}'")
        print(f"可用提供商: {', '.join(available_providers)}")
        return False
    
    # 设置默认模型
    if not model:
        model_defaults = {
            'openai': 'gpt-3.5-turbo',
            'gemini': 'gemini-pro',
            'copilot': 'copilot'
        }
        model = model_defaults.get(provider, 'default')
    
    # 更新环境文件
    env_file = Path(__file__).parent.parent / '.env'
    
    try:
        # 读取现有配置
        lines = []
        if env_file.exists():
            with open(env_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        
        # 更新或添加配置
        updated_llm_provider = False
        updated_model_name = False
        
        for i, line in enumerate(lines):
            if line.startswith('LLM_PROVIDER='):
                lines[i] = f'LLM_PROVIDER={provider}\n'
                updated_llm_provider = True
            elif line.startswith('MODEL_NAME='):
                lines[i] = f'MODEL_NAME={model}\n'
                updated_model_name = True
        
        # 如果没找到配置行，添加它们
        if not updated_llm_provider:
            lines.append(f'LLM_PROVIDER={provider}\n')
        if not updated_model_name:
            lines.append(f'MODEL_NAME={model}\n')
        
        # 写回文件
        with open(env_file, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        
        print(f"✓ 已切换到 {provider} / {model}")
        
        # 验证配置
        print("\n验证新配置...")
        # 重新加载配置
        os.environ['LLM_PROVIDER'] = provider
        os.environ['MODEL_NAME'] = model
        
        try:
            adapter = LLMFactory.create_adapter(
                provider=provider,
                openai_api_key=settings.openai_api_key,
                openai_api_base=settings.openai_api_base,
                gemini_api_key=settings.gemini_api_key,
                github_token=settings.github_token,
                model_name=model
            )
            print(f"✓ 新配置验证成功: {adapter.get_model_name()}")
            return True
        except Exception as e:
            print(f"✗ 新配置验证失败: {e}")
            return False
            
    except Exception as e:
        print(f"错误: 无法更新配置文件 - {e}")
        return False


def test_llm():
    """测试当前LLM配置"""
    print("=== 测试LLM连接 ===")
    
    try:
        adapter = LLMFactory.create_adapter(
            provider=settings.llm_provider,
            openai_api_key=settings.openai_api_key,
            openai_api_base=settings.openai_api_base,
            gemini_api_key=settings.gemini_api_key,
            github_token=settings.github_token,
            model_name=settings.model_name
        )
        
        # 发送测试消息
        test_messages = [
            {"role": "user", "content": "请说'你好，我是AI助手'"}
        ]
        
        print("发送测试消息...")
        response = adapter.chat(test_messages)
        print(f"✓ LLM响应: {response}")
        return True
        
    except Exception as e:
        print(f"✗ LLM测试失败: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="LLM切换工具")
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # status命令
    subparsers.add_parser('status', help='显示当前LLM配置')
    
    # list命令
    subparsers.add_parser('list', help='列出可用的LLM提供商')
    
    # switch命令
    switch_parser = subparsers.add_parser('switch', help='切换LLM提供商')
    switch_parser.add_argument('provider', help='LLM提供商 (openai/gemini/copilot)')
    switch_parser.add_argument('--model', help='模型名称 (可选)')
    
    # test命令
    subparsers.add_parser('test', help='测试LLM连接')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        if args.command == 'status':
            show_current_llm()
        elif args.command == 'list':
            list_providers()
        elif args.command == 'switch':
            switch_llm(args.provider, args.model)
        elif args.command == 'test':
            test_llm()
            
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()