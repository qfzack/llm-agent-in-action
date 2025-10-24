#!/usr/bin/env python3
"""查看向量数据库内容的脚本"""

import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.services.vector_store import VectorStore
from src.core.config import settings
import json


def view_database_info():
    """查看数据库基本信息"""
    print("=== ChromaDB 向量数据库信息 ===\n")
    
    vector_store = VectorStore(settings.vector_db_path)
    
    # 基本信息
    print(f"数据库路径: {settings.vector_db_path}")
    print(f"集合名称: {vector_store.collection_name}")
    print(f"文档总数: {vector_store.count()}")
    print(f"嵌入模型: all-MiniLM-L6-v2")
    
    # 集合信息
    collection_metadata = vector_store.collection.metadata
    print(f"集合描述: {collection_metadata.get('description', 'N/A')}")
    
    return vector_store


def view_all_documents(vector_store, limit=10):
    """查看所有文档"""
    print(f"\n=== 文档内容 (前 {limit} 个) ===\n")
    
    try:
        # 获取所有文档
        results = vector_store.collection.get(limit=limit)
        
        if not results['documents']:
            print("数据库中没有文档")
            return
        
        for i, (doc_id, document, metadata) in enumerate(zip(
            results['ids'], 
            results['documents'], 
            results['metadatas']
        )):
            print(f"📄 文档 {i+1}:")
            print(f"   ID: {doc_id}")
            print(f"   内容长度: {len(document)} 字符")
            print(f"   内容预览: {document[:200]}{'...' if len(document) > 200 else ''}")
            
            if metadata:
                print(f"   元数据:")
                for key, value in metadata.items():
                    print(f"     {key}: {value}")
            
            print("-" * 60)
    
    except Exception as e:
        print(f"获取文档时出错: {e}")


def search_documents(vector_store, query="什么", top_k=3):
    """搜索相关文档"""
    print(f"\n=== 搜索测试: '{query}' ===\n")
    
    try:
        results = vector_store.query(query, top_k)
        
        if not results:
            print("没有找到相关文档")
            return
        
        for i, result in enumerate(results, 1):
            print(f"🔍 相关文档 {i}:")
            print(f"   相似度距离: {result.get('distance', 'N/A'):.4f}")
            print(f"   内容: {result['content'][:300]}{'...' if len(result['content']) > 300 else ''}")
            
            if result.get('metadata'):
                print(f"   来源: {result['metadata'].get('filename', 'Unknown')}")
            
            print("-" * 60)
    
    except Exception as e:
        print(f"搜索时出错: {e}")


def view_collection_stats(vector_store):
    """查看集合统计信息"""
    print("\n=== 集合统计信息 ===\n")
    
    try:
        # 获取所有文档的元数据来统计
        results = vector_store.collection.get()
        
        if not results['metadatas']:
            print("没有元数据可统计")
            return
        
        # 统计文件类型
        file_types = {}
        filenames = set()
        
        for metadata in results['metadatas']:
            if metadata and 'filename' in metadata:
                filename = metadata['filename']
                filenames.add(filename)
                
                # 获取文件扩展名
                ext = Path(filename).suffix.lower()
                file_types[ext] = file_types.get(ext, 0) + 1
        
        print(f"文档块总数: {len(results['documents'])}")
        print(f"源文件数量: {len(filenames)}")
        print(f"文件类型分布:")
        for ext, count in file_types.items():
            print(f"   {ext or '无扩展名'}: {count} 个块")
        
        print(f"\n源文件列表:")
        for filename in sorted(filenames):
            print(f"   📁 {filename}")
    
    except Exception as e:
        print(f"获取统计信息时出错: {e}")


def main():
    """主函数"""
    try:
        # 查看基本信息
        vector_store = view_database_info()
        
        # 查看统计信息
        view_collection_stats(vector_store)
        
        # 查看文档内容
        view_all_documents(vector_store, limit=5)
        
        # 搜索测试
        search_documents(vector_store, "系统", top_k=3)
        
    except Exception as e:
        print(f"错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()