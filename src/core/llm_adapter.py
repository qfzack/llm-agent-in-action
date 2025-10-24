"""LLM适配器系统，支持多种LLM提供商"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any
import json

# OpenAI
from openai import OpenAI

# Gemini (新SDK)
try:
    from google import genai
    from google.genai import types
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
    
    def __init__(self, api_key: str, model: str = "gemini-2.5-flash"):
        if not GEMINI_AVAILABLE:
            raise ImportError("google-genai包未安装,请运行: pip install google-genai")
        
        # 创建客户端
        self.client = genai.Client(api_key=api_key)
        self.model_name = model
    
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """调用Gemini API

        支持的模型:
        - gemini-2.5-flash (推荐,最新最快)
        - gemini-1.5-flash (快速且经济)
        - gemini-1.5-flash-8b (更轻量)
        - gemini-1.5-pro (最强大,支持长上下文)
        """
        try:
            # 分离system消息和对话消息
            system_messages = []
            chat_messages = []
            
            for message in messages:
                if message['role'] == 'system':
                    system_messages.append(message['content'])
                else:
                    chat_messages.append(message)
            
            # 构建system_instruction
            system_instruction = "\n".join(system_messages) if system_messages else None
            
            # 配置生成参数
            config = types.GenerateContentConfig(
                temperature=kwargs.get('temperature', 0.7),
                max_output_tokens=kwargs.get('max_tokens', 2000),
                system_instruction=system_instruction
            )
            
            # 处理对话历史
            if not chat_messages:
                raise ValueError("至少需要一条对话消息")
            
            # 如果只有一条用户消息,直接使用generate_content
            if len(chat_messages) == 1 and chat_messages[0]['role'] == 'user':
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=chat_messages[0]['content'],
                    config=config
                )
                return response.text
            
            # 多轮对话: 使用新的chats API
            chat = self.client.chats.create(
                model=self.model_name,
                config=config
            )
            
            # 发送历史消息(除了最后一条)
            for msg in chat_messages[:-1]:
                if msg['role'] == 'user':
                    chat.send_message(msg['content'])
                # assistant消息会自动记录在历史中,无需手动发送
            
            # 发送最后一条消息并获取响应
            response = chat.send_message(chat_messages[-1]['content'])
            return response.text
        
        except Exception as e:
            raise Exception(f"Gemini API调用失败: {str(e)}")
    
    def get_model_name(self) -> str:
        return f"gemini/{self.model_name}"

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
                model=kwargs.get('model_name', 'gemini-2.5-flash')
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