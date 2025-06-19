from pathlib import Path
from dotenv import load_dotenv

# Load OPENAI_API_KEY from .env or environment
load_dotenv()

# ------------ global constants ------------
INDEX_DIR = Path("faiss_index")

CHUNK_SIZE = 512
CHUNK_OVERLAP = 64

EMBED_MODEL = "text-embedding-3-small"   # OpenAI
LLM_MODEL   = "gpt-3.5-turbo"             # OpenAI chat
