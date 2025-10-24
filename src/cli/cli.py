"""命令行工具"""
import argparse
import sys
from pathlib import Path

from ..core.config import settings
from ..core.agent import AIAgent
from ..services.document_loader import DocumentLoader, TextSplitter
from ..services.vector_store import VectorStore


def load_documents():
    """加载文档到向量数据库"""
    print("=== 加载文档 ===\n")
    
    # 初始化组件
    document_loader = DocumentLoader(settings.documents_path)
    text_splitter = TextSplitter(settings.chunk_size, settings.chunk_overlap)
    vector_store = VectorStore(settings.vector_db_path)
    
    # 清空现有数据
    print("清空现有向量数据库...")
    vector_store.clear()
    
    # 加载所有文档
    print(f"从 {settings.documents_path} 加载文档...")
    documents = document_loader.load_all_documents()
    
    if not documents:
        print("警告: 没有找到文档")
        return
    
    # 分割文档
    print("\n分割文档...")
    chunks = text_splitter.split_documents(documents)
    print(f"生成了 {len(chunks)} 个文档块")
    
    # 添加到向量数据库
    print("\n添加到向量数据库...")
    vector_store.add_documents(chunks)
    
    print(f"\n✓ 成功！加载了 {len(documents)} 个文档")


def query_interactive():
    """交互式查询"""
    print("=== AI Agent 交互式问答 ===")
    print("输入 'quit' 或 'exit' 退出\n")
    
    # 初始化组件
    vector_store = VectorStore(settings.vector_db_path)
    agent = AIAgent(vector_store)
    
    # 检查是否有文档
    doc_count = vector_store.count()
    if doc_count == 0:
        print("警告: 向量数据库为空，请先使用 'uv run python -m src.cli load' 加载文档\n")
    else:
        print(f"知识库中有 {doc_count} 个文档块\n")
    
    # 对话历史
    conversation_history = []
    
    while True:
        try:
            # 获取用户输入
            query = input("您: ").strip()
            
            if not query:
                continue
            
            if query.lower() in ['quit', 'exit', 'q']:
                print("再见！")
                break
            
            # 查询
            print("\nAI: ", end="", flush=True)
            result = agent.chat(query, conversation_history)
            print(result['answer'])
            
            # 更新对话历史
            conversation_history.append({"role": "user", "content": query})
            conversation_history.append({"role": "assistant", "content": result['answer']})
            
            # 显示相关文档
            if result['retrieved_docs']:
                print("\n--- 相关文档 ---")
                for i, doc in enumerate(result['retrieved_docs'], 1):
                    filename = doc['metadata'].get('filename', '未知')
                    print(f"{i}. {filename}")
            
            print()
        
        except KeyboardInterrupt:
            print("\n\n再见！")
            break
        except Exception as e:
            print(f"\n错误: {e}\n")


def query_once(question: str):
    """单次查询"""
    vector_store = VectorStore(settings.vector_db_path)
    agent = AIAgent(vector_store)
    
    result = agent.chat(question)
    print(result['answer'])


def show_status():
    """显示系统状态"""
    print("=== 系统状态 ===\n")
    
    vector_store = VectorStore(settings.vector_db_path)
    doc_count = vector_store.count()
    
    print(f"向量数据库路径: {settings.vector_db_path}")
    print(f"文档目录: {settings.documents_path}")
    print(f"文档块数量: {doc_count}")
    print(f"模型: {settings.model_name}")
    print(f"检索Top-K: {settings.top_k}")


def main():
    parser = argparse.ArgumentParser(description="AI Agent 命令行工具")
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # load命令
    subparsers.add_parser('load', help='加载文档到向量数据库')
    
    # query命令
    query_parser = subparsers.add_parser('query', help='查询知识库')
    query_parser.add_argument('question', nargs='?', help='问题（如果不提供则进入交互模式）')
    
    # status命令
    subparsers.add_parser('status', help='显示系统状态')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        if args.command == 'load':
            load_documents()
        elif args.command == 'query':
            if args.question:
                query_once(args.question)
            else:
                query_interactive()
        elif args.command == 'status':
            show_status()
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
