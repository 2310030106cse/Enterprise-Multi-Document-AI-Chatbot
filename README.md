# 📚 Enterprise Multi-Document AI Chatbot

A retrieval-augmented generation (RAG) chatbot that answers questions grounded in your own PDF, DOCX, and TXT files — fully local, no paid API keys required.

## Features
- **Multi-format ingestion**: PDF, DOCX, and TXT document loaders
- **Semantic search**: HuggingFace sentence embeddings + FAISS vector store
- **Local LLM inference**: Ollama running Llama 3.2, no cloud API costs
- **Conversation memory**: multi-turn context for natural follow-up questions
- **Document management**: view indexed docs, chunk counts, delete individual files or reset the index
- **Source attribution**: every answer cites which document(s) it came from
- **Dual interface**: Streamlit chat UI + FastAPI REST backend

## Architecture
Upload → Load & split (PDF/DOCX/TXT loaders + recursive chunking) → Embed & index (MiniLM embeddings → FAISS) → Retrieve top-k relevant chunks → Generate grounded answer (Ollama Llama 3.2) → Return answer with sources.

## Tech Stack
| Layer | Technology |
|---|---|
| LLM | Ollama (Llama 3.2, local) |
| Embeddings | HuggingFace `sentence-transformers/all-MiniLM-L6-v2` |
| Vector Store | FAISS |
| Orchestration | LangChain |
| Frontend | Streamlit |
| API | FastAPI |

## Setup

\`\`\`bash
# Clone and enter project
git clone <your-repo-url>
cd Enterprise-Multi-Document-AI-Chatbot

# Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1   # Windows PowerShell

# Install dependencies
pip install -r requirements.txt

# Install Ollama (https://ollama.com) and pull the model
ollama pull llama3.2

# Run the Streamlit app
streamlit run frontend/streamlit_app.py
\`\`\`

## Usage
1. Upload PDF/DOCX/TXT files in the sidebar
2. Click **Process Documents** to chunk and index them
3. Ask questions in the chat — answers are grounded in your documents with source citations
4. Manage indexed documents (delete individual files or reset the whole index) from the sidebar

## API
Run the FastAPI backend separately for programmatic access:
\`\`\`bash
uvicorn api.routes:app --reload
\`\`\`
Interactive docs at `http://localhost:8000/docs`.

## Project Structure
\`\`\`
├── api/
│   └── routes.py          # FastAPI endpoints
├── frontend/
│   └── streamlit_app.py   # Streamlit chat UI
├── src/
│   ├── pdf_loader.py
│   ├── docx_loader.py
│   ├── txt_loader.py
│   ├── text_splitter.py
│   ├── embeddings.py
│   ├── vector_store.py    # FAISS index + document management
│   ├── prompts.py
│   ├── rag.py              # Ollama LLM + retrieval logic
│   └── chatbot.py          # orchestration layer
└── requirements.txt
\`\`\`