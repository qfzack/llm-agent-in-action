// BAML 客户端配置
// 定义多个 LLM 提供商，可以轻松切换

client GPT4 {
  provider openai
  options {
    model "gpt-4"
    api_key env.OPENAI_API_KEY
    base_url env.OPENAI_API_BASE
  }
}

client GPT35Turbo {
  provider openai
  options {
    model "gpt-3.5-turbo"
    api_key env.OPENAI_API_KEY
    base_url env.OPENAI_API_BASE
  }
}

client Claude {
  provider anthropic
  options {
    model "claude-3-sonnet-20240229"
    api_key env.ANTHROPIC_API_KEY
  }
}

client Gemini {
  provider google-ai
  options {
    model "gemini-pro"
    api_key env.GEMINI_API_KEY
  }
}
