# Orquestación con Docker Compose

Docker Compose permite definir y correr entornos multi-contenedor mediante un archivo YAML declarativo (`compose.yaml`).
Permite configurar volúmenes persistentes, redes bridge aisladas y directivas de control como `depends_on` con `condition: service_healthy` para asegurar el orden de inicio de los servicios.
