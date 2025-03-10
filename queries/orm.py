from sqlalchemy import select

from config.config import settings
from core.crypto import encrypt_password, decrypt_password
from core.database import async_engine, async_session_factory, Base
from core.models import PasswordModel


class TablesOrm:
    # создание таблиц
    @classmethod
    async def create_tables(cls):
        async with async_engine.begin() as connect:
            await connect.run_sync(Base.metadata.create_all)

    # удаление таблиц
    @classmethod
    async def drop_tables(cls):
        async with async_engine.begin() as connect:
            await connect.run_sync(Base.metadata.drop_all)


class PasswordOrm:
    # создание, обновление пароля
    @classmethod
    async def add_password(cls, service_name: str, password: str):
        async with async_session_factory() as session:
            encrypted_password = encrypt_password(password, settings.SECRET_KEY.encode())

            existing_password = await session.execute(
                select(PasswordModel).filter(PasswordModel.service_name == service_name)
            )
            existing_password = existing_password.scalar_one_or_none()

            # проверяеем существование пароля
            if existing_password:
                existing_password.password = encrypted_password
            else:
                password_entry = PasswordModel(service_name=service_name,
                                               password=encrypted_password)
                session.add(password_entry)

            await session.commit()

            return existing_password if existing_password else password_entry

    # получение пароля
    @classmethod
    async def get_password(cls, service_name: str):
        async with async_session_factory() as session:
            query = select(PasswordModel).filter(PasswordModel.service_name == service_name)
            result = await session.execute(query)
            password_model = result.scalars().first()

            # если пароль существует, то дешифруем его
            if password_model:
                decrypted_password = decrypt_password(password_model.password, settings.SECRET_KEY.encode())
                return {"password": decrypted_password, "service_name": password_model.service_name}

            return None

    # получение паролей по части сервиса
    @classmethod
    async def search_password(cls, part_of_service_name: str):
        async with async_session_factory() as session:
            query = select(PasswordModel).filter(PasswordModel.service_name.ilike(f"%{part_of_service_name}%"))
            result = await session.execute(query)
            password_models = result.scalars().all()

            if not password_models:
                return []

            return [
                {
                    "password": decrypt_password(model.password, settings.SECRET_KEY.encode()),
                    "service_name": model.service_name,
                }
                for model in password_models
            ]
