# API Yamdb
# Учебный проект.  

## Проект YaMDb собирает отзывы пользователей на произведения. 

Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка». Например, в категории «Книги» могут быть произведения «Винни-Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Жуки» и вторая сюита Баха. Список категорий может быть расширен (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»). 
Произведению может быть присвоен жанр из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»). 
Добавлять произведения, категории и жанры может только администратор.
Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв.
Пользователи могут оставлять комментарии к отзывам.
Добавлять отзывы, комментарии и ставить оценки могут только аутентифицированные пользователи.

Целью проекта является закрепление знаний в области создания REST API на базе Django-проекта.

В проекте реализованы возможности:
    - регистрация пользователей;
    - CRD для категорий произведений;
    - CRD для жанров произведений;
    - CRUD для произведений (метод PUT не поддерживается);
    - CRUD для отзывов (метод PUT не поддерживается);
    - CRUD для комментариев на отзывы (метод PUT не поддерживается);
    - CRUD для пользователей (метод PUT не поддерживается);
    - получение данных о своей учетной записи / обновление данных своей учетной записи.

Алгоритм регистрации пользователей
    Пользователь отправляет POST-запрос на добавление нового пользователя с параметрами email и username на эндпоинт /api/v1/auth/signup/.
    YaMDB отправляет письмо с кодом подтверждения (confirmation_code) на адрес email.
    Пользователь отправляет POST-запрос с параметрами username и confirmation_code на эндпоинт /api/v1/auth/token/, в ответе на запрос ему приходит token (JWT-токен).
    При желании пользователь отправляет PATCH-запрос на эндпоинт /api/v1/users/me/ и заполняет поля в своём профайле (описание полей — в документации).

Пользовательские роли:
    Аноним — может просматривать описания произведений, читать отзывы и комментарии.
    Аутентифицированный пользователь (user) — может, как и Аноним, читать всё, дополнительно он может публиковать отзывы и ставить оценку произведениям (фильмам/книгам/песенкам), может комментировать чужие отзывы; может редактировать и удалять свои отзывы и комментарии. Эта роль присваивается по умолчанию каждому новому пользователю.
    Модератор (moderator) — те же права, что и у Аутентифицированного пользователя плюс право удалять любые отзывы и комментарии.
    Администратор (admin) — полные права на управление всем контентом проекта. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям.
    Суперюзер Django — обладет правами администратора (admin)


Стэк: Python 3.9.10 / Django 3.2 / djangorestframework 3.12.4


Установка:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:fluegergehaimer/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Перейти в корневую папку:
```
cd api_yamdb
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```


Некоторые примеры запросов к API:

Регистрация нового пользователя:
```

POST запрос:
api/v1/auth/signup/
{
"email": "user@example.com",
"username": "string"
}
```
Ответ:
```
{
"email": "string",
"username": "string"
}`
```
Получение JWT-токена:
```
POST запрос:
api/v1/auth/token/
{
"username": "string",
"confirmation_code": "string"
}
```
Ответ:
```
{
"token": "string"
}
```

Получение списка всех категорий:
```
GET запрос:
api/v1/categories/
```
Ответ
```
{
"count": 0,
"next": "string",
"previous": "string",
"results": [
{}
]
}
```

Добавление новой категории:

```
POST запрос:
api/v1/categories/

{
"name": "string",
"slug": "string"
}
```
Ответ
```
{
"name": "string",
"slug": "string"
}
```

Удаление категории:

```
DELETE запрос:
api/v1/categories/{slug}/

```

Получение списка всех произведений:
```
GET запрос:
api/v1/titles/
```
Ответ
```
{
"count": 0,
"next": "string",
"previous": "string",
"results": [
{}
]
}
```

Добавление произведения:

```
POST запрос:
api/v1/titles/

{
"name": "string",
"year": 0,
"description": "string",
"genre": [
"string"
],
"category": "string"
}
```
Ответ
```
{
"id": 0,
"name": "string",
"year": 0,
"rating": 0,
"description": "string",
"genre": [
{}
],
"category": {
"name": "string",
"slug": "string"
}
}
```

Получение информации о произведении:

```
GET запрос:
api/v1/titles/{titles_id}/

```
Ответ:
```
{
"id": 0,
"name": "string",
"year": 0,
"rating": 0,
"description": "string",
"genre": [
{}
],
"category": {
"name": "string",
"slug": "string"
}
}
```
Частичное обновление информации о произведении:
```
PATCH запрос:
api/v1/titles/{titles_id}/
```
Ответ:
```
{
"id": 0,
"name": "string",
"year": 0,
"rating": 0,
"description": "string",
"genre": [
{}
],
"category": {
"name": "string",
"slug": "string"
}
}
```
Удаление произведения:
```
DELETE запрос:
api/v1/titles/{titles_id}/
```


Получение списка всех пользователей:

```
GET запрос:
api/v1/users/

```
Ответ:
```
{
"count": 0,
"next": "string",
"previous": "string",
"results": [
{}
]
}
```
Добавление пользователя:
```
POST запрос:
api/v1/users/
{
"username": "string",
"email": "user@example.com",
"first_name": "string",
"last_name": "string",
"bio": "string",
"role": "user"
}
```
Ответ:
```
{
"username": "string",
"email": "user@example.com",
"first_name": "string",
"last_name": "string",
"bio": "string",
"role": "user"
}
```
Получение пользователя по username:

```
GET запрос:
api/v1/users/{username}/
```
Ответ:
```
{
"username": "string",
"email": "user@example.com",
"first_name": "string",
"last_name": "string",
"bio": "string",
"role": "user"
}
```
Изменение данных пользователя по username:
```
PATCH запрос:
api/v1/users/{username}/
{
"username": "string",
"email": "user@example.com",
"first_name": "string",
"last_name": "string",
"bio": "string",
"role": "user"
}
```
Ответ:
```
{
"username": "string",
"email": "user@example.com",
"first_name": "string",
"last_name": "string",
"bio": "string",
"role": "user"
}
```
Удаление пользователя по username:
```
DELETE запрос:
api/v1/users/{username}/
```

Получение данных своей учетной записи:
```
GET запрос:
api/v1/users/me/
```
Ответ:
```
{
"username": "string",
"email": "user@example.com",
"first_name": "string",
"last_name": "string",
"bio": "string",
"role": "user"
}
```
Изменение данных своей учетной записи:
```
PATCH запрос:
api/v1/users/me/
{
"username": "string",
"email": "user@example.com",
"first_name": "string",
"last_name": "string",
"bio": "string"
}
```
Ответ:
```
{
"username": "string",
"email": "user@example.com",
"first_name": "string",
"last_name": "string",
"bio": "string",
"role": "user"
}
```





Авторы: 
```
- команда Yandex-практикума https://github.com/yandex-praktikum?tab=repositories
```
```
- fluegergehaimer https://github.com/fluegergehaimer
```
```
- herrShneider https://github.com/herrShneider
```




