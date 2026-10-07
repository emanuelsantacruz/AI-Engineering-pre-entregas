import os
import glob
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_core.documents import Document

load_dotenv()

INDEX_NAME = os.getenv("INDEX_NAME", "rag-index")
DOCS_DIR = os.path.join(os.path.dirname(__file__), "docs")

def init_pinecone_index():
    api_key = os.getenv("PINECONE_API_KEY")
    pc = Pinecone(api_key=api_key)

    existing_indexes = [index.name for index in pc.list_indexes()]
    if INDEX_NAME not in existing_indexes:
        print(f"Creando índice Serverless '{INDEX_NAME}'...")
        pc.create_index(
            name=INDEX_NAME,
            dimension=1536,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1")
        )
        print("Índice creado.")
    else:
        print(f"El índice '{INDEX_NAME}' ya existe.")
    return pc

def load_and_chunk_documents():
    docs = []
    for filepath in glob.glob(os.path.join(DOCS_DIR, "*.md")):
        doc_id = os.path.splitext(os.path.basename(filepath))[0]
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        docs.append(Document(
            page_content=content,
            metadata={"source": os.path.basename(filepath), "doc_id": doc_id, "category": "technical"}
        ))

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)
    return chunks

def run_ingestion():
    init_pinecone_index()
    chunks = load_and_chunk_documents()
    print(f"Cargando {len(chunks)} fragmentos en Pinecone...")

    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vectorstore = PineconeVectorStore.from_documents(
        documents=chunks,
        embedding=embeddings,
        index_name=INDEX_NAME
    )
    print("Ingesta completada exitosamente.")
    return vectorstore

if __name__ == "__main__":
    run_ingestion()
