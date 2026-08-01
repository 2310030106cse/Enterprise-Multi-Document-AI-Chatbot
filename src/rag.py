import requests
from src.prompts import RAG_PROMPT
from src.vector_store import load_vector_store

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3.2"

def generate_answer(prompt: str) -> str:
    try:
        response = requests.post(
            OLLAMA_URL,
            json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False},
            timeout=120
        )
        response.raise_for_status()
        return response.json()["response"].strip()
    except requests.exceptions.ConnectionError:
        return "⚠️ Couldn't reach Ollama. Make sure it's installed and running (try `ollama list` in a terminal)."

def _format_history(chat_history: list) -> str:
    if not chat_history:
        return "(no previous conversation)"
    lines = []
    for turn in chat_history[-5:]:
        lines.append(f"User: {turn['user']}")
        lines.append(f"Assistant: {turn['assistant']}")
    return "\n".join(lines)

def answer_question(query: str, chat_history: list = None):
    vectordb = load_vector_store()
    if vectordb is None:
        return "No documents indexed yet. Please upload documents first.", []

    retriever = vectordb.as_retriever(search_kwargs={"k": 4})
    relevant_docs = retriever.invoke(query)

    context = "\n\n".join([doc.page_content for doc in relevant_docs])
    history_text = _format_history(chat_history)

    prompt = RAG_PROMPT.format(context=context, question=query, history=history_text)
    answer = generate_answer(prompt)

    sources = list({doc.metadata.get("source", "unknown") for doc in relevant_docs})
    return answer, sources