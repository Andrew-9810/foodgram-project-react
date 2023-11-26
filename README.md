# Foodgram - продуктовый помощник
## Описание проекта
Сервис позволяет пользователям публиковать рецепты,
подписываться на публикации других пользователей, 
добавлять понравившиеся рецепты в список «Избранное»,
а перед походом в магазин скачивать сводный список продуктов,
необходимых для приготовления одного или нескольких выбранных блюд.

Адрес ресурса: 51.250.24.84
Администрато: login: an@mail.ru password:an1234an

## Запуск проекта на локальной машине:
Клонировать репозиторий:
`https://github.com/Andrew-9810/foodgram-project-react`
В корневой директории проекта файл .env заполнить своими данными:
```
POSTGRES_DB=foot
POSTGRES_USER=foot_user
POSTGRES_PASSWORD=foot_password
DB_HOST=db
DB_PORT=5432
DEBUG=False
SECRET_KEY='секретный ключ Django'
```
Создать и запустить контейнеры Docker, выполнить команду в терминале из корневой директории проекта:
```
docker-compose up -d
```
После успешной сборки выполнить миграции:
```
docker-compose exec backend python manage.py migrate
```
Собрать статику:
```
docker-compose exec backend python manage.py collectstatic
```
Копирование статики в рабочую диреторию:
```
docker compose exec backend cp -r /app/collected_static/. /backend_static/static/ 
```
Создать суперпользователя:
```
docker-compose exec backend python manage.py createsuperuser
```
Наполнить базу данных содержимым из файла ingredients.json:
```
docker-compose exec backend python manage.py loaddata ingredients.json
```

После запуска проект будут доступен по адресу: http://localhost/

Документация будет доступна по адресу: http://localhost/api/docs/

## Технологии: 
- Python
- Django
- Django REST Framework
- PostgreSQL
- NGINX
- gunicorn
- Docker
- GitHub Actions


## Автор:
Голованов Андрей

