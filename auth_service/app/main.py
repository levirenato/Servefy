from contextlib import asynccontextmanager
from fastapi import FastAPI
from .router import router
from .database import engine, Base
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Código de inicialização
    Base.metadata.create_all(bind=engine)
    yield
    # Código de finalização
    engine.dispose()


app = FastAPI(lifespan=lifespan)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/auth")
