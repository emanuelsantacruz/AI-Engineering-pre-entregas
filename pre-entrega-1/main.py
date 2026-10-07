import asyncio
import os
from dotenv import load_dotenv

from schemas import ChatMessage, ModelConfig
from clients import AsyncLLMManager

load_dotenv()

async def main():
    provider = os.getenv("LLM_PROVIDER", "openai")
    print(f"--- Iniciando prueba con proveedor: {provider} ---\n")

    manager = AsyncLLMManager(provider=provider)

    messages = [
        ChatMessage(role="user", content="¿Qué es la entropía?")
    ]

    model_name = "gpt-4o-mini" if provider == "openai" else "claude-3-haiku-20240307"
    config = ModelConfig(model=model_name, temperature=0.7, max_tokens=200)

    print("1. Modo Normal (generate):")
    response = await manager.generate(messages, config)
    if response.error:
        print(f"Error: {response.error}")
    else:
        print(f"Respuesta ({response.model}):\n{response.content}")
        print(f"Tokens usados: {response.tokens_used}")

    print("\n" + "=" * 40 + "\n")

    print("2. Modo Streaming (stream):")
    print("Respuesta: ", end="", flush=True)
    async for chunk in manager.stream(messages, config):
        print(chunk, end="", flush=True)
    print("\n\n--- Fin de la prueba ---")

if __name__ == "__main__":
    asyncio.run(main())
