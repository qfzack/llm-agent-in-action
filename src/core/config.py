"""配置管理模块"""
from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    """应用配置"""
    
    # LLM提供商配置 - 支持: openai, gemini, copilot
    llm_provider: str = "openai"
    
    # OpenAI配置
    openai_api_key: str = ""
    openai_api_base: str = "https://api.openai.com/v1"
    
    # Gemini配置
    gemini_api_key: str = ""
    
    # GitHub Copilot配置 (使用GitHub Copilot Chat API)
    github_token: str = ""
    
    # 模型配置
    model_name: str = "gpt-3.5-turbo"
    
    # 向量数据库配置
    vector_db_path: str = "./data/chroma_db"
    
    # 文档存储路径
    documents_path: str = "./knowledge_base"
    
    # 服务配置
    host: str = "0.0.0.0"
    port: int = 8000
    
    # 向量检索配置
    chunk_size: int = 1000
    chunk_overlap: int = 200
    top_k: int = 3
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# 创建全局配置实例
settings = Settings()

# 确保必要的目录存在
Path(settings.vector_db_path).parent.mkdir(parents=True, exist_ok=True)
Path(settings.documents_path).mkdir(parents=True, exist_ok=True)
