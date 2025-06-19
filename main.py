from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import router
from prometheus_fastapi_instrumentator import Instrumentator



app = FastAPI(
    title="Simple RAG API",
    description="A simple RAG (Retrieval-Augmented Generation) API using LangChain and OpenAI",
    version="1.0.0"
)

#  Add Prometheus instrumentation
Instrumentator().instrument(app).expose(app)

# Add CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/")
def root():
    """Root endpoint with API information"""
    return {
        "message": "Simple RAG API",
        "docs": "/docs",
        "health": "/health"
    }