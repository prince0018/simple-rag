import argparse
from pathlib import Path

from app.ingest import ingest
from app.chat_loop import chat

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
