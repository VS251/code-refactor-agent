# Autonomous Code Refactoring Agent (Local Llama 3.1)

An autonomous AI agent that performs static code analysis and refactoring on your local codebase. Built with **Python**, **LangChain**, and **Ollama**, it runs completely offline using the **Llama 3.1** Large Language Model.

## Features

* **Autonomous Agentic Loop:** Uses a ReAct (Reason + Act) loop to read files, plan refactors, and execute changes.
* **RAG Memory:** Ingests the entire codebase into a local Vector Database (**ChromaDB**) to understand context across multiple files.
* **Safety Guards:** Includes a syntax validation tool (`ast` module) that prevents the agent from saving broken Python code.
* **Privacy-First:** Runs 100% locally on your machine—no code leaves your computer.

## 🛠️ Tech Stack

* **Core Logic:** Python 3.9+
* **Orchestration:** LangChain
* **LLM:** Llama 3.1 (8B) via Ollama
* **Vector DB:** ChromaDB
* **CLI:** Typer

## Installation

1.  **Clone the repo**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/code-refactor-agent.git](https://github.com/YOUR_USERNAME/code-refactor-agent.git)
    cd code-refactor-agent
    ```

2.  **Install Dependencies**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

3.  **Setup Ollama**
    * Download [Ollama](https://ollama.com/)
    * Pull the model: `ollama pull llama3.1`
    * Start the server: `ollama serve`

## Usage

**1. Ingest your codebase (Build Memory)**
```bash
python ingest.py
```

**2. Run the Agent**
```bash
python main.py --file your_script.py --instruction "Refactor this to use a class structure and add type hints."
```

## Architecture
* **Ingestion:** Scans .py files -> Embeds using all-MiniLM-L6-v2 -> Stores in ChromaDB.
* **Retrieval:** Agent queries ChromaDB for context ("How is this function used elsewhere?").
* **Action:** Agent uses read_file -> validate_syntax -> write_file tools to safely modify code.
