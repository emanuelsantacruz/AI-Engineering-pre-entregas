# SQLAlchemy con Motor Asíncrono

SQLAlchemy 2.0 soporta operaciones no bloqueantes mediante `create_async_engine` y el driver `asyncpg` para PostgreSQL.
Las sesiones de base de datos se manejan mediante `async_sessionmaker`. Las consultas se ejecutan con `await session.execute(select(...))` y se commitean con `await session.commit()`.
