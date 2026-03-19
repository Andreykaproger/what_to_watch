# 🎞️ What to Watch (WHW) 

Веб-приложение и API для публикации и модерации пользовательских мнений о фильмах.

## Возможности 

### Пользователи 👥

- Регистрация и авторизация
- Просмотр мнений о фильмах
- Добавление, редактирование и удаление своих мнений
- Просмотр профиля

### Администратор 👮

- Модерация мнений (принятие/отклонение)
- Блокировка и разблокировка пользователей
- Просмотр статистики

### API 🤖

- JWT-аутентификация (access + refresh tokens
- CRUD для мнений
- Админ API
- Документация через APIFlask (Swagger / ReDoc)

## Технологии 🧑‍💻

- Python 3.11+
- Flask / APIFlask
- SQLAlchemy
- Flask-Login
- Flask-JWT-Extended
- PostgreSQL / SQLite
- Pytest

## Установка проекта ⬆️

#### 1. Клонирование репозитория

```
git clone https://github.com/Andreykaproger/what_to_watch.git 
cd what-to-watch
```
#### 2. Создание виртуального окружения

``python -m venv venv``


#####  Активировать

Windows

`` venv\Scripts\activate ``

Linux / Mac

`` source venv/bin/activate ``

#### 3. Установка зависимостей 🧑‍🏭

``` 
python3 -m pip install --upgrade pip
pip install -r requirements.txt 
```

## Настройка окружения ⚙️

Нужно создать файл ``.env`` в корне проекта и указать в нем следующие параметры:

```
FLASK_APP=opinions_app
SECRET_KEY=your_secret_key
JWT_SECRET_KEY=your_jwt_secret_key
SQLALCHEMY_DATABASE_URI=sqlite:///app.db
```

Для PostgreSQL:

`SQLALCHEMY_DATABASE_URI=postgresql://user:password@localhost/db_name`


## Работа с базой данных 🗄️
1. Инициализация миграций

`flask db init`

2. Создание миграции

`flask db migrate -m "Commit message"`

3. Применение миграции

`flask db upgrade`

## Запуск приложения 🤘

`flask run`

Приложение будет доступно

`http://127.0.0.1:5000/`

## API документация 📄

Swagger:

`http://127.0.0.1:5000/api/docs`


## Аутентификация API 🔐

#### Регистрация

`POST /api/auth/register`

#### Логин

`POST /api/auth/login`

Ответ:

```
{
   "message": "Добро пожаловать, your_username"
   "access_token": "...",
   "refresh_token": "..."
}
```

## Тестирование 🧪

Запуск тестов:

`pytest`

## Основные сущности 🤓

Модель User:

- username
- email
- password (хранение в виде хэша)
- role (user/ admin)
- is_active
- opinion (One-to-many)

Модель Opinion:

- title
- text
- status (pending/ approved / rejected)
- rejection_reason

## Роли 🎭

- `user` - обычный пользователь
- `admin` - администратор

## Планы по развитию 📈

- Сервис подтверждения почты
- Уведомления пользователя о модерации
- Лайки / дизлайки
- Комментарии
- Парсинг мнений с IMDb
- Кэширование
- Docker
