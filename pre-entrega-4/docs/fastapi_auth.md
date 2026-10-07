# Autenticación en FastAPI

FastAPI implementa esquemas OAuth2 mediante `OAuth2PasswordBearer`. Para la generación de tokens se utiliza `python-jose` y cifrado HS256 o RS256.
Los endpoints protegidos reciben la dependencia `Depends(get_current_user)` la cual valida la firma del token y extrae los claims del usuario.
