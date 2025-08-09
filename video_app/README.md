# VideoApp

VideoApp — это Django-приложение для управления пользователями и видео.  
Использует PostgreSQL в качестве базы данных и Django REST Framework для API.

## Возможности

- Регистрация и управление пользователями  
- Создание и публикация видео  
- REST API для работы с контентом  
- Генерация большого объёма тестовых данных (10k пользователей, 100k видео)

## Установка
```
git clone https://github.com/username/video_app.git
cd video_app
python -m venv .venv
.venv\Scripts\activate   # Windows
# source .venv/bin/activate   # Linux/Mac
pip install -r requirements.txt
```

## Настройка базы данных

В video_app/settings.py укажите параметры подключения:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'video_app',
        'USER': 'postgres',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

Создайте базу данных в PostgreSQL:
```
CREATE DATABASE video_app;
```

## Применение миграций и создание суперпользователя
```
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

## Генерация тестовых данных

В проекте есть management-команда для создания пользователей и видео:
```
python manage.py generate_test_data
```
- создаёт 10 000 пользователей
- создаёт 100 000 опубликованных видео
- оптимизировано для быстрого выполнения через bulk_create

## Запуск сервера

```
python manage.py runserver
```
После запуска проект будет доступен по адресу:
http://127.0.0.1:8000/

##  API эндпоинты

| Метод | URL            | Описание                        |
| ----- | -------------- | ------------------------------- |
| GET   | `/api/videos/` | Список всех видео               |
| POST  | `/api/videos/` | Создание нового видео           |
| GET   | `/api/users/`  | Список всех пользователей       |
| POST  | `/api/users/`  | Регистрация нового пользователя |

##  Структура проекта

video_app/
├── manage.py
├── video_app/            # Настройки проекта
├── users/                # Приложение для пользователей
├── videos/               # Приложение для видео
│   ├── management/
│   │   ├── commands/
│   │   │   └── generate_test_data.py
└── requirements.txt

## Требования
- Python 3.10+
- PostgreSQL 13+
- Django 5+
- Django REST Framework
