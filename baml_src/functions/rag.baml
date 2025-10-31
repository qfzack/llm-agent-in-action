// RAG (Retrieval-Augmented Generation) 相关函数

// 基于知识库的问答
function RAGChat(
  query: string,
  context: string,
  has_context: bool
) -> ChatResponse {
  client GPT4
  prompt #"
    你是一个专业的AI助手，专门负责基于知识库进行问答。
    
    {% if has_context %}
    请根据以下文档内容回答用户的问题。
    如果文档中没有相关信息，请明确说明。
    
    文档内容：
    {{ context }}
    {% else %}
    注意：当前知识库中没有找到相关文档。
    请根据你的通用知识回答，并提醒用户这不是基于特定文档的回答。
    {% endif %}
    
    用户问题：{{ query }}
    
    请提供详细的回答，并包含：
    - 置信度（0-1之间的数值）
    - 引用的文档来源（如果适用）
    - 问题分类（Technical/General/Personal/Unknown）
    
    {{ ctx.output_format }}
  "#
}

// 简化版问答（只返回答案文本）
function SimpleRAGQuery(
  query: string,
  context: string
) -> string {
  client GPT35Turbo
  prompt #"
    基于以下文档内容回答问题：
    
    文档：{{ context }}
    问题：{{ query }}
    
    提供简洁准确的回答。
  "#
}

// 多轮对话
function MultiTurnChat(
  query: string,
  context: string,
  conversation_history: string
) -> ChatResponse {
  client GPT4
  prompt #"
    你是一个专业的AI助手。请根据对话历史和文档内容回答问题。
    
    对话历史：
    {{ conversation_history }}
    
    相关文档：
    {{ context }}
    
    当前问题：{{ query }}
    
    请提供连贯的回答，考虑对话上下文。
    
    {{ ctx.output_format }}
  "#
}
