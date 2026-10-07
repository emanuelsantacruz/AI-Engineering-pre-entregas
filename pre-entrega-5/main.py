import asyncio
import json
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from agent import create_agent

async def run_step(app, user_input: str, config: dict, trace: list):
    print(f"\nUsuario: \"{user_input}\"")
    trace.append({"rol": "usuario", "contenido": user_input})

    inputs = {"messages": [HumanMessage(content=user_input)]}

    async for chunk in app.astream(inputs, config=config, stream_mode="values"):
        last_message = chunk["messages"][-1]

    for msg in chunk["messages"]:
        if isinstance(msg, AIMessage) and msg.tool_calls:
            for tc in msg.tool_calls:
                call_info = f"Uso de herramienta: {tc['name']}({tc['args']})"
                print(f"  -> {call_info}")
                trace.append({"tipo": "tool_call", "herramienta": tc["name"], "argumentos": tc["args"]})
        elif isinstance(msg, ToolMessage):
            tool_res = f"Resultado de herramienta: {msg.content}"
            print(f"  -> {tool_res}")
            trace.append({"tipo": "tool_response", "contenido": msg.content})
        elif isinstance(msg, AIMessage) and not msg.tool_calls and msg == chunk["messages"][-1]:
            print(f"Respuesta: \"{msg.content}\"")
            trace.append({"rol": "asistente", "respuesta": msg.content})

async def main():
    app = create_agent()
    config = {
        "configurable": {"thread_id": "sesion_cliente_102"},
        "recursion_limit": 10
    }
    trace_log = []

    print("=== INICIO DE PRUEBA: AGENTE CÍCLICO CON PERSISTENCIA ===")

    print("\n--- Interacción 1: Razonamiento Multi-paso ---")
    await run_step(
        app,
        "¿Cuántos pedidos tuvo el cliente Carlos Gómez y cuál fue el total?",
        config,
        trace_log
    )

    print("\n--- Interacción 2: Memoria Persistente (mismo thread_id) ---")
    await run_step(
        app,
        "¿Y cuál fue el último producto que compró en su historial?",
        config,
        trace_log
    )

    with open("trace_react.json", "w", encoding="utf-8") as f:
        json.dump(trace_log, f, indent=2, ensure_ascii=False)

    print("\nTraza completa guardada exitosamente en 'trace_react.json'.")

if __name__ == "__main__":
    asyncio.run(main())
