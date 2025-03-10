import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import patch, MagicMock
from app import app
from queries.orm import PasswordOrm


# мок для работы с базой данных
@pytest.fixture
def mock_password_orm():
    with patch.object(PasswordOrm, 'add_password') as mock_add_password, \
            patch.object(PasswordOrm, 'get_password') as mock_get_password, \
            patch.object(PasswordOrm, 'search_password') as mock_search_password:
        yield mock_add_password, mock_get_password, mock_search_password


# добавление пароля
@pytest.mark.asyncio
async def test_post_password(mock_password_orm):
    mock_add_password, mock_get_password, mock_search_password = mock_password_orm

    # имитация модели PasswordModel
    mock_password = MagicMock()
    mock_password.service_name = 'google'
    mock_password.password = '1875'

    mock_add_password.return_value = mock_password

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post('/password/google', json={'password': '1875'})

        assert response.status_code == 200
        data = response.json()
        assert data == {'password': '1875', 'service_name': 'google'}


# получение пароля по имени сервиса
@pytest.mark.asyncio
async def test_get_password(mock_password_orm):
    mock_add_password, mock_get_password, mock_search_password = mock_password_orm

    mock_get_password.return_value = {"service_name": "google", "password": "1875"}

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get('/password/google')

    assert response.status_code == 200
    data = response.json()
    assert data == {'password': '1875', 'service_name': 'google'}


# получение пароля которого нет в базе
@pytest.mark.asyncio
async def test_get_no_password(mock_password_orm):
    mock_add_password, mock_get_password, mock_search_password = mock_password_orm

    mock_get_password.return_value = None

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get('/password/no_service')

    assert response.status_code == 200
    data = response.json()
    assert data == {'error': 'Пароль не найден'}


# поиск паролей по части имени
@pytest.mark.asyncio
async def test_search_password(mock_password_orm):
    mock_add_password, mock_get_password, mock_search_password = mock_password_orm

    mock_search_password.return_value = [
        {"service_name": "google", "password": "1875"},
    ]

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get('/password/', params={'service_name': 'go'})

    assert response.status_code == 200
    data = response.json()

    assert len(data) == 1
    assert data[0]["service_name"] == "google"
    assert data[0]["password"] == "1875"


# поиск несуществующих паролей
@pytest.mark.asyncio
async def test_search_no_password(mock_password_orm):
    mock_add_password, mock_get_password, mock_search_password = mock_password_orm

    mock_search_password.return_value = []

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get('/password/', params={'service_name': 'no_service'})

    assert response.status_code == 200
    data = response.json()
    assert data == []
