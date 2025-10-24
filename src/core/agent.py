"""AI Agent核心模块"""
from typing import List, Dict

from ..core.config import settings
from ..core.llm_adapter import LLMFactory, LLMAdapter
from ..services.vector_store import VectorStore


class AIAgent:
    """AI Agent，基于RAG实现知识库问答"""
    
    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store
        self.top_k = settings.top_k
        
        # 初始化LLM适配器
        self.llm_adapter = LLMFactory.create_adapter(
            provider=settings.llm_provider,
            openai_api_key=settings.openai_api_key,
            openai_api_base=settings.openai_api_base,
            gemini_api_key=settings.gemini_api_key,
            github_token=settings.github_token,
            model_name=settings.model_name
        )
        
        print(f"✓ 已初始化LLM: {self.llm_adapter.get_model_name()}")
    
    def build_context(self, query: str) -> str:
        """从向量数据库检索相关文档构建上下文"""
        # 检索相关文档
        results = self.vector_store.query(query, top_k=self.top_k)
        
        if not results:
            return ""
        
        # 构建上下文
        context_parts = []
        for i, result in enumerate(results, 1):
            filename = result['metadata'].get('filename', '未知')
            content = result['content']
            context_parts.append(f"[文档{i}: {filename}]\n{content}")
        
        return "\n\n".join(context_parts)
    
    def generate_prompt(self, query: str, context: str) -> str:
        """生成提示词"""
        if context:
            prompt = f"""你是一个专业的AI助手，负责根据提供的文档知识库回答用户的问题。

请基于以下文档内容回答用户的问题。如果文档中没有相关信息，请明确告诉用户。

文档内容：
{context}

用户问题：{query}

请提供准确、详细的回答："""
        else:
            prompt = f"""你是一个专业的AI助手。用户的问题是：{query}

注意：当前知识库中没有找到相关文档，请根据你的通用知识回答，并提醒用户这不是基于特定文档的回答。"""
        
        return prompt
    
    def chat(self, query: str, conversation_history: List[Dict[str, str]] = None) -> Dict[str, str]:
        """
        与AI进行对话
        
        Args:
            query: 用户问题
            conversation_history: 对话历史，格式为 [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]
        
        Returns:
            包含回答和检索到的文档的字典
        """
        # 检索相关文档
        context = self.build_context(query)
        
        # 生成提示词
        prompt = self.generate_prompt(query, context)
        
        # 构建消息列表
        messages = []
        
        # 添加历史对话（如果有）
        if conversation_history:
            messages.extend(conversation_history[-10:])  # 只保留最近10轮对话
        
        # 添加当前问题
        messages.append({"role": "user", "content": prompt})
        
        try:
            # 调用LLM API
            answer = self.llm_adapter.chat(
                messages=messages,
                temperature=0.7,
                max_tokens=2000
            )
            
            # 检索用到的文档
            retrieved_docs = self.vector_store.query(query, top_k=self.top_k)
            
            return {
                "answer": answer,
                "retrieved_docs": retrieved_docs,
                "has_context": bool(context)
            }
        
        except Exception as e:
            return {
                "answer": f"抱歉，处理您的问题时发生错误: {str(e)}",
                "retrieved_docs": [],
                "has_context": False,
                "error": str(e)
            }
    
    def simple_query(self, query: str) -> str:
        """简单查询，只返回答案文本"""
        result = self.chat(query)
        return result["answer"]
