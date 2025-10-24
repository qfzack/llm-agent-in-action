"""测试脚本 - 支持自动启动服务器"""
import requests
import json
import time
import subprocess
import sys
import os
from pathlib import Path


BASE_URL = "http://localhost:8000"
PROJECT_ROOT = Path(__file__).parent.parent
SERVER_SCRIPT = PROJECT_ROOT / "server.py"


def check_server_running():
    """检查服务器是否正在运行"""
    try:
        response = requests.get(f"{BASE_URL}/", timeout=2)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False


def start_server():
    """启动测试服务器"""
    print("🚀 启动测试服务器...")
    
    # 使用 uv run 启动服务器
    process = subprocess.Popen(
        ["uv", "run", "python", str(SERVER_SCRIPT)],
        cwd=str(PROJECT_ROOT),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # 等待服务器启动（最多30秒）
    print("⏳ 等待服务器就绪", end="", flush=True)
    for i in range(30):
        time.sleep(1)
        print(".", end="", flush=True)
        if check_server_running():
            print(" ✓")
            print(f"✓ 服务器已启动 (PID: {process.pid})")
            return process
        
        # 检查进程是否异常退出
        if process.poll() is not None:
            stdout, stderr = process.communicate()
            print(" ✗")
            print(f"❌ 服务器启动失败")
            if stderr:
                print(f"错误信息:\n{stderr}")
            return None
    
    print(" ✗")
    print("❌ 服务器启动超时")
    process.terminate()
    return None


def stop_server(process):
    """停止测试服务器"""
    if process and process.poll() is None:
        print("\n🛑 停止测试服务器...")
        process.terminate()
        try:
            process.wait(timeout=5)
            print("✓ 服务器已停止")
        except subprocess.TimeoutExpired:
            process.kill()
            print("✓ 服务器已强制停止")


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
    
    server_process = None
    server_was_running = check_server_running()
    
    try:
        # 如果服务器未运行，自动启动
        if not server_was_running:
            print("ℹ️  服务器未运行，将自动启动临时服务器")
            server_process = start_server()
            if not server_process:
                print("❌ 无法启动服务器，测试中止")
                return False
            print()
        else:
            print("ℹ️  检测到服务器已在运行，将使用现有服务器")
            print()
        
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
        print("✓ 所有测试通过！")
        print("=" * 60)
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ 错误: 无法连接到服务器")
        print("请检查服务器是否正常运行")
        return False
    except KeyboardInterrupt:
        print("\n⚠️  测试被用户中断")
        return False
    except Exception as e:
        print(f"❌ 测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # 只在我们启动的服务器时才停止
        if server_process:
            stop_server(server_process)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # 单独测试模式（不自动启动服务器）
        if not check_server_running():
            print("❌ 服务器未运行")
            print("提示: 直接运行 'python test_api.py' 可自动启动服务器")
            sys.exit(1)
        
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
            print("  python test_api.py              # 运行所有测试（自动启动服务器）")
            print("  python test_api.py query <问题>  # 测试查询")
            print("  python test_api.py upload <文件> # 测试上传")
    else:
        # 运行完整测试套件（自动管理服务器）
        success = run_all_tests()
        sys.exit(0 if success else 1)
