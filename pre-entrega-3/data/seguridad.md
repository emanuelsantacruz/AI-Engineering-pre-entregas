# Políticas de Seguridad e Identidad

La autenticación de usuarios se gestiona mediante tokens JWT firmados con clave asimétrica RS256.

## Expiración y Rotación
- El access token tiene un tiempo de expiración estricto de 15 minutos.
- El refresh token tiene una validez de 7 días y se invalida automáticamente si se detecta uso simultáneo desde distintas IPs.
- Todas las API keys y secretos del sistema deben rotarse cada 90 días calendario.
- El acceso administrativo al clúster requiere autenticación multifactor (MFA) obligatoria y conexión por VPN corporativa WireGuard.
