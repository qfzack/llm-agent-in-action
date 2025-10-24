"""文档加载和处理模块"""
import os
from typing import List, Dict
from pathlib import Path
import pypdf
import docx
import markdown
from bs4 import BeautifulSoup


class DocumentLoader:
    """文档加载器，支持多种文档格式"""
    
    def __init__(self, documents_path: str):
        self.documents_path = Path(documents_path)
        
    def load_pdf(self, file_path: Path) -> str:
        """加载PDF文件"""
        text = ""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = pypdf.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
        except Exception as e:
            print(f"加载PDF文件失败 {file_path}: {e}")
        return text
    
    def load_docx(self, file_path: Path) -> str:
        """加载Word文档"""
        text = ""
        try:
            doc = docx.Document(file_path)
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
        except Exception as e:
            print(f"加载Word文档失败 {file_path}: {e}")
        return text
    
    def load_markdown(self, file_path: Path) -> str:
        """加载Markdown文件"""
        text = ""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                md_content = file.read()
                html = markdown.markdown(md_content)
                soup = BeautifulSoup(html, 'html.parser')
                text = soup.get_text()
        except Exception as e:
            print(f"加载Markdown文件失败 {file_path}: {e}")
        return text
    
    def load_txt(self, file_path: Path) -> str:
        """加载纯文本文件"""
        text = ""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
        except Exception as e:
            print(f"加载文本文件失败 {file_path}: {e}")
        return text
    
    def load_document(self, file_path: Path) -> Dict[str, str]:
        """根据文件类型加载文档"""
        suffix = file_path.suffix.lower()
        
        loaders = {
            '.pdf': self.load_pdf,
            '.docx': self.load_docx,
            '.doc': self.load_docx,
            '.md': self.load_markdown,
            '.txt': self.load_txt,
        }
        
        loader = loaders.get(suffix)
        if loader:
            content = loader(file_path)
            return {
                'filename': file_path.name,
                'path': str(file_path),
                'content': content,
                'type': suffix
            }
        else:
            print(f"不支持的文件类型: {suffix}")
            return None
    
    def load_all_documents(self) -> List[Dict[str, str]]:
        """加载目录下所有支持的文档"""
        documents = []
        
        if not self.documents_path.exists():
            print(f"文档目录不存在: {self.documents_path}")
            return documents
        
        supported_extensions = {'.pdf', '.docx', '.doc', '.md', '.txt'}
        
        for file_path in self.documents_path.rglob('*'):
            if file_path.is_file() and file_path.suffix.lower() in supported_extensions:
                doc = self.load_document(file_path)
                if doc and doc['content'].strip():
                    documents.append(doc)
                    print(f"已加载: {file_path.name}")
        
        print(f"总共加载了 {len(documents)} 个文档")
        return documents


class TextSplitter:
    """文本分割器，将长文本分割成小块"""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def split_text(self, text: str) -> List[str]:
        """将文本分割成固定大小的块"""
        chunks = []
        start = 0
        text_length = len(text)
        
        while start < text_length:
            end = start + self.chunk_size
            chunk = text[start:end]
            
            # 尝试在句子边界处分割
            if end < text_length:
                last_period = chunk.rfind('。')
                last_newline = chunk.rfind('\n')
                last_space = chunk.rfind(' ')
                
                split_point = max(last_period, last_newline, last_space)
                if split_point > self.chunk_size // 2:
                    chunk = chunk[:split_point + 1]
                    end = start + len(chunk)
            
            if chunk.strip():
                chunks.append(chunk.strip())
            
            start = end - self.chunk_overlap
        
        return chunks
    
    def split_documents(self, documents: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """分割多个文档"""
        chunks = []
        
        for doc in documents:
            text_chunks = self.split_text(doc['content'])
            for i, chunk in enumerate(text_chunks):
                chunks.append({
                    'content': chunk,
                    'metadata': {
                        'filename': doc['filename'],
                        'path': doc['path'],
                        'type': doc['type'],
                        'chunk_id': i
                    }
                })
        
        return chunks
