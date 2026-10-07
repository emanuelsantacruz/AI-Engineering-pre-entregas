import asyncio
from rag_system import RAGSystem

async def main():
    rag = RAGSystem()
    pregunta = "¿Qué broker y decorador se usa para encolar tareas con Celery?"

    print(f"Pregunta: {pregunta}\n")
    print("Buscando documentos con recuperador híbrido...")
    docs = rag.get_top_documents(pregunta)
    for i, doc in enumerate(docs, 1):
        print(f"[{i}] Fuente: {doc.metadata.get('source')} (ID: {doc.metadata.get('doc_id')})")

    print("\nGenerando respuesta...")
    respuesta = await rag.answer(pregunta)
    print(f"\nRespuesta:\n{respuesta}")

if __name__ == "__main__":
    asyncio.run(main())
