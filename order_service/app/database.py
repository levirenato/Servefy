from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

Base = declarative_base()

# URL do banco de dados
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql+asyncpg://user:password@db:5432/auth_service_db"
)

# Configuração do motor assíncrono
engine = create_async_engine(DATABASE_URL, future=True, echo=True)

# Criação do sessionmaker com AsyncSession
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, class_=AsyncSession  # Remove o bind aqui
)


async def init_db():
    # Inicializa o banco de dados
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
