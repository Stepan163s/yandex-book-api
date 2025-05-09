# 📚 Неофициальное api яндекс книг
![Логотип](./img/logo.jpg)

# Yandex Book API

**Yandex Book API** — профессиональная Pydantic-обёртка для Bookmate API. Предоставляет модели для основных сущностей, методы для получения данных и скачивания медиа.

## Установка

```bash
pip install yandex-book-api
```

## Быстрый старт

```python
from yandex_book import User, Book

# Получение пользователя и его книг (замените id на нужный)
user = User.get("b1234567890")
print(user.name, user.login)

books = User.list_books(user.id)
for b in books[:3]:
    print(b.title)

# Работа с конкретной книгой (замените id на нужный)
book = Book.get("mqK3FFjg")
print(book.title, book.annotation)
book.download_cover(size="small", dest="mqK3FFjg_thumb.jpg")
```

---

## Архитектура библиотеки

- **YandexBooksModel** — базовый класс всех моделей. Содержит методы:
  - `fetch(endpoint, key)` — получить одиночный объект;
  - `fetch_list(endpoint, key)` — получить список объектов;
  - `download_media(url, dest)` — скачать файл.

- **Модели** наследуются от `YandexBooksModel`. Каждая модель описывает поля API и предоставляет классовые методы:
  - `.get(...)`, `.list_...(...)` для запросов;
  - методы скачивания обложек или аватаров.

---

## Список моделей

### Image / Avatar

**Изображения и аватары**

| Поле                   | Тип      | Описание                 |
| ---------------------- | -------- | ------------------------ |
| `small`                | `str?`   | URL миниатюры            |
| `large`                | `str?`   | URL большого изображения |
| `placeholder`          | `str?`   | Base64-заглушка          |
| `ratio`                | `float?` | Соотношение сторон       |
| `background_color_hex` | `str?`   | Цвет фона (HEX)          |

### Label

**Метка контента**

| Поле    | Тип   | Описание       |
| ------- | ----- | -------------- |
| `title` | `str` | Текст метки    |
| `kind`  | `str` | Категория метки|

### Person

**Автор, иллюстратор, чтец**

| Поле          | Тип        | Описание                          |
| ------------- | ---------- | --------------------------------- |
| `name`        | `str`      | Имя                                |
| `locale`      | `str`      | Локаль (`ru`, `en` и т.п.)       |
| `uuid`        | `str`      | Уникальный идентификатор          |
| `works_count` | `int?`     | Количество работ                   |
| `image`       | `Image?`   | Профильное изображение            |
| `removed`     | `bool?`    | Помечен как удалённый             |
| `id`          | `int?`     | Числовой ID                       |

### User

**Пользователь**

| Поле                   | Тип       | Описание                         |
| ---------------------- | --------- | -------------------------------- |
| `id`                   | `int`     | Числовой ID                      |
| `login`                | `str`     | Логин                            |
| `name`                 | `str?`    | Имя пользователя                 |
| `avatar`               | `Avatar?` | Аватар                           |
| `bookshelves_count`    | `int?`    | Кол-во полок                     |
| `cards_count`          | `int?`    | Кол-во карточек                  |
| `followers_count`      | `int?`    | Кол-во подписчиков               |
| `followings_count`     | `int?`    | Кол-во подписок                  |
| `following`            | `bool?`   | Подписан на другого пользователя |
| `gender`               | `str?`    | Пол (`m`/`f`)                    |
| `library_cards_count`  | `int?`    | Книг в библиотеке                |
| `background_color_hex` | `str?`    | Цвет фона профиля                |
| `about`                | `str?`    | О себе                           |
| `facebook`, `twitter`, `vk`, `site` | `str?` | Соцсети / сайт       |
| `social_networks`      | `List[Any]?` | Дополнительные сети           |

**Методы**:
```
User.get(user_id) -> User
User.list_books(user_id) -> List[Book]
User.list_audiobooks(user_id) -> List[Audiobook]
User.list_comics(user_id) -> List[Comicbook]
User.list_bookshelves(user_id) -> List[Bookshelf]
User.list_followings(user_id) -> List[User]
User.list_impressions(user_id) -> List[Impression]
User.list_quotes(user_id) -> List[Quote]
User.list_reading_achievements(user_id) -> List[ReadingAchievement]
user.download_avatar(size, dest) -> str
```

### Book

**Книга**

| Поле             | Тип             | Описание            |
| ---------------- | --------------- | ------------------- |
| `uuid`           | `str`           | Идентификатор       |
| `title`          | `str?`          | Название            |
| `annotation`     | `str?`          | Аннотация           |
| `resource_type`  | `str?`          | Тип ресурса         |
| `cover`          | `Image?`        | Обложка             |
| `authors_objects`| `List[Person]?` | Авторы              |

**Методы**:
```
Book.get(book_id) -> Book
Book.impressions(book_id) -> List[Impression]
book.download_cover(size, dest) -> str
```

### Audiobook

**Аудиокнига**
Наследует `Book`, добавляет:

| Поле                   | Тип            | Описание                   |
| ---------------------- | -------------- | -------------------------- |
| `document_uuid`        | `str?`         | UUID документа             |
| `background_color_hex` | `str?`         | Цвет фона                  |
| `bookshelves_count`    | `int?`         | Кол-во полок               |
| `can_be_listened`      | `bool?`        | Доступна к прослушиванию   |
| `duration`             | `int?`         | Длительность (с)           |
| `impressions_count`    | `int?`         | Кол-во оценок              |
| `labels`               | `List[Label]?` | Метки                      |
| `language`             | `str?`         | Язык                       |
| `listeners_count`      | `int?`         | Кол-во слушателей          |
| `publication_date`     | `int?`         | Дата публикации            |
| `age_restriction`      | `str?`         | Ограничение по возрасту    |
| `owner_catalog_title`  | `str?`         | Название издательства      |
| `editor_annotation`    | `str?`         | Аннотация редактора        |
| `subscription_level`   | `str?`         | Уровень доступа            |
| `narrators`            | `List[Person]?`| Чтецы                      |

### Comicbook

**Комикс**
Наследует `Audiobook`, добавляет:
- `comic_card: Any?` — Дополнительные данные

**Методы**:
```
Comicbook.get(comic_id) -> Comicbook
Comicbook.impressions(comic_id) -> List[Impression]
comic.download_cover(size, dest) -> str
```

### Bookshelf

**Книжная полка**

| Поле             | Тип             | Описание            |
| ---------------- | --------------- | ------------------- |
| `uuid`           | `str`           | Идентификатор       |
| `title`          | `str`           | Название            |
| `annotation`     | `str?`          | Описание            |
| `cover`          | `Image?`        | Обложка             |
| `followers_count`| `int?`          | Подписчики          |
| `books_count`    | `int?`          | Кол-во книг         |
| `following`      | `bool?`         | Подписан ли         |
| `posts_count`    | `int?`          | Кол-во постов       |
| `creator`        | `User?`         | Создатель           |
| `authors`        | `List[Person]?` | Авторы              |

### Impression

**Впечатление**

| Поле             | Тип             | Описание                    |
| ---------------- | --------------- | --------------------------- |
| `book`           | `Book?`         | Связанная книга             |
| `comments_count` | `int?`          | Комментарии                 |
| `content`        | `str?`          | Текст впечатления           |
| `created_at`     | `int?`          | Время создания              |
| `liked`          | `bool?`         | Лайк установлен             |
| `likes_count`    | `int?`          | Кол-во лайков               |
| `resource`       | `Audiobook?`    | Связанный аудио             |
| `liker_users`    | `List[User]?`   | Пользователи, лайкнувшие    |

**Методы**:
```
User.list_impressions(user_id) -> List[Impression]
Book.impressions(book_id) -> List[Impression]
Comicbook.impressions(comic_id) -> List[Impression]
```

### Quote

**Цитата**

| Поле                | Тип      | Описание                        |
| ------------------- | -------- | ------------------------------- |
| `cfi`               | `str`    | Координаты в тексте             |
| `color`             | `int`    | Цвет подсветки                  |
| `comment`           | `str?`   | Комментарий                     |
| `comments_count`    | `int`    | Количество комментариев         |
| `content`           | `str`    | Текст цитаты                    |
| `created_at`        | `int`    | Время создания                  |
| `item_uuid`         | `str`    | UUID документа                  |
| `progress`          | `int`    | Процент прочитанного            |
| `start_node_offset` | `int`    | Начальная позиция               |
| `finish_node_offset`| `int`    | Конечная позиция                |
| `state`             | `str`    | Статус (`exists`/`removed`)     |
| `style`             | `str`    | Стиль выделения                 |
| `cover`             | `Image?` | Обложка книги                   |

**Методы**:
```
User.list_quotes(user_id) -> List[Quote]
```

### ReadingAchievement

**Достижения по чтению**

| Поле                   | Тип                  | Описание                       |
| ---------------------- | -------------------- | ------------------------------ |
| `finished_books_count` | `int`                | Завершённых книг               |
| `year`                 | `int`                | Год                            |
| `seconds`              | `int`                | Время (секунды)                |
| `pages`                | `int`                | Страницы                       |
| `share_url`            | `str`                | Ссылка на поделиться           |
| `reading_challenge`    | `ReadingChallenge?`  | Связанный челлендж             |

### ReadingChallenge

**Челлендж**

| Поле                  | Тип   | Описание                           |
| --------------------- | ----- | ---------------------------------- |
| `promised_books_count`| `int` | Цель — книг за год                 |
| `image_url`           | `str` | Картинка для шаринга               |
| `share_url`           | `str` | Ссылка на шаринг челленджа         |

---

## Лицензия

MIT

