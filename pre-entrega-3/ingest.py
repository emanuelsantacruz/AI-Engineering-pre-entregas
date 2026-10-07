import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

load_dotenv()

PERSIST_DIR = os.path.join(os.path.dirname(__file__), "vectorstore")
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

def get_embeddings():
    return OpenAIEmbeddings(model="text-embedding-3-small")

def ingest_documents(force: bool = False) -> Chroma:
    embeddings = get_embeddings()

    if os.path.exists(PERSIST_DIR) and os.listdir(PERSIST_DIR) and not force:
        print(f"Base vectorial ya existente encontrada en '{PERSIST_DIR}'. Cargando...")
        return Chroma(persist_directory=PERSIST_DIR, embedding_function=embeddings)

    print(f"Indexando documentos desde '{DATA_DIR}'...")
    loader = DirectoryLoader(DATA_DIR, glob="**/*.md", loader_cls=TextLoader, loader_kwargs={"encoding": "utf-8"})
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=PERSIST_DIR
    )
    print(f"Indexación completada: {len(chunks)} fragmentos guardados en '{PERSIST_DIR}'.")
    return vectorstore

if __name__ == "__main__":
    ingest_documents(force=True)
