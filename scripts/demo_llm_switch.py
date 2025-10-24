#!/usr/bin/env python3
"""LLM切换演示脚本"""

import sys
from pathlib import Path
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.llm_adapter import LLMFactory


def demo_llm_switch():
    """演示LLM切换功能"""
    
    print("=== LLM切换演示 ===\n")
    
    # 测试消息
    test_messages = [
        {"role": "user", "content": "请用一句话介绍你自己"}
    ]
    
    # 演示不同的LLM
    configs = [
        {
            "name": "OpenAI GPT-3.5",
            "provider": "openai",
            "config": {
                "openai_api_key": os.getenv("OPENAI_API_KEY", ""),
                "openai_api_base": os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1"),
                "model_name": "gpt-3.5-turbo"
            }
        },
        {
            "name": "Google Gemini Pro", 
            "provider": "gemini",
            "config": {
                "gemini_api_key": os.getenv("GEMINI_API_KEY", ""),
                "model_name": "gemini-pro"
            }
        },
        {
            "name": "GitHub Copilot",
            "provider": "copilot", 
            "config": {
                "github_token": os.getenv("GITHUB_TOKEN", ""),
            }
        }
    ]
    
    for config in configs:
        print(f"🤖 测试 {config['name']} ...")
        
        try:
            # 创建适配器
            adapter = LLMFactory.create_adapter(
                provider=config['provider'],
                **config['config']
            )
            
            print(f"   模型: {adapter.get_model_name()}")
            
            # 检查API密钥
            if config['provider'] == 'openai' and not config['config']['openai_api_key']:
                print("   ⚠️  需要设置 OPENAI_API_KEY")
                print()
                continue
            elif config['provider'] == 'gemini' and not config['config']['gemini_api_key']:
                print("   ⚠️  需要设置 GEMINI_API_KEY") 
                print()
                continue
            elif config['provider'] == 'copilot' and not config['config']['github_token']:
                print("   ⚠️  需要设置 GITHUB_TOKEN")
                print()
                continue
            
            # 发送测试消息
            response = adapter.chat(test_messages, max_tokens=100)
            print(f"   💬 回复: {response[:100]}{'...' if len(response) > 100 else ''}")
            
        except Exception as e:
            print(f"   ❌ 错误: {e}")
        
        print()


if __name__ == "__main__":
    demo_llm_switch()