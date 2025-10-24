"""FastAPI服务主文件"""
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict
import uvicorn
import os
from pathlib import Path

from ..core.config import settings
from ..core.agent import AIAgent
from ..services.document_loader import DocumentLoader, TextSplitter
from ..services.vector_store import VectorStore


# 创建FastAPI应用
app = FastAPI(
    title="AI Agent 知识库问答系统",
    description="基于RAG的AI知识库问答系统",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化组件
vector_store = VectorStore(settings.vector_db_path)
agent = AIAgent(vector_store)
document_loader = DocumentLoader(settings.documents_path)
text_splitter = TextSplitter(settings.chunk_size, settings.chunk_overlap)


# 请求模型
class QueryRequest(BaseModel):
    query: str
    conversation_history: Optional[List[Dict[str, str]]] = None


class QueryResponse(BaseModel):
    answer: str
    retrieved_docs: List[Dict]
    has_context: bool


class StatusResponse(BaseModel):
    status: str
    document_count: int
    message: str


# API路由
@app.get("/")
async def root():
    """健康检查"""
    return {
        "message": "AI Agent 知识库问答系统正在运行",
        "version": "1.0.0",
        "status": "healthy"
    }


@app.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    """
    查询知识库
    
    Args:
        request: 包含查询问题和对话历史的请求
    
    Returns:
        包含答案和相关文档的响应
    """
    try:
        result = agent.chat(request.query, request.conversation_history)
        return QueryResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """
    上传文档到知识库
    
    Args:
        file: 上传的文件
    
    Returns:
        上传状态
    """
    try:
        # 保存文件
        file_path = Path(settings.documents_path) / file.filename
        
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # 加载文档
        doc = document_loader.load_document(file_path)
        
        if not doc:
            raise HTTPException(status_code=400, detail="不支持的文件格式")
        
        # 分割文档
        chunks = text_splitter.split_documents([doc])
        
        # 添加到向量数据库
        vector_store.add_documents(chunks)
        
        return {
            "status": "success",
            "message": f"文档 {file.filename} 上传成功",
            "chunks": len(chunks)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/reload", response_model=StatusResponse)
async def reload_documents():
    """
    重新加载所有文档
    
    Returns:
        加载状态
    """
    try:
        # 清空向量数据库
        vector_store.clear()
        
        # 加载所有文档
        documents = document_loader.load_all_documents()
        
        if not documents:
            return StatusResponse(
                status="warning",
                document_count=0,
                message="没有找到文档"
            )
        
        # 分割文档
        chunks = text_splitter.split_documents(documents)
        
        # 添加到向量数据库
        vector_store.add_documents(chunks)
        
        return StatusResponse(
            status="success",
            document_count=len(documents),
            message=f"成功加载 {len(documents)} 个文档，共 {len(chunks)} 个文档块"
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/status", response_model=StatusResponse)
async def get_status():
    """
    获取系统状态
    
    Returns:
        系统状态信息
    """
    try:
        doc_count = vector_store.count()
        return StatusResponse(
            status="running",
            document_count=doc_count,
            message=f"系统正在运行，共有 {doc_count} 个文档块"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/clear")
async def clear_database():
    """
    清空知识库
    
    Returns:
        清空状态
    """
    try:
        vector_store.clear()
        return {
            "status": "success",
            "message": "知识库已清空"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 启动函数
def start_server():
    """启动服务器"""
    uvicorn.run(
        "src.api.main:app",
        host=settings.host,
        port=settings.port,
        reload=True
    )


if __name__ == "__main__":
    start_server()
