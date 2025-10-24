"""测试脚本"""
import requests
import json
import time


BASE_URL = "http://localhost:8000"


def test_health_check():
    """测试健康检查"""
    print("1. 测试健康检查...")
    response = requests.get(f"{BASE_URL}/")
    print(f"   状态码: {response.status_code}")
    print(f"   响应: {response.json()}")
    print()


def test_status():
    """测试获取状态"""
    print("2. 测试获取系统状态...")
    response = requests.get(f"{BASE_URL}/status")
    print(f"   状态码: {response.status_code}")
    result = response.json()
    print(f"   文档数量: {result['document_count']}")
    print(f"   系统状态: {result['status']}")
    print()


def test_reload():
    """测试重新加载文档"""
    print("3. 测试重新加载文档...")
    response = requests.post(f"{BASE_URL}/reload")
    print(f"   状态码: {response.status_code}")
    result = response.json()
    print(f"   加载状态: {result['status']}")
    print(f"   文档数量: {result['document_count']}")
    print(f"   消息: {result['message']}")
    print()


def test_query(question):
    """测试查询"""
    print(f"4. 测试查询: '{question}'")
    response = requests.post(
        f"{BASE_URL}/query",
        json={"query": question}
    )
    print(f"   状态码: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"   回答: {result['answer'][:200]}...")
        print(f"   相关文档数: {len(result['retrieved_docs'])}")
        
        if result['retrieved_docs']:
            print("   相关文档:")
            for i, doc in enumerate(result['retrieved_docs'], 1):
                filename = doc['metadata'].get('filename', '未知')
                print(f"     {i}. {filename}")
    else:
        print(f"   错误: {response.text}")
    print()


def test_query_with_history():
    """测试带对话历史的查询"""
    print("5. 测试带对话历史的查询...")
    
    conversation_history = [
        {"role": "user", "content": "这个系统是做什么的？"},
        {"role": "assistant", "content": "这是一个基于RAG的AI知识库问答系统。"}
    ]
    
    response = requests.post(
        f"{BASE_URL}/query",
        json={
            "query": "它有哪些功能？",
            "conversation_history": conversation_history
        }
    )
    
    print(f"   状态码: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"   回答: {result['answer'][:200]}...")
    print()


def test_upload(file_path):
    """测试上传文档"""
    print(f"6. 测试上传文档: {file_path}")
    try:
        with open(file_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(f"{BASE_URL}/upload", files=files)
        
        print(f"   状态码: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"   上传状态: {result['status']}")
            print(f"   消息: {result['message']}")
            print(f"   文档块数: {result['chunks']}")
    except FileNotFoundError:
        print(f"   文件不存在: {file_path}")
    except Exception as e:
        print(f"   错误: {e}")
    print()


def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("AI Agent 系统测试")
    print("=" * 60)
    print()
    
    try:
        # 基础测试
        test_health_check()
        test_status()
        
        # 加载文档
        test_reload()
        
        # 等待一下确保加载完成
        time.sleep(2)
        
        # 查询测试
        test_query("这个系统有什么功能？")
        test_query("RAG 是什么？")
        test_query_with_history()
        
        print("=" * 60)
        print("测试完成！")
        print("=" * 60)
        
    except requests.exceptions.ConnectionError:
        print("错误: 无法连接到服务器")
        print("请确保服务器正在运行: python main.py")
    except Exception as e:
        print(f"测试过程中发生错误: {e}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "query":
            question = " ".join(sys.argv[2:])
            test_query(question)
        elif sys.argv[1] == "upload":
            if len(sys.argv) > 2:
                test_upload(sys.argv[2])
            else:
                print("用法: python test_api.py upload <文件路径>")
        else:
            print("用法:")
            print("  python test_api.py              # 运行所有测试")
            print("  python test_api.py query <问题>  # 测试查询")
            print("  python test_api.py upload <文件> # 测试上传")
    else:
        run_all_tests()
