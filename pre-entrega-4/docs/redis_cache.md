# Estrategias de Caché en Redis

Redis se utiliza como almacén de datos en memoria clave-valor para acelerar lecturas frecuentes y reducir carga en la base relacional.
Se recomienda configurar tiempo de expiración (TTL) en cada clave utilizando `redis.set(key, value, ex=300)` para evitar claves huérfanas y desbordamiento de memoria RAM.
