from fastapi import APIRouter

from config.config import logger
from queries.orm import PasswordOrm
from core.schemas import AddPasswordSchema

router = APIRouter(
    prefix='/password',
    tags=['Пароли'],
)


@router.post('/{service_name}', summary='Добавление пароля')
async def add_password_manager(
        service_name: str,
        data: AddPasswordSchema
):
    """
        создает, обновляет пароль для указанного сервиса

        arg:
            service_name (str): название сервиса,
            data (AddPasswordSchema): объект с переданным паролем.

    """
    logger.info(f'Запрос на добавление пароля: {service_name}')
    password_data = await PasswordOrm.add_password(service_name, data.password)
    logger.info(f'Пароль добавлен для сервиса {service_name}')

    return {
        "password": data.password,
        "service_name": password_data.service_name,
    }


@router.get('/{service_name}', summary='Получение пароля')
async def get_password_manager(service_name: str):
    """
        получает пароль для указанного сервиса

        arg:
            service_name (str): название сервиса.

    """
    password_data = await PasswordOrm.get_password(service_name)

    if password_data:
        logger.info(f'Получен пароль для сервиса {service_name}')
        return password_data
    else:
        logger.info(f'Пароль не найден')
        return {"error": "Пароль не найден"}


@router.get('/', summary='Поиск паролей по части имени сервиса')
async def search_password_manager(service_name: str):
    """
        Ищет пароли по частичному совпадению названия сервиса.

        arg:
            service_name (str): Часть названия сервиса для поиска.

        return:
            list: cписок найденных паролей с сервисами или пустой список.
    """
    password_data = await PasswordOrm.search_password(service_name)

    if password_data:
        logger.info(f'Найдены совпадения для {service_name}')
    else:
        logger.info(f'Совпадения не найдены для {service_name}')

    return password_data



