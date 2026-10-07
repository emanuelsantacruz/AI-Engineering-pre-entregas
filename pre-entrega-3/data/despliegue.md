# Protocolo de Despliegue y Release

Los despliegues en DevFlow siguen una estrategia de integración continua (CI/CD) a través de GitHub Actions.

## Ambientes
1. **Desarrollo**: Despliegue automático ante cada push a la rama `dev`.
2. **Staging**: Despliegue automático ante cada pull request aprobado a la rama `main`.
3. **Producción**: Requiere aprobación manual de al menos dos mantenedores y se realiza mediante despliegues Canary graduales (10%, 25%, 50%, 100%).

## Rollback
En caso de tasa de errores 5xx superior al 1% en producción durante los primeros 10 minutos, el script de monitoreo ejecuta automáticamente un rollback a la versión anterior de la imagen de Docker.
