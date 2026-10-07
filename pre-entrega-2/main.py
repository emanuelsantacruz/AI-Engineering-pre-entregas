import asyncio
import json
from chain import process_text

async def main():
    ejemplo_texto = (
        "Se detectaron múltiples errores 504 en la API desarrollada con FastAPI. "
        "El clúster de Redis alcanzó el 98% de consumo de memoria y la base de datos "
        "PostgreSQL empezó a rechazar conexiones concurrentes en producción, "
        "afectando las transacciones de pago."
    )

    print("--- Texto de entrada ---")
    print(ejemplo_texto)
    print("\n--- Ejecutando pipeline LCEL ---")

    resultado = await process_text(ejemplo_texto)

    print("\n--- Resultado validado (Pydantic / JSON) ---")
    print(json.dumps(resultado.model_dump(), indent=2, ensure_ascii=False))

if __name__ == "__main__":
    asyncio.run(main())
