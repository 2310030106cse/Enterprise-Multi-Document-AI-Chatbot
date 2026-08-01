from langchain_core.prompts import PromptTemplate

RAG_PROMPT = PromptTemplate(
    input_variables=["context", "question", "history"],
    template="""You are a helpful enterprise assistant answering questions using ONLY the document context below.
Use the conversation history to understand follow-up questions (like "what about..." or "explain more"), but ground every answer in the document context.
If the answer isn't in the context, say "I couldn't find that in the documents."

Conversation history:
{history}

Document context:
{context}

Question: {question}

Answer:"""
)