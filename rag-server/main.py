import os
import sys
from pathlib import Path

# ✅ 먼저 API 키 직접 설정
os.environ["OPENAI_API_KEY"] = "YOUR_API_KEY"
# ✅ 설정된 환경 변수 확인
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    print("ERROR: OPENAI_API_KEY environment variable is not set.", file=sys.stderr)
    sys.exit(1)

import logging
from mcp.server.fastmcp import FastMCP

from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

logging.basicConfig(level=logging.INFO)

mcp = FastMCP("PDF-RAG")

# ✅ PDF 경로 설정
PDF_PATH = "C:\\vibeCoding\\rag-server\\스마트팜.pdf"

# ✅ PDF 로드
loader = PyPDFLoader(PDF_PATH)
pages = loader.load()

# ✅ 텍스트 나누기
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs = splitter.split_documents(pages)

# ✅ 임베딩 + 모델 준비
embeddings = OpenAIEmbeddings()
llm = ChatOpenAI(model="gpt-4o")

# ✅ 벡터 저장소 구성
vectorstore = Chroma.from_documents(docs, embeddings)

# ✅ 질의응답 체인 구성
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectorstore.as_retriever()
)

# ✅ MCP 툴 등록
@mcp.tool()
def ask_pdf(query: str) -> str:
    """PDF 내용을 기반으로 질문에 답변합니다."""
    logging.info(f"Received query: {query}")
    return qa_chain.run(query)

# ✅ MCP 실행
if __name__ == "__main__":
    mcp.run(transport="stdio")



