from contextlib import asynccontextmanager

from fastapi import FastAPI

from config.config import logger
from core.routers import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info('Запуск приложения')
    yield
    logger.info('Завершение работы')


app = FastAPI(lifespan=lifespan)
app.include_router(router)

