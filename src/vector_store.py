import os
import shutil
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from src.embeddings import get_embeddings

INDEX_PATH = "data/faiss_index"

def build_vector_store(chunks: list[str], source_name: str = "unknown"):
    embeddings = get_embeddings()
    docs = [Document(page_content=chunk, metadata={"source": source_name}) for chunk in chunks]

    if os.path.exists(INDEX_PATH):
        vectordb = FAISS.load_local(INDEX_PATH, embeddings, allow_dangerous_deserialization=True)
        vectordb.add_documents(docs)
    else:
        vectordb = FAISS.from_documents(docs, embeddings)

    vectordb.save_local(INDEX_PATH)
    return vectordb

def load_vector_store():
    embeddings = get_embeddings()
    if not os.path.exists(INDEX_PATH):
        return None
    return FAISS.load_local(INDEX_PATH, embeddings, allow_dangerous_deserialization=True)

def list_documents() -> dict:
    """Returns {source_name: chunk_count} for every indexed document."""
    vectordb = load_vector_store()
    if vectordb is None:
        return {}
    summary = {}
    for doc in vectordb.docstore._dict.values():
        src = doc.metadata.get("source", "unknown")
        summary[src] = summary.get(src, 0) + 1
    return summary

def delete_document(source_name: str) -> int:
    """Deletes all chunks belonging to source_name. Returns number of chunks removed."""
    vectordb = load_vector_store()
    if vectordb is None:
        return 0
    ids_to_delete = [
        doc_id for doc_id, doc in vectordb.docstore._dict.items()
        if doc.metadata.get("source") == source_name
    ]
    if ids_to_delete:
        vectordb.delete(ids_to_delete)
        vectordb.save_local(INDEX_PATH)
    return len(ids_to_delete)

def reset_all():
    """Wipes the entire index."""
    if os.path.exists(INDEX_PATH):
        shutil.rmtree(INDEX_PATH)