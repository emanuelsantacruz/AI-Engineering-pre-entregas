# Pre-entrega 1: Cliente de LLM Robusto y Asíncrono

Este proyecto implementa un cliente asíncrono e intercambiable para interactuar con modelos de lenguaje de OpenAI y Anthropic bajo una interfaz unificada.

## Características

- **Interfaz unificada**: Clases `OpenAIClient` y `AnthropicClient` que heredan de `BaseLLMClient`.
- **Asincronía**: Métodos basados en `async`/`await` utilizando los SDKs oficiales asíncronos (`AsyncOpenAI` y `AsyncAnthropic`).
- **Streaming**: Generador asíncrono con `yield` para recibir tokens en tiempo real.
- **Validación con Pydantic**: Esquemas para mensajes (`ChatMessage`), configuración (`ModelConfig`) y respuestas (`ModelResponse`).
- **Control de errores**: Captura excepciones de red, cuota y rate limiting devolviendo respuestas controladas.

## Estructura del Proyecto

```text
pre-entrega-1/
├── schemas.py       # Modelos de datos con Pydantic
├── clients.py       # Clases de clientes y AsyncLLMManager
├── main.py          # Script de prueba (normal y streaming)
├── requirements.txt # Dependencias del proyecto
├── .env.example     # Ejemplo de variables de entorno
└── .gitignore       # Archivos ignorados por git
```

## Instalación y Configuración

1. Crear y activar un entorno virtual:

```bash
python -m venv venv
# En Windows:
venv\Scripts\activate
# En Linux/macOS:
source venv/bin/activate
```

2. Instalar las dependencias:

```bash
pip install -r requirements.txt
```

3. Configurar las variables de entorno:

Copiar el archivo `.env.example` como `.env` y completar con las API keys correspondientes:

```bash
cp .env.example .env
```

Variables requeridas en `.env`:
- `OPENAI_API_KEY`: Clave de API de OpenAI.
- `ANTHROPIC_API_KEY`: Clave de API de Anthropic (opcional si se usa OpenAI).
- `LLM_PROVIDER`: Proveedor por defecto (`openai` o `anthropic`).

## Ejecución

Para correr el script de prueba:

```bash
python main.py
```

El script consultará "¿Qué es la entropía?" primero en modo normal y luego utilizando streaming.
