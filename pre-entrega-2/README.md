# Pre-entrega 2: Pipeline de Procesamiento Validado

Pipeline de extracción de entidades técnicas a partir de texto no estructurado utilizando LangChain (LCEL) y Pydantic.

## Componentes

- **Esquema Pydantic (`schemas.py`)**: Modelo `EntidadesTecnicas` con validación de tecnologías detectadas, nivel de criticidad (`baja`, `media`, `alta`) y resumen técnico.
- **Cadena LCEL (`chain.py`)**: Composición modular usando `ChatPromptTemplate`, `ChatOpenAI`, `.with_structured_output()` y reintentos automáticos con `.with_retry()`.
- **Ejecución Asíncrona**: Función `process_text()` con `.ainvoke()` y registro de logs.

## Estructura del Proyecto

```text
pre-entrega-2/
├── schemas.py       # Modelo Pydantic
├── chain.py         # Cadena LCEL y función process_text()
├── main.py          # Script de prueba asíncrono
├── requirements.txt # Dependencias
├── .env.example     # Variables de entorno
└── .gitignore       # Archivos ignorados por git
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

3. Configurar `.env`:

```bash
cp .env.example .env
```

Configurar la variable `OPENAI_API_KEY`.

## Ejecución

Para ejecutar la prueba del pipeline:

```bash
python main.py
```

## Ejemplo de Salida

```json
{
  "tecnologias": [
    "FastAPI",
    "Redis",
    "PostgreSQL"
  ],
  "nivel_de_criticidad": "alta",
  "resumen_tecnico": "Caída en producción por alto consumo de memoria en Redis y saturación de conexiones en PostgreSQL afectando transacciones de la API FastAPI."
}
```
