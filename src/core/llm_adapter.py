"""LLM适配器系统，支持多种LLM提供商"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any
import json

# OpenAI
from openai import OpenAI

# Gemini
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

# GitHub Copilot (通过GitHub API)
import requests


class LLMAdapter(ABC):
    """LLM适配器基类"""
    
    @abstractmethod
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """发送聊天消息并返回回复"""
        pass
    
    @abstractmethod
    def get_model_name(self) -> str:
        """获取模型名称"""
        pass


class OpenAIAdapter(LLMAdapter):
    """OpenAI适配器"""
    
    def __init__(self, api_key: str, base_url: str = "https://api.openai.com/v1", model: str = "gpt-3.5-turbo"):
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model = model
    
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """调用OpenAI Chat API"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=kwargs.get('temperature', 0.7),
                max_tokens=kwargs.get('max_tokens', 2000)
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"OpenAI API调用失败: {str(e)}")
    
    def get_model_name(self) -> str:
        return f"openai/{self.model}"


class GeminiAdapter(LLMAdapter):
    """Google Gemini适配器"""
    
    def __init__(self, api_key: str, model: str = "gemini-pro"):
        if not GEMINI_AVAILABLE:
            raise ImportError("google-generativeai包未安装，请运行: pip install google-generativeai")
        
        genai.configure(api_key=api_key)
        self.model_name = model
        self.model = genai.GenerativeModel(model)
    
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """调用Gemini API"""
        try:
            # 将消息格式转换为Gemini格式
            # Gemini需要将对话历史组合成一个提示
            conversation = []
            for message in messages:
                role = message['role']
                content = message['content']
                
                if role == 'user':
                    conversation.append(f"用户: {content}")
                elif role == 'assistant':
                    conversation.append(f"助手: {content}")
                elif role == 'system':
                    conversation.append(f"系统: {content}")
            
            # 使用最后一个用户消息作为主要输入
            prompt = "\n".join(conversation)
            
            # 配置生成参数
            generation_config = genai.types.GenerationConfig(
                temperature=kwargs.get('temperature', 0.7),
                max_output_tokens=kwargs.get('max_tokens', 2000),
            )
            
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config
            )
            
            return response.text
        
        except Exception as e:
            raise Exception(f"Gemini API调用失败: {str(e)}")
    
    def get_model_name(self) -> str:
        return f"gemini/{self.model_name}"


class CopilotAdapter(LLMAdapter):
    """GitHub Copilot适配器"""
    
    def __init__(self, github_token: str):
        self.github_token = github_token
        self.api_base = "https://api.github.com"
        # 注意: 这是一个示例实现，实际的GitHub Copilot API可能有所不同
        # 目前GitHub Copilot主要通过VS Code扩展提供，没有公开的REST API
    
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """
        注意: GitHub Copilot目前主要通过VS Code扩展提供服务
        这里提供一个概念性的实现，实际使用需要GitHub官方API支持
        """
        # 这里使用GitHub的其他AI服务作为替代方案
        # 或者可以集成其他兼容OpenAI格式的服务
        
        # 临时实现: 使用GitHub API获取代码建议
        # 实际应用中可能需要使用其他方法
        try:
            headers = {
                "Authorization": f"token {self.github_token}",
                "Accept": "application/vnd.github.v3+json"
            }
            
            # 这里只是一个示例，实际的Copilot API调用需要GitHub官方支持
            # 目前返回一个说明信息
            return "GitHub Copilot目前主要通过VS Code扩展提供服务。如需使用AI代码助手，建议使用OpenAI或Gemini。"
        
        except Exception as e:
            raise Exception(f"GitHub Copilot API调用失败: {str(e)}")
    
    def get_model_name(self) -> str:
        return "github/copilot"


class LLMFactory:
    """LLM工厂类，用于创建不同的LLM适配器"""
    
    @staticmethod
    def create_adapter(provider: str, **kwargs) -> LLMAdapter:
        """
        创建LLM适配器
        
        Args:
            provider: 提供商 ('openai', 'gemini', 'copilot')
            **kwargs: 配置参数
        
        Returns:
            LLM适配器实例
        """
        provider = provider.lower()
        
        if provider == "openai":
            return OpenAIAdapter(
                api_key=kwargs.get('openai_api_key'),
                base_url=kwargs.get('openai_api_base', 'https://api.openai.com/v1'),
                model=kwargs.get('model_name', 'gpt-3.5-turbo')
            )
        
        elif provider == "gemini":
            return GeminiAdapter(
                api_key=kwargs.get('gemini_api_key'),
                model=kwargs.get('model_name', 'gemini-pro')
            )
        
        elif provider == "copilot":
            return CopilotAdapter(
                github_token=kwargs.get('github_token')
            )
        
        else:
            raise ValueError(f"不支持的LLM提供商: {provider}。支持的提供商: openai, gemini, copilot")
    
    @staticmethod
    def get_available_providers() -> List[str]:
        """获取可用的LLM提供商列表"""
        providers = ["openai"]
        
        if GEMINI_AVAILABLE:
            providers.append("gemini")
        
        providers.append("copilot")  # 概念性支持
        
        return providers