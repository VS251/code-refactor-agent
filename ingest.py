import os
import glob
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

DB_DIR = "chroma_db"

EMBEDDING_MODEL = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def ingest_codebase(root_dir="."):
    """Scans for .py files, chunks them, and saves to Vector DB."""
    print(f"Scanning '{root_dir}' for Python files...")

    files = glob.glob(os.path.join(root_dir, "**/*.py"), recursive=True)

    files = [f for f in files if "venv" not in f and "chroma_db" not in f and "__" not in f]

    if not files:
        print("No Python files found!")
        return

    documents = []
    for f in files:
        try:
            loader = TextLoader(f)
            documents.extend(loader.load())
        except Exception as e:
            print(f"Could not load {f}: {e}")

    print(f"📄 Loaded {len(documents)} files. Splitting into chunks...")

    text_splitter = RecursiveCharacterTextSplitter.from_language(
        language="python",
        chunk_size=1000,
        chunk_overlap=100
    )
    texts = text_splitter.split_documents(documents)

    print(f"Saving {len(texts)} chunks to ChromaDB at '{DB_DIR}'...")
    
    Chroma.from_documents(
        documents=texts,
        embedding=EMBEDDING_MODEL,
        persist_directory=DB_DIR
    )
    print("Memory Updated! The agent now knows this codebase.")

if __name__ == "__main__":
    ingest_codebase()