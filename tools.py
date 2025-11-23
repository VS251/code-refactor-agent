import ast
import os
from langchain_core.tools import tool

def log_action(action, details):
    print(f"\033[93m[TOOL EXECUTION] {action}: {details}\033[0m")

@tool
def read_file(file_path: str) -> str:
    """Reads the code from a specific file path."""
    log_action("READING", file_path) 
    try:
        if not os.path.exists(file_path):
            return f"Error: File {file_path} does not exist."
        with open(file_path, "r") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {e}"

@tool
def write_file(file_path: str, content: str) -> str:
    """
    Overwrites the target file with new content.
    """
    log_action("WRITING", f"Saving {len(content)} chars to {file_path}") # <--- Log it!
    
    if "refactored code" in content.lower() and len(content) < 200:
        return "ERROR: It looks like you wrote a placeholder. You must write the FULL code."

    try:
        with open(file_path, "w") as f:
            f.write(content)
        return f"Successfully wrote to {file_path}"
    except Exception as e:
        return f"Error writing file: {e}"

@tool
def validate_syntax(code: str) -> str:
    """Checks if the given Python code has valid syntax."""
    try:
        ast.parse(code)
        return "Valid Syntax"
    except SyntaxError as e:
        return f"Syntax Error: {e}"

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
DB_DIR = "chroma_db"
EMBEDDING_MODEL = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

@tool
def search_codebase(query: str) -> str:
    """Searches the codebase."""
    log_action("SEARCHING", query)
    try:
        db = Chroma(persist_directory=DB_DIR, embedding_function=EMBEDDING_MODEL)
        results = db.similarity_search(query, k=3)
        if not results: return "No relevant code found."
        output = ""
        for doc in results:
            output += f"\n--- Source: {doc.metadata.get('source', 'unknown')} ---\n{doc.page_content}\n"
        return output
    except Exception as e:
        return f"Error: {e}"