"""主入口文件"""
import sys
from pathlib import Path

# 添加 src 到 Python 路径
sys.path.insert(0, str(Path(__file__).parent))

from src.cli.cli import main

if __name__ == "__main__":
    main()
