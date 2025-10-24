"""向量存储模块"""
import chromadb
from chromadb.config import Settings as ChromaSettings
from typing import List, Dict
from sentence_transformers import SentenceTransformer


class VectorStore:
    """向量存储，使用ChromaDB"""
    
    def __init__(self, db_path: str, collection_name: str = "documents"):
        self.db_path = db_path
        self.collection_name = collection_name
        
        # 初始化ChromaDB
        self.client = chromadb.PersistentClient(
            path=db_path,
            settings=ChromaSettings(anonymized_telemetry=False)
        )
        
        # 初始化嵌入模型
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # 获取或创建集合
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"description": "文档知识库"}
        )
    
    def add_documents(self, chunks: List[Dict[str, str]]):
        """添加文档到向量数据库"""
        if not chunks:
            print("没有文档需要添加")
            return
        
        print(f"正在添加 {len(chunks)} 个文档块到向量数据库...")
        
        # 准备数据
        documents = []
        metadatas = []
        ids = []
        
        for i, chunk in enumerate(chunks):
            documents.append(chunk['content'])
            metadatas.append(chunk['metadata'])
            ids.append(f"doc_{i}")
        
        # 生成嵌入向量
        embeddings = self.embedding_model.encode(documents).tolist()
        
        # 添加到ChromaDB
        self.collection.add(
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )
        
        print(f"成功添加 {len(chunks)} 个文档块")
    
    def query(self, query_text: str, top_k: int = 3) -> List[Dict]:
        """查询相关文档"""
        # 生成查询向量
        query_embedding = self.embedding_model.encode([query_text]).tolist()
        
        # 查询ChromaDB
        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=top_k
        )
        
        # 格式化结果
        formatted_results = []
        if results['documents']:
            for i in range(len(results['documents'][0])):
                formatted_results.append({
                    'content': results['documents'][0][i],
                    'metadata': results['metadatas'][0][i],
                    'distance': results['distances'][0][i] if 'distances' in results else None
                })
        
        return formatted_results
    
    def clear(self):
        """清空集合"""
        self.client.delete_collection(name=self.collection_name)
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"description": "文档知识库"}
        )
        print("向量数据库已清空")
    
    def count(self) -> int:
        """获取文档数量"""
        return self.collection.count()
