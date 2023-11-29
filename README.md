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
- Gunicorn
- Docker
- GitHub Actions

## Как использовать проект:

Без аудентификации на проекте вам будут доступны:
- Получение списка рецептов;
- Получение данных отдельного рецепта;
- Получение списока пользователей;
- Получение токена авторизации;
- Регистрация пользователя.

Для аудентификации вам необходимо получить JWT токен, далее вам доступен функционал:
- Получение списка рецептов;
- Создание рецепта;
- Получение данных отдельного рецепта;
- Обновление данных рецепта текущего пользователя;
- Удаление данных рецепта текущего пользователя;
- Получение данных другого пользователя;
- Получение данных подписок текущего пользователя;
- Подписаться на пользователя;
- Отписаться от пользователя;
- Получение данных избранных рецептов текущего пользователя;
- Добавить рецепт в избраное;
- Удалить рецепт из избраного;
- Добавить рецепт в список покупок;
- Удалить рецепт из списка покупок;
- Загрузка списока покупок;
- Получение списка тегов;
- Получение данных отдельного тега;
- Получение списка ингридиентов;
- Получение данных отдельного ингридиента.


## База данных (пример):

Таблица users
|id|password |last_login |is_siperuser|usermame    |last_name  |email                |is_staff|is_active|date_joined               |first_name|
|--|:-------:|:---------:|:----------:|:----------:|:---------:|:-------------------:|:------:|:-------:|:------------------------:|:---------|
|1 |******** |           |1           |an          |an         |an@mail.ru           |1       |1        |2023-05-28 12:08:27.302971|an        |
|2 |******** |           |            |vasya.pupkin|Пупкин     |vpupkin@yandex.ru    |0       |1        |2023-05-28 12:08:27.302971|Вася      |
|3 |******** |           |            |second-user |Макаревский|second_user@email.org|0       |1        |2023-05-28 12:08:27.302971|Андрей    |

Таблица follow
|id|author_id|user_id|
|--|:-------:|:------|
|3 |2        |1      |

Таблица tegs
|id|name   |color  |slug   |
|--|:-----:|:-----:|:------|
|1 |Zavtrac|#1FFFC3|Zavtrac|
|2 |Obed   |#FFFFFF|Obed   |
|3 |Ужин   |#2CFFE3|Yjin   |

Таблица ingridients
|id|name               |measurement_unit|
|--|:-----------------:|:---------------|
|1 |абрикосовое варенье|г               |
|2 |абрикосовое пюре   |г               |

Таблица recipes
|id|name                    |text                           |pub_date                  |image|author_id|cooking_time|
|--|:----------------------:|:-----------------------------:|:------------------------:|:---:|:-------:|:-----------|
|6 |Рецепт от Васи          |Суп по Васински                |2023-05-29 02:53:10.886509|     |2        |15          |
|7 |Суп как у мамы          |Возми Добавь И все будет хорошо|2023-05-29 02:53:10.886509|     |3        |13          |
|7 |Рецепт от Администратора|Просто рецепт!                 |2023-05-29 02:53:10.886509|     |1        |18          |

Таблица amountingridients
|id|ingridient_id|recipe_id|amount|
|--|:-----------:|:-------:|:-----|
|9 |1            |6        |3     |
|10|2            |7        |4     |
|11|1            |8        |1     |
|12|2            |9        |2     |

Таблица recipe_tags
|id|recipe_id|tag_id|
|--|:-------:|:-----|
|9 |6        |1     |
|10|6        |2     |
|11|7        |1     |
|12|8        |2     |

Таблица favoriterecipe
|id|recipe_id|user_id|
|--|:-------:|:------|
|2 |7        |3      |

Таблица shoppinglist
|id|recipe_id|user_id|
|--|:-------:|:------|
|  |         |       |


## Примеры запросов к API

### Регистрация пользователя

#### POST запрос

```
/api/users/
```

##### Тело запроса

```
{
    "email": "test@yandex.ru",
    "username": "test",
    "first_name": "test",
    "last_name": "test",
    "password": "test1234test"
}
```

#### Ответ от сервера

```
{
    "id": 5,
    "username": "test",
    "first_name": "test",
    "last_name": "test",
    "email": "test@yandex.ru"
}
```

#### Статус код ответа от сервера 201 Created

-------------------------------------------

### Получение списка пользователей

#### GET запрос

```
/api/users/
```

#### Ответ от сервера

```
{
    "count": 5,
    "next": null,
    "previous": null,
    "results": [
        {
            "email": "an@mail.ru",
            "id": 1,
            "username": "an",
            "first_name": "an",
            "last_name": "an",
            "is_subscribed": false
        },
        {
            "email": "vpupkin@yandex.ru",
            "id": 2,
            "username": "vasya.pupkin",
            "first_name": "Вася",
            "last_name": "Пупкин",
            "is_subscribed": false
        },
        {
            "email": "second_user@email.org",
            "id": 3,
            "username": "second-user",
            "first_name": "Андрей",
            "last_name": "Макаревский",
            "is_subscribed": false
        },
        {
            "email": "third-user@user.ru",
            "id": 4,
            "username": "third-user-username",
            "first_name": "Гордон",
            "last_name": "Рамзиков",
            "is_subscribed": false
        },
        {
            "email": "test@yandex.ru",
            "id": 5,
            "username": "test",
            "first_name": "test",
            "last_name": "test",
            "is_subscribed": false
        }
    ]
}
```

#### Статус код ответа от сервера 200 OK

----------------------------------------------------------------------------

### Получение токена (аудентификация)

#### POST запрос

```
/api/auth/token/login/
```

##### Тело запроса

```
{
    "email": "test@yandex.ru",
    "password": "test1234test"
}
```

#### Ответ от сервера

```
{
    "auth_token": "e196ff457190f1e1d2c826ab474105b3955897b2"
}
```

#### Статус код ответа от сервера 201 Created

----------------------------------------------------------------------------

### Получение текущего пользователя

#### GET запрос 

```
/api/users/me
```

#### Ответ от сервера

```
{
    "email": "test@yandex.ru",
    "id": 5,
    "username": "test",
    "first_name": "test",
    "last_name": "test",
    "is_subscribed": false
}
```

#### Статус код ответа от сервера 200 OK

----------------------------------------------------------------------------

### Получение профиля пользователя

#### GET запрос 

```
/api/users/3
```

#### Ответ от сервера

```
{
    "email": "second_user@email.org",
    "id": 3,
    "username": "second-user",
    "first_name": "Андрей",
    "last_name": "Макаревский",
    "is_subscribed": false
}
```

#### Статус код ответа от сервера 200 OK

-----------------------------------------

### Получение списка тегов

#### GET запрос
 
```
/api/tags/
```

#### Ответ от сервера

```
[
    {
        "id": 1,
        "name": "Zavtrac",
        "color": "#1FFFC3",
        "slug": "Zavtrac"
    },
    {
        "id": 2,
        "name": "Obed",
        "color": "#FFFFFF",
        "slug": "Obed"
    },
    {
        "id": 3,
        "name": "Ужин",
        "color": "#2CFFE3",
        "slug": "Yjin"
    }
]
```

#### Статус код ответа от сервера 200 OK

-----------------------------------------

### Получение списка ингридиентов

#### GET запрос

  
```
/api/ingredients/
```

#### Ответ от сервера

```
[
    {
        "id": 1,
        "name": "абрикосовое варенье",
        "measurement_unit": "г"
    },
    {
        "id": 2,
        "name": "абрикосовое пюре",
        "measurement_unit": "г"
    }
]
```

#### Статус код ответа от сервера 200 OK

-----------------------------------------

### Добавление рецепта в избранное

#### POST запрос

```
/api/recipes/6/favorite/
```

#### Ответ от сервера

```
{

    "id": 6,
    "name": "Рецепт от Васи",
    "image": "http://127.0.0.1:8000/media/recipes/e98f14d5-f6c5-4716-9fa5-66d0768f2b48.png",
    "cooking_time": 15
}
```

#### Статус код ответа от сервера 201 Created

-----------------------------------------------

### Создание рецепта

#### POST запрос

```
/api/recipes/
```

##### Тело запроса

```
{
    "ingredients": 
    [
        {
            "id": 1,
            "amount": 10
        }
    ],
    "tags": 
    [
        1,
        2
    ],
    "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
    "name": "Лучшее что вы пробовали",
    "text": "Варенье",
    "cooking_time": 5
}
```

#### Ответ от сервера

```
{
    "id": 9,
    "tags": [
        {
            "id": 1,
            "name": "Zavtrac",
            "color": "#1FFFC3",
            "slug": "Zavtrac"
        },
        {
            "id": 2,
            "name": "Obed",
            "color": "#FFFFFF",
            "slug": "Obed"
        }
    ],
    "author": {
        "email": "test@yandex.ru",
        "id": 5,
        "username": "test",
        "first_name": "test",
        "last_name": "test",
        "is_subscribed": false
    },
    "ingredients": [
        {
            "id": 1,
            "name": "абрикосовое варенье",
            "measurement_unit": "г",
            "amount": 10
        }
    ],
    "is_favorited": false,
    "is_in_shopping_cart": false,
    "name": "Лучшее что вы пробовали",
    "image": "http://127.0.0.1:8000/media/recipes/1cb723e9-a525-428c-9964-7cbec7d19284.png",
    "text": "Варенье",
    "cooking_time": 5
}
```
#### Статус код ответа от сервера 201 OK

-----------------------------------------

### Получение списка рецептов

#### GET запрос

```
/api/recipes/
```

#### Ответ от сервера

```
{
    "count": 4,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 9,
            "tags": [
                {
                    "id": 1,
                    "name": "Zavtrac",
                    "color": "#1FFFC3",
                    "slug": "Zavtrac"
                },
                {
                    "id": 2,
                    "name": "Obed",
                    "color": "#FFFFFF",
                    "slug": "Obed"
                }
            ],
            "author": {
                "email": "test@yandex.ru",
                "id": 5,
                "username": "test",
                "first_name": "test",
                "last_name": "test",
                "is_subscribed": false
            },
            "ingredients": [
                {
                    "id": 1,
                    "name": "абрикосовое варенье",
                    "measurement_unit": "г",
                    "amount": 10
                }
            ],
            "is_favorited": false,
            "is_in_shopping_cart": false,
            "name": "Лучшее что вы пробовали",
            "image": "http://127.0.0.1:8000/media/recipes/1cb723e9-a525-428c-9964-7cbec7d19284.png",
            "text": "Варенье",
            "cooking_time": 5
        },
        {
            "id": 8,
            "tags": [
                {
                    "id": 2,
                    "name": "Obed",
                    "color": "#FFFFFF",
                    "slug": "Obed"
                }
            ],
            "author": {
                "email": "an@mail.ru",
                "id": 1,
                "username": "an",
                "first_name": "an",
                "last_name": "an",
                "is_subscribed": false
            },
            "ingredients": [
                {
                    "id": 1,
                    "name": "абрикосовое варенье",
                    "measurement_unit": "г",
                    "amount": 1
                },
                {
                    "id": 2,
                    "name": "абрикосовое пюре",
                    "measurement_unit": "г",
                    "amount": 2
                }
            ],
            "is_favorited": false,
            "is_in_shopping_cart": false,
            "name": "Рецепт от Администратора",
            "image": "http://127.0.0.1:8000/media/recipes/photo_5260303085048286153_y.jpg",
            "text": "Просто рецепт!",
            "cooking_time": 18
        },
        {
            "id": 7,
            "tags": [
                {
                    "id": 1,
                    "name": "Zavtrac",
                    "color": "#1FFFC3",
                    "slug": "Zavtrac"
                }
            ],
            "author": {
                "email": "second_user@email.org",
                "id": 3,
                "username": "second-user",
                "first_name": "Андрей",
                "last_name": "Макаревский",
                "is_subscribed": false
            },
            "ingredients": [
                {
                    "id": 2,
                    "name": "абрикосовое пюре",
                    "measurement_unit": "г",
                    "amount": 4
                }
            ],
            "is_favorited": false,
            "is_in_shopping_cart": false,
            "name": "Суп как у мамы",
            "image": "http://127.0.0.1:8000/media/recipes/%D0%A1%D0%BD%D0%B8%D0%BC%D0%BE%D0%BA_%D1%8D%D0%BA%D1%80%D0%B0%D0%BD%D0%B0_2023-11-25_%D0%B2_19.31.01.png",
            "text": "Возми \r\nДобавь\r\nИ все будет хорошо",
            "cooking_time": 13
        },
        {
            "id": 6,
            "tags": [
                {
                    "id": 1,
                    "name": "Zavtrac",
                    "color": "#1FFFC3",
                    "slug": "Zavtrac"
                },
                {
                    "id": 2,
                    "name": "Obed",
                    "color": "#FFFFFF",
                    "slug": "Obed"
                }
            ],
            "author": {
                "email": "vpupkin@yandex.ru",
                "id": 2,
                "username": "vasya.pupkin",
                "first_name": "Вася",
                "last_name": "Пупкин",
                "is_subscribed": false
            },
            "ingredients": [
                {
                    "id": 1,
                    "name": "абрикосовое варенье",
                    "measurement_unit": "г",
                    "amount": 3
                }
            ],
            "is_favorited": true,
            "is_in_shopping_cart": false,
            "name": "Рецепт от Васи",
            "image": "http://127.0.0.1:8000/media/recipes/e98f14d5-f6c5-4716-9fa5-66d0768f2b48.png",
            "text": "Суп по Васински",
            "cooking_time": 15
        }
    ]
}
```

#### Статус код ответа от сервера 200 ОК

-----------------------------------------

### Обновление рецепта

#### PATСH запрос

```
/api/recipes/9/
```

##### Тело запроса

```
{
    "ingredients": 
    [
        {
            "id": 1,
            "amount": 15
        }
    ],
    "tags": 
    [
        1,
        2,
        3
    ],
    "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
    "name": "Лучшее что вы пробовали, но не факт.",
    "text": " Много варенья",
    "cooking_time": 7
}
```

#### Ответ от сервера

```
{
    "id": 9,
    "tags": [
        {
            "id": 1,
            "name": "Zavtrac",
            "color": "#1FFFC3",
            "slug": "Zavtrac"
        },
        {
            "id": 2,
            "name": "Obed",
            "color": "#FFFFFF",
            "slug": "Obed"
        },
        {
            "id": 3,
            "name": "Ужин",
            "color": "#2CFFE3",
            "slug": "Yjin"
        }
    ],
    "author": {
        "email": "test@yandex.ru",
        "id": 5,
        "username": "test",
        "first_name": "test",
        "last_name": "test",
        "is_subscribed": false
    },
    "ingredients": [
        {
            "id": 1,
            "name": "абрикосовое варенье",
            "measurement_unit": "г",
            "amount": 15
        }
    ],
    "is_favorited": false,
    "is_in_shopping_cart": false,
    "name": "Лучшее что вы пробовали, но не факт.",
    "image": "http://127.0.0.1:8000/media/recipes/3f4e4b87-dbf0-4862-b08b-7765ad804bf8.png",
    "text": "Много варенья",
    "cooking_time": 7
}
```
#### Статус код ответа от сервера 200 OK

-----------------------------------------

### Получение рецепта

#### GET запрос

```
/api/recipes/7/
```

#### Ответ от сервера
```
{
    "id": 7,
    "tags": [
        {
            "id": 1,
            "name": "Zavtrac",
            "color": "#1FFFC3",
            "slug": "Zavtrac"
        }
    ],
    "author": {
        "email": "second_user@email.org",
        "id": 3,
        "username": "second-user",
        "first_name": "Андрей",
        "last_name": "Макаревский",
        "is_subscribed": false
    },
    "ingredients": [
        {
            "id": 2,
            "name": "абрикосовое пюре",
            "measurement_unit": "г",
            "amount": 4
        }
    ],
    "is_favorited": false,
    "is_in_shopping_cart": false,
    "name": "Суп как у мамы",
    "image": "http://127.0.0.1:8000/media/recipes/%D0%A1%D0%BD%D0%B8%D0%BC%D0%BE%D0%BA_%D1%8D%D0%BA%D1%80%D0%B0%D0%BD%D0%B0_2023-11-25_%D0%B2_19.31.01.png",
    "text": "Возми \r\nДобавь\r\nИ все будет хорошо",
    "cooking_time": 13
}
```

#### Статус код ответа от сервера 200 OK

-----------------------------------------

### Добавить рецепт в список покупок

#### POST запрос

```
/api/recipes/8/shopping_cart/
```

#### Ответ от сервера

```
{
    "id": 8,
    "name": "Рецепт от Администратора",
    "image": "http://127.0.0.1:8000/media/recipes/photo_5260303085048286153_y.jpg",
    "cooking_time": 18
}
```

#### Статус код ответа от сервера 201 Created

-----------------------------------

### Скачать список покупок

#### GET запрос

```
/api/recipes/download_shopping_cart/
```

#### Ответ от сервера

```
Список покупок: 
абрикосовое варенье, 1 г
абрикосовое пюре, 2 г
```

#### Статус код ответа от сервера 200 ОК

-----------------------------------------

## Автор:
Голованов Андрей

