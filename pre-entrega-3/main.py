import asyncio
import json
from rag import get_rag_response

async def main():
    print("=== TEST 1: Pregunta cuya respuesta está en los documentos ===")
    pregunta_valida = "¿Cuál es el tiempo de expiración de los access tokens y cada cuánto se deben rotar las API keys?"
    print(f"Pregunta: {pregunta_valida}\n")
    
    resp_1 = await get_rag_response(pregunta_valida)
    print("Respuesta:")
    print(json.dumps(resp_1.model_dump(), indent=2, ensure_ascii=False))

    print("\n" + "=" * 50 + "\n")

    print("=== TEST 2: Pregunta trampa (información inexistente) ===")
    pregunta_trampa = "¿Cuál es el presupuesto anual asignado al clúster de servidores?"
    print(f"Pregunta: {pregunta_trampa}\n")

    resp_2 = await get_rag_response(pregunta_trampa)
    print("Respuesta:")
    print(json.dumps(resp_2.model_dump(), indent=2, ensure_ascii=False))

if __name__ == "__main__":
    asyncio.run(main())
