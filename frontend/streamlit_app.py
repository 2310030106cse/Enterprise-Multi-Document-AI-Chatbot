import streamlit as st
import sys, os, tempfile

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.chatbot import process_document, chat, get_documents, remove_document, reset_index

st.set_page_config(page_title="Multi-Document AI Chatbot", layout="wide", page_icon="📚")
st.title("📚 Enterprise Multi-Document AI Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.header("📁 Documents")

    uploaded_files = st.file_uploader(
        "Upload PDF, DOCX, or TXT files",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True
    )
    if st.button("⬆️ Process Documents", use_container_width=True) and uploaded_files:
        with st.spinner("Indexing documents..."):
            for file in uploaded_files:
                with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.name)[1]) as tmp:
                    tmp.write(file.read())
                    tmp_path = tmp.name
                n_chunks = process_document(tmp_path, original_filename=file.name)
                st.success(f"{file.name}: {n_chunks} chunks indexed")
        st.rerun()

    st.divider()
    st.subheader("Indexed documents")
    docs = get_documents()
    if not docs:
        st.caption("No documents indexed yet.")
    else:
        for source, count in docs.items():
            col1, col2 = st.columns([4, 1])
            col1.markdown(f"**{source}**  \n`{count} chunks`")
            if col2.button("🗑️", key=f"del_{source}", help=f"Remove {source}"):
                remove_document(source)
                st.rerun()

    st.divider()
    if st.button("🔄 Reset entire index", use_container_width=True):
        reset_index()
        st.session_state.messages = []
        st.rerun()

    st.divider()
    if st.button("🧹 Clear chat history", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant" and msg.get("sources"):
            st.caption(f"📄 Sources: {', '.join(msg['sources'])}")

if query := st.chat_input("Ask something about your documents..."):
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    history_pairs = []
    msgs = st.session_state.messages[:-1]
    for i in range(0, len(msgs) - 1, 2):
        if msgs[i]["role"] == "user" and msgs[i + 1]["role"] == "assistant":
            history_pairs.append({"user": msgs[i]["content"], "assistant": msgs[i + 1]["content"]})

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            answer, sources = chat(query, chat_history=history_pairs)
            st.markdown(answer)
            if sources:
                st.caption(f"📄 Sources: {', '.join(sources)}")
    st.session_state.messages.append({"role": "assistant", "content": answer, "sources": sources})