from typing import List, Literal
from pydantic import BaseModel, Field

class EntidadesTecnicas(BaseModel):
    tecnologias: List[str] = Field(
        min_length=1,
        description="Lista de tecnologías, librerías, bases de datos o servicios mencionados."
    )
    nivel_de_criticidad: Literal["baja", "media", "alta"] = Field(
        description="Criticidad del evento o arquitectura (baja, media, alta)."
    )
    resumen_tecnico: str = Field(
        description="Resumen breve y técnico del texto proporcionado."
    )
