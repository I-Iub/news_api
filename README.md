# news_api

Ссылки на запущенное приложение:
- [панель администратора](http://45.145.65.42/admin/)
- [документация](http://45.145.65.42/swagger/)

## Запуск проекта

Клонируйте проект в целевую папку.
```
git clone https://github.com/I-Iub/news_api.git
```

Перейдите в папку с проектом. Создайте файл `.env`. Запишите в файл `.env` 
переменные по примеру в файле [.env.example](https://github.com/I-Iub/news_api/blob/main/.env.example).
Если проект разворачивается на удалённом сервере, а не локально, то в файле 
`news/news/settings.py` в переменной `CSRF_TRUSTED_ORIGINS` укажите доменное 
имя или IP хоста.
```
CSRF_TRUSTED_ORIGINS = ['http://<домен или IP>']
```

Запустите контейнеры:
```
docker compose up -d
docker compose exec web python manage.py migrate               # миграции
docker compose exec web python manage.py collectstatic         # собрать статику
docker compose exec web python manage.py createsuperuser       # создать суперпользователя
```
Готово.

## Запуск сервера разработчика и тестов

Создайте виртуальное окружение и активируйте его (работа проверялась только на 
Python 3.10.5).
```
python3 -m venv venv
. venv/bin/activate     # Linux
```

Установите зависимости
```
pip install --upgrade pip
pip install -r requirements.txt
```

В приведённой выше инструкции "Запуск проекта" по команде `docker compose up -d` 
контейнер базы данных запускается без открытых наружу портов. Тестам и серверу 
разработчика нужен доступ к базе, поэтому для их запуска нужно открыть порты. 
Для этого остановите контейнеры. Находясь в корневой папке проекта выполните:
```
docker compose down
```
И запустите контейнеры, указав файл `docker-compose.dev.yaml`:
```
docker compose -f docker-compose.dev.yaml up -d
```
Запустите тесты:
```
pytest
```
Для запуска сервера разработчика перейдите в папку news (в ней есть файл 
manage.py)
```
cd news
POSTGRES_HOST=localhost POSTGRES_PORT=35432 python manage.py runserver
```
