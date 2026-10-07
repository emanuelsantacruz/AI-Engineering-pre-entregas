# Pre-entrega 5: Agente de Razonamiento Cíclico con Memoria Persistente

Implementación de un agente autónomo de razonamiento cíclico (ReAct) con memoria persistente utilizando LangGraph, LangChain y `SqliteSaver`.

## Criterios Cumplidos

- **Autonomía**: El modelo decide cuándo ejecutar herramientas basándose en sus docstrings, utilizando `tools_condition` sin estructuras `if/else` manuales.
- **Ciclo de Retorno y Multi-paso**: Permite invocar herramientas en serie para resolver preguntas complejas (ej. buscar cliente por nombre para obtener su ID y luego consultar sus pedidos).
- **Persistencia de Sesión**: Utiliza `SqliteSaver` con `thread_id` para recordar el contexto de turnos anteriores en una conversación continua.
- **Control de Recursión**: Configurado con `recursion_limit: 10` para prevenir bucles infinitos.
- **Traza ReAct**: Registro estructurado en `trace_react.json`.

## Estructura del Proyecto

```text
pre-entrega-5/
├── tools.py          # Herramientas decoradas con @tool y docstrings
├── agent.py          # StateGraph con MessagesState, ToolNode y SqliteSaver
├── main.py           # Script de prueba multi-paso y persistencia
├── trace_react.json  # Traza de ejecución del razonamiento cíclico
├── requirements.txt  # Dependencias del proyecto
├── .env.example      # Plantilla de variables de entorno
└── .gitignore        # Archivos ignorados por git
```

## Instalación y Configuración

1. Crear y activar entorno virtual:

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate
```

2. Instalar dependencias:

```bash
pip install -r requirements.txt
```

3. Configurar variables de entorno:

```bash
cp .env.example .env
```

Configurar la variable `OPENAI_API_KEY` en el archivo `.env`.

## Ejecución

Para correr la prueba del agente:

```bash
python main.py
```

El script ejecutará:
1. Una consulta multi-paso: `"¿Cuántos pedidos tuvo el cliente Carlos Gómez y cuál fue el total?"` (invoca `buscar_cliente` y luego `buscar_pedidos`).
2. Una repregunta en la misma sesión (`thread_id`): `"¿Y cuál fue el último producto que compró en su historial?"` (responde utilizando el historial en memoria).
3. Guardará la traza ReAct en `trace_react.json`.

## Ejemplo de Traza ReAct (`trace_react.json`)

```json
[
  {
    "rol": "usuario",
    "contenido": "¿Cuántos pedidos tuvo el cliente Carlos Gómez y cuál fue el total?"
  },
  {
    "tipo": "tool_call",
    "herramienta": "buscar_cliente",
    "argumentos": {
      "identificador": "Carlos Gómez"
    }
  },
  {
    "tipo": "tool_response",
    "contenido": "{\"id\": 102, \"nombre\": \"Carlos Gómez\", \"email\": \"carlos@example.com\"}"
  },
  {
    "tipo": "tool_call",
    "herramienta": "buscar_pedidos",
    "argumentos": {
      "cliente_id": 102
    }
  },
  {
    "tipo": "tool_response",
    "contenido": "{\"pedidos\": 3, \"total\": 14500, ...}"
  },
  {
    "rol": "asistente",
    "respuesta": "El cliente Carlos Gómez (ID 102) tuvo un total de 3 pedidos por un monto acumulado de $14.500."
  }
]
```
