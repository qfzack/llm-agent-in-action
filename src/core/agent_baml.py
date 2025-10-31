"""使用 BAML 的 AI Agent 实现

这个模块展示了如何使用 BAML 来改进 AI Agent：
1. 类型安全的输入输出
2. 模块化的 Prompt 管理
3. 轻松切换 LLM 模型
4. 结构化的响应解析
"""

from typing import List, Dict, Optional
import asyncio

# 注意：这些导入需要先运行 `baml-cli generate` 生成客户端代码
# from baml_client import b
# from baml_client.types import ChatResponse, DocumentAnalysis, ReasoningResult

from ..services.vector_store import VectorStore
from ..core.config import settings


class BAMLAgent:
    """基于 BAML 的 AI Agent
    
    相比原始实现的优势：
    1. 类型安全：所有输入输出都有明确的类型
    2. Prompt 分离：Prompt 在 .baml 文件中管理，不在代码里
    3. 易于测试：可以使用 BAML 的测试框架
    4. 多模型支持：切换模型只需改配置，不需要改代码
    """
    
    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store
        self.top_k = settings.top_k
        print(f"✓ 已初始化 BAML Agent")
    
    async def chat(self, query: str, conversation_history: Optional[List[Dict[str, str]]] = None):
        """
        与 AI 进行对话（使用 BAML）
        
        Args:
            query: 用户问题
            conversation_history: 对话历史（可选）
        
        Returns:
            ChatResponse: 结构化的响应对象，包含：
                - answer: 答案文本
                - confidence: 置信度
                - has_context: 是否基于知识库
                - sources: 来源列表
                - category: 问题分类
        """
        # 1. 检索相关文档
        docs = self.vector_store.query(query, top_k=self.top_k)
        context = self._build_context(docs)
        has_context = bool(docs)
        
        try:
            # 2. 调用 BAML 函数
            # 注意：这需要先安装 BAML 并生成客户端
            """
            if conversation_history:
                # 使用多轮对话函数
                history_str = self._format_history(conversation_history)
                response = await b.MultiTurnChat(
                    query=query,
                    context=context,
                    conversation_history=history_str
                )
            else:
                # 使用基础 RAG 函数
                response = await b.RAGChat(
                    query=query,
                    context=context,
                    has_context=has_context
                )
            
            return response  # 类型安全的 ChatResponse 对象
            """
            
            # 临时返回（在安装 BAML 前）
            return {
                "answer": "BAML Agent 需要先安装 BAML 并生成客户端代码",
                "confidence": 0.0,
                "has_context": has_context,
                "sources": [doc['metadata'].get('filename', '') for doc in docs],
                "category": "Unknown",
                "note": "请运行: pip install baml-py && baml-cli generate"
            }
        
        except Exception as e:
            print(f"错误: {e}")
            return {
                "answer": f"处理问题时发生错误: {str(e)}",
                "confidence": 0.0,
                "has_context": False,
                "sources": [],
                "category": "Unknown",
                "error": str(e)
            }
    
    async def analyze_document(self, text: str):
        """
        分析文档并提取结构化信息
        
        Args:
            text: 文档文本
        
        Returns:
            DocumentAnalysis: 包含摘要、关键点、实体等
        """
        try:
            # response = await b.AnalyzeDocument(text=text)
            # return response
            
            # 临时返回
            return {
                "summary": "需要安装 BAML",
                "key_points": [],
                "topics": [],
                "sentiment": "Neutral",
                "entities": [],
                "complexity": "Unknown"
            }
        except Exception as e:
            print(f"分析文档时出错: {e}")
            return None
    
    async def reason_step_by_step(self, question: str, context: str):
        """
        使用逐步推理回答问题
        
        Args:
            question: 问题
            context: 背景信息
        
        Returns:
            ReasoningResult: 包含推理步骤和最终答案
        """
        try:
            # response = await b.StepByStepReasoning(
            #     question=question,
            #     context=context
            # )
            # return response
            
            # 临时返回
            return {
                "steps": [],
                "final_answer": "需要安装 BAML",
                "confidence": 0.0
            }
        except Exception as e:
            print(f"推理时出错: {e}")
            return None
    
    def _build_context(self, docs: List[Dict]) -> str:
        """构建上下文字符串"""
        if not docs:
            return ""
        
        context_parts = []
        for i, doc in enumerate(docs, 1):
            filename = doc['metadata'].get('filename', '未知')
            content = doc['content']
            context_parts.append(f"[文档{i}: {filename}]\n{content}")
        
        return "\n\n".join(context_parts)
    
    def _format_history(self, history: List[Dict[str, str]]) -> str:
        """格式化对话历史"""
        formatted = []
        for msg in history[-10:]:  # 只保留最近10轮
            role = msg.get('role', 'unknown')
            content = msg.get('content', '')
            if role == 'user':
                formatted.append(f"用户: {content}")
            elif role == 'assistant':
                formatted.append(f"助手: {content}")
        return "\n".join(formatted)


# 示例：如何使用 BAML Agent
async def example_usage():
    """使用示例"""
    from ..services.vector_store import VectorStore
    
    # 初始化
    vector_store = VectorStore(settings.vector_db_path)
    agent = BAMLAgent(vector_store)
    
    # 示例1：基础问答
    print("=== 示例1：基础问答 ===")
    response = await agent.chat("什么是机器学习？")
    print(f"回答: {response['answer']}")
    print(f"置信度: {response['confidence']}")
    print(f"分类: {response['category']}")
    
    # 示例2：多轮对话
    print("\n=== 示例2：多轮对话 ===")
    history = [
        {"role": "user", "content": "什么是Python？"},
        {"role": "assistant", "content": "Python是一种编程语言..."}
    ]
    response = await agent.chat("它有什么优点？", conversation_history=history)
    print(f"回答: {response['answer']}")
    
    # 示例3：文档分析
    print("\n=== 示例3：文档分析 ===")
    document_text = """
    机器学习是人工智能的一个分支，它使计算机能够从数据中学习并做出决策。
    主要类型包括监督学习、无监督学习和强化学习。
    """
    analysis = await agent.analyze_document(document_text)
    if analysis:
        print(f"摘要: {analysis['summary']}")
        print(f"情感: {analysis['sentiment']}")
    
    # 示例4：逐步推理
    print("\n=== 示例4：逐步推理 ===")
    reasoning = await agent.reason_step_by_step(
        question="为什么机器学习很重要？",
        context="机器学习可以从数据中发现模式，自动化决策过程。"
    )
    if reasoning:
        print(f"最终答案: {reasoning['final_answer']}")
        print(f"推理步骤数: {len(reasoning['steps'])}")


if __name__ == "__main__":
    asyncio.run(example_usage())
