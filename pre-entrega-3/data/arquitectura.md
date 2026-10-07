# Arquitectura del Sistema DevFlow

El sistema DevFlow utiliza una arquitectura de microservicios contenerizados en Docker.
El backend principal está desarrollado en FastAPI y se comunica mediante gRPC con el servicio de procesamiento en segundo plano.

## Almacenamiento y Caché
- La base de datos relacional principal es PostgreSQL 15, configurada en clúster primario-réplica.
- Para caché de consultas frecuentes y control de límites de peticiones (rate limiting) se utiliza una instancia de Redis 7 con política de desalojo volatile-lru.
- Los archivos estáticos y subidas de usuarios se almacenan en buckets compatibles con S3 mediante MinIO.
