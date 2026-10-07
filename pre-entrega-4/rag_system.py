import os
from typing import List
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_pinecone import PineconeVectorStore
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from ingest import INDEX_NAME, load_and_chunk_documents

load_dotenv()

class RAGSystem:
    def __init__(self):
        chunks = load_and_chunk_documents()
        self.bm25_retriever = BM25Retriever.from_documents(chunks)
        self.bm25_retriever.k = 5

        embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        self.vectorstore = PineconeVectorStore.from_existing_index(
            index_name=INDEX_NAME,
            embedding=embeddings
        )
        self.vector_retriever = self.vectorstore.as_retriever(search_kwargs={"k": 5})

        self.ensemble_retriever = EnsembleRetriever(
            retrievers=[self.bm25_retriever, self.vector_retriever],
            weights=[0.5, 0.5]
        )

        prompt = ChatPromptTemplate.from_messages([
            ("system", "Responde la pregunta basándote únicamente en el contexto:\n\n{contexto}"),
            ("human", "{pregunta}")
        ])
        model = ChatOpenAI(model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"), temperature=0.0)
        self.chain = prompt | model | StrOutputParser()

    def get_top_documents(self, query: str) -> List[Document]:
        return self.ensemble_retriever.invoke(query)[:5]

    async def answer(self, query: str) -> str:
        docs = self.get_top_documents(query)
        contexto = "\n\n".join([d.page_content for d in docs])
        return await self.chain.ainvoke({"contexto": contexto, "pregunta": query})
