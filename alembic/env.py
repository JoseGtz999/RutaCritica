from logging.config import fileConfig
from sqlalchemy import pool, create_engine
from app.database import Base
from app.models.proyecto_db import ProyectoDB
from app.models.hito_db import HitoDB
from app.models.tarea_db import TareaDB
from app.models.subtarea_db import SubtareaDB
from alembic import context

# Configuración de Alembic
config = context.config

# Leer el archivo de configuración para el logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Añadir los modelos para 'autogenerate'
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Ejecutar migraciones en modo 'offline'."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Ejecutar migraciones en modo 'online'."""
    # Usamos el motor sincrónico
    connectable = create_engine(config.get_main_option("sqlalchemy.url"), poolclass=pool.NullPool)

    # Establecer la conexión sincrónica
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with connection.begin():
            context.run_migrations()

# Lógica para ejecutar en modo offline o online
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
