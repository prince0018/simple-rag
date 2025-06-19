from langchain.chains import ConversationalRetrievalChain
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

INDEX_DIR = Path("faiss_index")
EMBED_MODEL = "text-embedding-ada-002"
LLM_MODEL = "gpt-3.5-turbo"

def create_rag_chain():
    """Create and return a RAG chain with proper error handling"""
    try:
        # Check if index exists
        if not INDEX_DIR.exists():
            raise FileNotFoundError(f"FAISS index not found at {INDEX_DIR}. Please run your rag.py to create it first.")
        
        embeddings = OpenAIEmbeddings(
            model=EMBED_MODEL,
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            default_headers={"OpenAI-Project": os.getenv("OPENAI_PROJECT_ID")} if os.getenv("OPENAI_PROJECT_ID") else None
        )
        
        db = FAISS.load_local(INDEX_DIR, embeddings, allow_dangerous_deserialization=True)
        retriever = db.as_retriever(search_kwargs={"k": 3})

        llm = ChatOpenAI(
            model=LLM_MODEL,
            temperature=0.2,
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            default_headers={"OpenAI-Project": os.getenv("OPENAI_PROJECT_ID")} if os.getenv("OPENAI_PROJECT_ID") else None
        )

        return ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=retriever,
            return_source_documents=True,
        )
    except Exception as e:
        print(f"Error creating RAG chain: {e}")
        raise