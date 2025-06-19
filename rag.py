# rag_core.py  ✧ upgraded for incremental ingestion

import argparse
import os
from pathlib import Path
from typing import List

from dotenv import load_dotenv


from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import ConversationalRetrievalChain

# --------------------------------------------------
# Configuration
# --------------------------------------------------
load_dotenv()                                     # expects OPENAI_API_KEY and optionally OPENAI_PROJECT_ID
INDEX_DIR = Path("faiss_index")                   # folder will be created on first run
CHUNK_SIZE = 512
CHUNK_OVERLAP = 64
EMBED_MODEL = "text-embedding-ada-002"
LLM_MODEL = "gpt-3.5-turbo"

# --------------------------------------------------
# Helpers
# --------------------------------------------------
def load_files(file_paths: List[Path]):
    """Return a list[Document] from plain-text files."""
    docs = []
    for fp in file_paths:
        if not fp.exists():
            print(f"⚠️  File not found: {fp}")
            continue
        docs.extend(TextLoader(str(fp)).load())
    return docs


def chunk_docs(raw_docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", " ", ""],
    )
    return splitter.split_documents(raw_docs)


def get_vector_store(embeddings):
    """Load existing FAISS store or create an empty one in memory."""
    if INDEX_DIR.exists():
        return FAISS.load_local(INDEX_DIR, embeddings, allow_dangerous_deserialization=True)
    # return an empty store (will be populated later)
    return FAISS.from_documents([], embeddings)


def create_embeddings():
    """Create embeddings with proper OpenAI configuration."""
    # If you have OPENAI_PROJECT_ID in your .env file
    project_id = os.getenv("OPENAI_PROJECT_ID")
    if project_id:
        return OpenAIEmbeddings(
            model=EMBED_MODEL,
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            default_headers={"OpenAI-Project": project_id}
        )
    
    # Fallback to standard configuration
    return OpenAIEmbeddings(model=EMBED_MODEL)


def ingest(files: List[Path]):
    print(f"📥  Ingesting {len(files)} file(s)…")
    raw_docs = load_files(files)
    if not raw_docs:
        print("Nothing to ingest.")
        return

    chunks = chunk_docs(raw_docs)
    print(f" → {len(raw_docs)} docs → {len(chunks)} chunks")

    embeddings = create_embeddings()

    if INDEX_DIR.exists():
        db = FAISS.load_local(INDEX_DIR, embeddings, allow_dangerous_deserialization=True)
        db.add_documents(chunks)
    else:
        db = FAISS.from_documents(chunks, embeddings)

    db.save_local(INDEX_DIR)
    print("✅  Index updated & saved.")


# --------------------------------------------------
# Interactive chat loop
# --------------------------------------------------
def chat():
    if not INDEX_DIR.exists():
        print("❌ No index found. Run with --add first to ingest documents.")
        return

    embeddings = create_embeddings()
    db = FAISS.load_local(INDEX_DIR, embeddings, allow_dangerous_deserialization=True)
    retriever = db.as_retriever(search_kwargs={"k": 3})

    # Configure LLM with project ID if available
    project_id = os.getenv("OPENAI_PROJECT_ID")
    if project_id:
        llm = ChatOpenAI(
            model=LLM_MODEL, 
            temperature=0.2,
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            default_headers={"OpenAI-Project": project_id}
        )
    else:
        llm = ChatOpenAI(model=LLM_MODEL, temperature=0.2)
    
    rag_chain = ConversationalRetrievalChain.from_llm(
        llm,
        retriever=retriever,
        return_source_documents=True,
    )

    chat_history = []

    print("🤖  RAG chat ready. Type questions or 'exit'.")
    while True:
        query = input("\nYou: ").strip()
        if query.lower() in {"exit", "quit"}:
            break

        result = rag_chain({"question": query, "chat_history": chat_history})
        answer = result["answer"]
        chat_history.append((query, answer))

        print("\nAssistant:", answer)
        print("\nSources:")
        for doc in result["source_documents"]:
            print(" •", doc.metadata.get("source", "unknown"))


# --------------------------------------------------
# CLI entry-point
# --------------------------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Mini RAG demo")
    parser.add_argument(
        "--add",
        metavar="FILE",
        type=Path,
        nargs="+",
        help="Add one or more text files to the vector store and exit",
    )
    args = parser.parse_args()

    if args.add:
        ingest(args.add)
    else:
        chat()