import os
from src.pdf_loader import load_pdf
from src.docx_loader import load_docx
from src.txt_loader import load_txt
from src.text_splitter import split_text
from src.vector_store import build_vector_store, list_documents, delete_document, reset_all
from src.rag import answer_question

def process_document(file_path: str, original_filename: str = None):
    ext = os.path.splitext(file_path)[1].lower()
    filename = original_filename or os.path.basename(file_path)

    if ext == ".pdf":
        text = load_pdf(file_path)
    elif ext == ".docx":
        text = load_docx(file_path)
    elif ext == ".txt":
        text = load_txt(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

    chunks = split_text(text)
    build_vector_store(chunks, source_name=filename)
    return len(chunks)

def chat(query: str, chat_history: list = None):
    answer, sources = answer_question(query, chat_history)
    return answer, sources

def get_documents():
    return list_documents()

def remove_document(source_name: str):
    return delete_document(source_name)

def reset_index():
    reset_all()