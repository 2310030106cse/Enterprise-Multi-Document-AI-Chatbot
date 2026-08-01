from langchain_community.document_loaders import Docx2txtLoader

def load_docx(file_path: str):
    loader = Docx2txtLoader(file_path)
    docs = loader.load()
    text = "\n".join([doc.page_content for doc in docs])
    return text