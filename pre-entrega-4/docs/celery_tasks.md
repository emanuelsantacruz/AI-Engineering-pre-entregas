# Tareas Asíncronas con Celery

Celery es una cola de tareas distribuida enfocada en operaciones en tiempo real y tareas programadas periódicas (Celery Beat).
Utiliza Redis o RabbitMQ como message broker para encolar mensajes y almacena los resultados en el result backend configurado. Las tareas se definen con el decorador `@celery_app.task`.
