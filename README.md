Менеджер паролей

Описание

Данный проект представляет собой API для управления паролями, привязанными к названию сервиса.API позволяет:

🔐 Добавлять/обновлять пароль для конкретного сервиса.

🔓 Получать пароль по названию сервиса.

🔎 Искать пароли по частичному совпадению названия сервиса.

Пароли хранятся в зашифрованном виде, а сам проект разворачивается с использованием Docker Compose.

📂 Структура проекта
<pre>
.
├── app.py              # Точка входа в приложение
├── config             
│   ├── config.py       # Конфигурация приложения
├── core
│   ├── database.py     # Настройка подключения к БД
│   ├── models.py       # Описание модели паролей
│   ├── schemas.py      # Pydantic-схемы
│   ├── routers.py      # Основные ручки API
├── queries
│   ├── orm.py          # Запросы через orm к базе
├── tests
│   ├── __init__.py     
│   ├── test_api.py     # Тесты API
├── Dockerfile          # Образ для приложения
├── docker-compose.yml  # Компоновка сервисов Docker
├── .env                # Переменные окружения
└── requirements.txt    # Зависимости проекта
</pre>

✅ Как запустить проект

1. Клонировать репозиторий 
<pre>
git clone ссылка на репозиторий
cd название папки
</pre>

2. Заполнить файл .env

Создайте файл .env в корне проекта и добавьте туда такие переменные:

.env:

    DB_NAME=password_manager
    DB_USER=postgres
    DB_PASS=postgres
    DB_HOST=db
    DB_PORT=5432

    SECRET_KEY=supersecretkey

Воспользуйте функцией generate_key() из файла core/сrypto.py,
чтобы получить SECRET_KEY

3. Запустить проект

Для запуска всех сервисов используйте команду:
<pre>
docker-compose up --build
</pre>
После запуска:

База данных будет доступна на порту: 5432

FastAPI-приложение будет доступно на порту: 8000

🔥 Проверка API

После запуска вы можете протестировать API с помощью Postman, cURL или открыть встроенную документацию.

📄 Swagger документация

После запуска откройте:👉 http://localhost:8000/docs

🚀 Примеры запросов

1. Добавить/обновить пароль для сервиса

POST /password/{service_name}
<pre>
curl -X POST "http://localhost:8000/password/google" \
-H "Content-Type: application/json" \
-d '{
  "password": "very_secret_pass"
}'
</pre>

Ответ:

<pre>{
  "password": "very_secret_pass", 
  "service_name": "google"
}
</pre>

2. Получить пароль по названию сервиса

GET /password/{service_name}
<pre>
curl -X GET "http://localhost:8000/password/google"
</pre>
Ответ:
<pre>
{
  "password": "very_secret_pass",
  "service_name": "google"
}
</pre>
3. Найти пароли по части имени сервиса

GET /password/?service_name=goo
<pre>
curl -X GET "http://localhost:8000/password/?service_name=goo"
</pre>
Ответ:
<pre>
[
  {
    "password": "very_secret_pass",
    "service_name": "google"
  }
]
</pre>
