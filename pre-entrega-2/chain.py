import os
import logging
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from schemas import EntidadesTecnicas

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "Eres un analista técnico especializado en infraestructura y desarrollo. "
        "Analiza el texto provisto y extrae las tecnologías mencionadas, "
        "el nivel de criticidad (baja, media o alta) y un resumen técnico conciso."
    ),
    ("human", "{texto}")
])

model = ChatOpenAI(
    model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
    temperature=0.0
)

structured_model = model.with_structured_output(EntidadesTecnicas)
chain = (prompt | structured_model).with_retry(stop_after_attempt=3)

async def process_text(texto: str) -> EntidadesTecnicas:
    logger.info("Iniciando procesamiento y validación del texto...")
    try:
        resultado = await chain.ainvoke({"texto": texto})
        logger.info("Procesamiento completado y validado exitosamente.")
        return resultado
    except Exception as e:
        logger.error(f"Error procesando el texto: {e}")
        raise e
