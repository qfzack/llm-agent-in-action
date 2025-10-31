// 推理和规划相关函数

// 逐步推理
function StepByStepReasoning(
  question: string,
  context: string
) -> ReasoningResult {
  client GPT4
  prompt #"
    请使用逐步推理的方式回答以下问题。
    
    背景信息：
    {{ context }}
    
    问题：{{ question }}
    
    请按照以下步骤进行推理：
    1. 首先，识别需要什么信息
    2. 然后，从背景中提取相关事实
    3. 应用逻辑推理
    4. 得出结论
    
    请提供详细的推理过程和最终答案。
    
    {{ ctx.output_format }}
  "#
}

// 问题分解
function DecomposeQuestion(
  complex_question: string
) -> string[] {
  client GPT4
  prompt #"
    请将以下复杂问题分解为一系列简单的子问题。
    
    复杂问题：{{ complex_question }}
    
    要求：
    - 每个子问题应该独立且可回答
    - 按逻辑顺序排列
    - 3-5个子问题
    
    返回子问题列表，每行一个。
  "#
}

// 答案验证
function VerifyAnswer(
  question: string,
  answer: string,
  context: string
) -> string {
  client GPT4
  prompt #"
    请验证以下答案是否正确且符合上下文。
    
    问题：{{ question }}
    答案：{{ answer }}
    上下文：{{ context }}
    
    请评估：
    1. 答案的准确性
    2. 是否与上下文一致
    3. 是否完整回答了问题
    4. 改进建议（如果需要）
    
    提供详细的验证报告。
  "#
}
