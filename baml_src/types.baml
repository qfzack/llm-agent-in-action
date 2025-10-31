// BAML 类型定义
// 定义结构化的输入输出类型，确保类型安全

// 聊天响应类型
class ChatResponse {
  answer string @description("AI 的回答内容")
  confidence float @description("置信度，0-1之间")
  has_context bool @description("是否基于知识库回答")
  sources string[] @description("引用的文档来源")
  category QuestionCategory @description("问题分类")
}

// 问题分类枚举
enum QuestionCategory {
  Technical @description("技术问题")
  General @description("通用问题")
  Personal @description("个人问题")
  Unknown @description("未知类型")
}

// 文档引用
class DocumentReference {
  filename string @description("文档文件名")
  content string @description("文档内容片段")
  score float @description("相关性分数")
}

// 文档分析结果
class DocumentAnalysis {
  summary string @description("文档摘要，不超过200字")
  key_points string[] @description("3-5个关键要点")
  topics string[] @description("主要主题标签")
  sentiment Sentiment @description("情感倾向")
  entities Entity[] @description("命名实体")
  complexity Complexity @description("复杂度级别")
}

// 情感枚举
enum Sentiment {
  Positive @description("积极")
  Negative @description("消极")
  Neutral @description("中性")
}

// 复杂度枚举
enum Complexity {
  Easy @description("简单")
  Medium @description("中等")
  Hard @description("困难")
}

// 命名实体
class Entity {
  name string @description("实体名称")
  type EntityType @description("实体类型")
  mentions int @description("提及次数")
}

// 实体类型枚举
enum EntityType {
  Person @description("人物")
  Organization @description("组织")
  Location @description("地点")
  Technology @description("技术")
  Concept @description("概念")
}

// 推理步骤
class ReasoningStep {
  step_number int @description("步骤编号")
  description string @description("步骤描述")
  conclusion string @description("该步骤的结论")
}

// 推理结果
class ReasoningResult {
  steps ReasoningStep[] @description("推理步骤列表")
  final_answer string @description("最终答案")
  confidence float @description("置信度")
}
