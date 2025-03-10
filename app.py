from contextlib import asynccontextmanager

from fastapi import FastAPI

from config.config import logger
from core.routers import router
from queries.orm import TablesOrm


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info('Запуск приложения')
    await TablesOrm.drop_tables()
    logger.info('База очищена')
    await TablesOrm.create_tables()
    logger.info('База готова к работе')
    yield
    logger.info('Завершение работы')


app = FastAPI(lifespan=lifespan)
app.include_router(router)

# if __name__ == '__main__':
#     import uvicorn
#     uvicorn.run('app:app', host='0.0.0.0', port=8000)

