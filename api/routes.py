from fastapi import FastAPI, UploadFile, File
import sys, os, tempfile

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.chatbot import process_document, chat

app = FastAPI(title="Multi-Document AI Chatbot API")

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    suffix = os.path.splitext(file.filename)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name
    n_chunks = process_document(tmp_path, original_filename=file.filename)
    return {"filename": file.filename, "chunks_indexed": n_chunks}

@app.post("/chat")
async def chat_endpoint(query: str):
    answer, sources = chat(query)
    return {"answer": answer, "sources": sources}