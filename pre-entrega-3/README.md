# Pre-entrega 3: Sistema de Recuperación Semántica Local (RAG)

Implementación de un flujo RAG (Retrieval-Augmented Generation) end-to-end local utilizando ChromaDB, LangChain y modelos de OpenAI.

## Componentes

- **Dataset (`data/`)**: 3 documentos de especificación técnica interna (`arquitectura.md`, `despliegue.md`, `seguridad.md`).
- **Módulo de Ingesta (`ingest.py`)**: Carga los archivos markdown, aplica `RecursiveCharacterTextSplitter` (fragmentos de 500 caracteres y 50 de solapamiento) y persiste los embeddings en un directorio local de ChromaDB (`./vectorstore`).
- **Módulo RAG (`rag.py`)**: Recuperador con búsqueda por similitud ($k=3$), prompt estricto contra alucinaciones y salida estructurada con Pydantic (`RAGResponse` con respuesta y fuentes).
- **Pruebas (`main.py`)**: Script asíncrono que evalúa una consulta válida y una pregunta trampa para verificar que el modelo no alucine.

## Estructura del Proyecto

```text
pre-entrega-3/
├── data/                    # Dataset de prueba (.md)
│   ├── arquitectura.md
│   ├── despliegue.md
│   └── seguridad.md
├── ingest.py                # Script de indexación y persistencia
├── rag.py                   # Cadena RAG y función get_rag_response()
├── main.py                  # Script de pruebas asíncrono
├── requirements.txt         # Dependencias
├── .env.example             # Variables de entorno de ejemplo
└── .gitignore               # Ignorados de Git
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

1. Opcional: Ejecutar la ingesta de documentos de forma independiente (se ejecuta automáticamente si no existe la base vectorial):

```bash
python ingest.py
```

2. Ejecutar las pruebas del sistema RAG:

```bash
python main.py
```

## Ejemplo de Salidas

### 1. Pregunta válida (Información existente)
```json
{
  "respuesta": "Los access tokens tienen un tiempo de expiración estricto de 15 minutos, y todas las API keys y secretos del sistema deben rotarse cada 90 días calendario.",
  "referencias": [
    "seguridad.md"
  ]
}
```

### 2. Pregunta trampa (Información inexistente)
```json
{
  "respuesta": "No lo sé. La información sobre el presupuesto anual del clúster de servidores no se encuentra en los documentos proporcionados.",
  "referencias": []
}
```
