"""Python 客户端示例"""
import requests
from typing import List, Dict, Optional


class AIAgentClient:
    """AI Agent 客户端"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.conversation_history: List[Dict[str, str]] = []
    
    def query(self, question: str, use_history: bool = True) -> Dict:
        """
        发送查询请求
        
        Args:
            question: 问题
            use_history: 是否使用对话历史
        
        Returns:
            查询结果
        """
        payload = {
            "query": question
        }
        
        if use_history and self.conversation_history:
            payload["conversation_history"] = self.conversation_history
        
        response = requests.post(f"{self.base_url}/query", json=payload)
        response.raise_for_status()
        
        result = response.json()
        
        # 更新对话历史
        if use_history:
            self.conversation_history.append({"role": "user", "content": question})
            self.conversation_history.append({"role": "assistant", "content": result["answer"]})
        
        return result
    
    def upload_document(self, file_path: str) -> Dict:
        """
        上传文档
        
        Args:
            file_path: 文件路径
        
        Returns:
            上传结果
        """
        with open(file_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(f"{self.base_url}/upload", files=files)
        
        response.raise_for_status()
        return response.json()
    
    def reload_documents(self) -> Dict:
        """重新加载所有文档"""
        response = requests.post(f"{self.base_url}/reload")
        response.raise_for_status()
        return response.json()
    
    def get_status(self) -> Dict:
        """获取系统状态"""
        response = requests.get(f"{self.base_url}/status")
        response.raise_for_status()
        return response.json()
    
    def clear_database(self) -> Dict:
        """清空知识库"""
        response = requests.delete(f"{self.base_url}/clear")
        response.raise_for_status()
        return response.json()
    
    def clear_history(self):
        """清空对话历史"""
        self.conversation_history = []
    
    def chat_interactive(self):
        """交互式对话"""
        print("AI Agent 交互式对话")
        print("输入 'quit' 或 'exit' 退出")
        print("输入 'clear' 清空对话历史")
        print("输入 'status' 查看系统状态")
        print()
        
        while True:
            try:
                question = input("您: ").strip()
                
                if not question:
                    continue
                
                if question.lower() in ['quit', 'exit', 'q']:
                    print("再见！")
                    break
                
                if question.lower() == 'clear':
                    self.clear_history()
                    print("对话历史已清空\n")
                    continue
                
                if question.lower() == 'status':
                    status = self.get_status()
                    print(f"\n系统状态: {status['status']}")
                    print(f"文档块数: {status['document_count']}\n")
                    continue
                
                # 查询
                result = self.query(question)
                
                print(f"\nAI: {result['answer']}")
                
                # 显示相关文档
                if result['retrieved_docs']:
                    print("\n相关文档:")
                    for i, doc in enumerate(result['retrieved_docs'], 1):
                        filename = doc['metadata'].get('filename', '未知')
                        print(f"  {i}. {filename}")
                
                print()
            
            except KeyboardInterrupt:
                print("\n\n再见！")
                break
            except Exception as e:
                print(f"\n错误: {e}\n")


def example_usage():
    """使用示例"""
    
    # 创建客户端
    client = AIAgentClient()
    
    print("=== AI Agent Python 客户端示例 ===\n")
    
    try:
        # 1. 检查系统状态
        print("1. 检查系统状态...")
        status = client.get_status()
        print(f"   系统状态: {status['status']}")
        print(f"   文档数量: {status['document_count']}")
        print()
        
        # 2. 单次查询
        print("2. 单次查询...")
        result = client.query("这个系统有什么功能？", use_history=False)
        print(f"   问题: 这个系统有什么功能？")
        print(f"   回答: {result['answer'][:150]}...")
        print()
        
        # 3. 带历史的对话
        print("3. 多轮对话...")
        client.clear_history()
        
        result1 = client.query("什么是 RAG？")
        print(f"   Q: 什么是 RAG？")
        print(f"   A: {result1['answer'][:100]}...")
        
        result2 = client.query("它有什么优势？")
        print(f"   Q: 它有什么优势？")
        print(f"   A: {result2['answer'][:100]}...")
        print()
        
        # 4. 查看相关文档
        print("4. 查看检索到的相关文档...")
        if result1['retrieved_docs']:
            for i, doc in enumerate(result1['retrieved_docs'], 1):
                filename = doc['metadata'].get('filename', '未知')
                print(f"   {i}. {filename}")
        print()
        
    except requests.exceptions.ConnectionError:
        print("错误: 无法连接到服务器")
        print("请确保服务器正在运行: python main.py")
    except Exception as e:
        print(f"错误: {e}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "interactive":
        # 交互模式
        client = AIAgentClient()
        client.chat_interactive()
    else:
        # 示例模式
        example_usage()
        
        print("\n提示: 运行 'python example_client.py interactive' 进入交互模式")
