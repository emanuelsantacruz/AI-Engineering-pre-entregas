from typing import Any, Dict
from langchain_core.tools import tool

CLIENTES_DB = {
    "carlos": {"id": 102, "nombre": "Carlos Gómez", "email": "carlos@example.com"},
    "carlos gomez": {"id": 102, "nombre": "Carlos Gómez", "email": "carlos@example.com"},
    "carlos gómez": {"id": 102, "nombre": "Carlos Gómez", "email": "carlos@example.com"},
    "carlos@example.com": {"id": 102, "nombre": "Carlos Gómez", "email": "carlos@example.com"},
}

PEDIDOS_DB = {
    102: {
        "pedidos": 3,
        "total": 14500,
        "historial": [
            {"pedido_id": 1001, "monto": 4500, "fecha": "2024-01-15", "item": "Teclado mecánico"},
            {"pedido_id": 1002, "monto": 5000, "fecha": "2024-02-10", "item": "Mouse inalámbrico"},
            {"pedido_id": 1003, "monto": 5000, "fecha": "2024-03-01", "item": "Auriculares gamer"}
        ]
    }
}

@tool
def buscar_cliente(identificador: str) -> Dict[str, Any]:
    """Busca los datos de un cliente a partir de su nombre o email. Retorna el cliente_id necesario para consultar pedidos o historial."""
    clave = identificador.strip().lower()
    if clave in CLIENTES_DB:
        return CLIENTES_DB[clave]
    return {"error": f"No se encontró ningún cliente con identificador '{identificador}'"}

@tool
def buscar_pedidos(cliente_id: int) -> Dict[str, Any]:
    """Consulta la base de datos de pedidos utilizando el cliente_id numérico. Retorna cantidad de pedidos, monto total y el detalle de cada compra."""
    if cliente_id in PEDIDOS_DB:
        return PEDIDOS_DB[cliente_id]
    return {"error": f"No se registraron pedidos para el cliente con ID {cliente_id}"}

tools = [buscar_cliente, buscar_pedidos]
