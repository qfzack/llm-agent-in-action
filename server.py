"""服务启动文件"""
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent))

if __name__ == "__main__":
    from src.api.main import start_server
    start_server()
