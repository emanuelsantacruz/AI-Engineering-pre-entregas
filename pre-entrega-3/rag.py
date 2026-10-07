import os
from typing import List
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from ingest import ingest_documents

load_dotenv()

class RAGResponse(BaseModel):
    respuesta: str = Field(description="Respuesta redactada a partir exclusivamente del contexto provisto.")
    referencias: List[str] = Field(description="Lista de archivos o fuentes utilizadas para responder.")

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "Eres un asistente técnico. Responde la pregunta del usuario utilizando "
        "ÚNICA Y EXCLUSIVAMENTE el siguiente contexto:\n\n"
        "{contexto}\n\n"
        "Reglas obligatorias:\n"
        "1. Si la respuesta no está presente en el contexto, di explícitamente 'No lo sé' o 'No tengo información sobre este tema en los documentos'.\n"
        "2. No agregues conocimiento externo ni supongas información que no esté en el texto."
    ),
    ("human", "{pregunta}")
])

async def get_rag_response(query: str) -> RAGResponse:
    vectorstore = ingest_documents(force=False)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    docs = await retriever.ainvoke(query)

    context_parts = []
    fuentes = set()
    for doc in docs:
        context_parts.append(doc.page_content)
        fuente = doc.metadata.get("source", "desconocido")
        fuentes.add(os.path.basename(fuente))

    contexto_str = "\n\n---\n\n".join(context_parts)

    model = ChatOpenAI(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        temperature=0.0
    )
    chain = prompt | model.with_structured_output(RAGResponse)

    resultado = await chain.ainvoke({
        "contexto": contexto_str,
        "pregunta": query
    })

    if "no lo sé" in resultado.respuesta.lower() or "no tengo información" in resultado.respuesta.lower():
        resultado.referencias = []
    elif not resultado.referencias:
        resultado.referencias = list(fuentes)

    return resultado
