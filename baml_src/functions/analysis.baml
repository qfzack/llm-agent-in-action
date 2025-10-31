// 文档分析相关函数

// 文档深度分析
function AnalyzeDocument(
  text: string
) -> DocumentAnalysis {
  client GPT4
  prompt #"
    请分析以下文档并提取结构化信息。
    
    文档内容：
    {{ text }}
    
    请提供全面的分析，包括：
    1. 简洁摘要（不超过200字）
    2. 3-5个关键要点
    3. 主题标签
    4. 整体情感倾向（Positive/Negative/Neutral）
    5. 命名实体及其类型
    6. 复杂度级别（Easy/Medium/Hard）
    
    {{ ctx.output_format }}
  "#
}

// 文档摘要
function SummarizeDocument(
  text: string,
  max_length: int
) -> string {
  client GPT35Turbo
  prompt #"
    请总结以下文档，摘要长度不超过 {{ max_length }} 字。
    
    文档：
    {{ text }}
    
    要求：
    - 保留关键信息
    - 简洁明了
    - 中文输出
  "#
}

// 关键词提取
function ExtractKeywords(
  text: string,
  num_keywords: int
) -> string[] {
  client GPT35Turbo
  prompt #"
    从以下文档中提取 {{ num_keywords }} 个最重要的关键词。
    
    文档：
    {{ text }}
    
    只返回关键词列表，每行一个。
  "#
}
