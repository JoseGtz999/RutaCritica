from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings  # Usa la instancia `settings` en lugar de la clase `Settings`

# Crea el motor asincrónico
engine = create_async_engine(settings.DATABASE_URL, echo=True, future=True)  # Aquí se usa `settings.DATABASE_URL`

# Define el modelo base para los modelos de datos
Base = declarative_base()

# Configura el sessionmaker para usar AsyncSession
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Dependencia para obtener la sesión de base de datos
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
