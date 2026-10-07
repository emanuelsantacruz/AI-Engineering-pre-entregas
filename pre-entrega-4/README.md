# Pre-entrega 4: Sistema RAG Escalable en la Nube con Pinecone

Módulo de recuperación híbrida (BM25 + Pinecone Serverless) y evaluación cuantitativa de recuperación con métricas Recall@k y Precision@k.

## Componentes

- **Dataset Técnico (`docs/`)**: 5 documentos en Markdown sobre herramientas de backend (`fastapi_auth.md`, `celery_tasks.md`, `sqlalchemy_async.md`, `redis_cache.md`, `docker_compose.md`).
- **Pipeline de Ingesta (`ingest.py`)**: Crea automáticamente el índice Serverless en Pinecone (dimensión 1536, métrica coseno) si no existe, divide los documentos en fragmentos con `RecursiveCharacterTextSplitter` y los carga con metadatos completos (`doc_id`, `source`, `category`).
- **Recuperador Híbrido (`rag_system.py`)**: Clase `RAGSystem` que integra `EnsembleRetriever` combinando búsqueda por palabras clave (`BM25Retriever`) y búsqueda vectorial (`PineconeVectorStore`).
- **Evaluación (`evaluate.py`)**: Valida un Golden Set de 5 consultas técnicas y calcula `Recall@5` y `Precision@5`.
- **Script de Prueba (`main.py`)**: Ejecuta una consulta de ejemplo e imprime las fuentes y la respuesta generada.

## Estructura del Proyecto

```text
pre-entrega-4/
├── docs/                 # Documentos de prueba
├── golden_set.json       # Preguntas y doc_id esperados
├── ingest.py             # Setup de índice e ingesta a Pinecone
├── rag_system.py         # Clase RAG con EnsembleRetriever
├── evaluate.py           # Script de cálculo de métricas
├── main.py               # Prueba de consulta
├── requirements.txt      # Dependencias
├── .env.example          # Plantilla de variables de entorno
└── .gitignore            # Ignorados de git
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

3. Configurar variables de entorno en `.env`:

```bash
cp .env.example .env
```

Variables requeridas:
- `OPENAI_API_KEY`: Clave de OpenAI.
- `PINECONE_API_KEY`: Clave de API de Pinecone.
- `INDEX_NAME`: Nombre del índice (ej. `rag-index`).

## Replicación del Índice e Ingesta

Para crear el índice en Pinecone e indexar los documentos:

```bash
python ingest.py
```

## Evaluación de Métricas

Para ejecutar la evaluación contra el Golden Set:

```bash
python evaluate.py
```

### Resultados de Evaluación Obtenidos

```text
=============================================
REPORTE DE EVALUACIÓN
=============================================
Total de consultas: 5
Aciertos en Top-5:  5/5
Recall@5:           100.00%
Precision@5:        20.00%
=============================================
```
*(Precision@5 es 20% ya que cada consulta tiene exactamente 1 documento relevante entre los 5 recuperados).*
