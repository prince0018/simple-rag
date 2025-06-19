from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Initialize RAG chain with error handling
try:
    from app.rag_chain import create_rag_chain
    rag_chain = create_rag_chain()
    chat_history = []
    logger.info("RAG chain initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize RAG chain: {e}")
    rag_chain = None

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str
    sources: List[str]

@router.post("/query", response_model=QueryResponse)
def query_rag(req: QueryRequest):
    """Query the RAG system with a question"""
    if rag_chain is None:
        raise HTTPException(
            status_code=500, 
            detail="RAG chain not initialized. Please check your FAISS index and environment variables."
        )
    
    try:
        result = rag_chain({
            "question": req.question,
            "chat_history": chat_history
        })
        
        answer = result["answer"]
        chat_history.append((req.question, answer))

        sources = [doc.metadata.get("source", "unknown") for doc in result["source_documents"]]
        
        logger.info(f"Query processed successfully: {req.question[:50]}...")
        return QueryResponse(answer=answer, sources=sources)
    
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

@router.get("/health")
def health():
    """Health check endpoint"""
    status = "ok" if rag_chain is not None else "error"
    return {
        "status": status,
        "rag_chain_initialized": rag_chain is not None
    }

@router.get("/chat-history")
def get_chat_history():
    """Get the current chat history"""
    return {"chat_history": chat_history}

@router.delete("/chat-history")
def clear_chat_history():
    """Clear the chat history"""
    global chat_history
    chat_history = []
    return {"message": "Chat history cleared"}
