import os
from langchain_community.document_loaders import TextLoader, UnstructuredMarkdownLoader, JSONLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
import json

# Paths
VECTOR_DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/vector_db"))
DOCS_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/docs"))

# Initialize Embeddings
embedding_function = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def get_vector_store():
    if not os.path.exists(VECTOR_DB_PATH):
        os.makedirs(VECTOR_DB_PATH)
    return Chroma(
        persist_directory=VECTOR_DB_PATH,
        embedding_function=embedding_function
    )

def load_documents(directory_path):
    documents = []
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        if filename.endswith(".md"):
            loader = UnstructuredMarkdownLoader(file_path)
            documents.extend(loader.load())
        elif filename.endswith(".txt"):
            loader = TextLoader(file_path, encoding='utf-8')
            documents.extend(loader.load())
        elif filename.endswith(".json"):
            # Custom JSON loading might be needed depending on structure, 
            # but for now let's try to load it as text or use a simple loader
            try:
                with open(file_path, 'r') as f:
                    content = f.read()
                documents.append(Document(page_content=content, metadata={"source": filename}))
            except Exception as e:
                print(f"Error loading JSON {filename}: {e}")
        elif filename.endswith(".html"):
             loader = TextLoader(file_path, encoding='utf-8') # Treat HTML as text for now to keep structure
             documents.extend(loader.load())
    return documents

def ingest_docs():
    # 1. Load Documents
    raw_documents = load_documents(DOCS_PATH)
    if not raw_documents:
        return "No documents found to ingest."

    # 2. Split Text
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", " ", ""]
    )
    chunks = text_splitter.split_documents(raw_documents)

    # 3. Add to Vector DB
    vector_store = get_vector_store()
    vector_store.add_documents(chunks)
    
    return f"Successfully ingested {len(chunks)} chunks from {len(raw_documents)} documents."

def query_vector_db(query, k=3):
    vector_store = get_vector_store()
    results = vector_store.similarity_search(query, k=k)
    return results
