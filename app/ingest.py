from pathlib import Path
from typing import List

from .io_utils import load_files, chunk_docs
from .vector_store import load_or_create, save


def ingest(file_paths: List[Path]):
    print(f"📥  Ingesting {len(file_paths)} file(s)…")
    raw_docs = load_files(file_paths)
    if not raw_docs:
        print("Nothing to ingest.")
        return

    chunks = chunk_docs(raw_docs)
    print(f" → {len(raw_docs)} docs → {len(chunks)} chunks")

    db = load_or_create()
    db.add_documents(chunks)
    save(db)
    print("✅  Index updated & saved.")
