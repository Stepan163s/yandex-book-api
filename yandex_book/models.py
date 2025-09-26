from __future__ import annotations
import os
import requests
from typing import Any, ClassVar, Dict, List, Optional, Type, TypeVar
from pydantic import BaseModel, Extra, root_validator

T = TypeVar('T', bound='YandexBooksModel')

class YandexBooksModel(BaseModel):
    """
    Базовый класс для всех моделей библиотеки YandexBooks.
    Предоставляет HTTP-запросы и скачивание медиа.

    Атрибуты класса:
      _BASE_URL: базовый адрес API
      _session: requests.Session для HTTP
    Методы:
      fetch: получить один объект
      fetch_list: получить список объектов
      download_media: скачать любой файл по URL
    """
    _BASE_URL: ClassVar[str] = "https://api.bookmate.ru/api/v5"
    _session: ClassVar[requests.Session] = requests.Session()

    class Config:
        extra = Extra.allow

    @classmethod
    def _request_json(cls, endpoint: str) -> Dict[str, Any]:
        url = f"{cls._BASE_URL}{endpoint}"
        response = cls._session.get(url)
        response.raise_for_status()
        return response.json()

    @classmethod
    def fetch(cls: Type[T], endpoint: str, key: str) -> T:
        """
        GET {BASE_URL}{endpoint}, взять под ключом key и вернуть модель.
        """
        payload = cls._request_json(endpoint).get(key, {})
        return cls(**payload)

    @classmethod
    def fetch_list(cls: Type[T], endpoint: str, key: str) -> List[T]:
        """
        GET {BASE_URL}{endpoint}, взять список под key и вернуть список моделей.
        """
        items = cls._request_json(endpoint).get(key, [])
        return [cls(**item) for item in items]

    @staticmethod
    def download_media(url: str, dest: str) -> str:
        """
        Скачивает файл по URL в локальный путь dest.
        Создаёт директории автоматически.
        """
        response = YandexBooksModel._session.get(url, stream=True)
        response.raise_for_status()
        directory = os.path.dirname(dest)
        if directory:
            os.makedirs(directory, exist_ok=True)
        with open(dest, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        return dest


# —————————————————————————————————————–
# Основные модели
# —————————————————————————————————————–

class Image(YandexBooksModel):
    small: Optional[str] = None
    large: Optional[str] = None
    placeholder: Optional[str] = None
    ratio: Optional[float] = None
    background_color_hex: Optional[str] = None


class Avatar(Image):
    """Аватар пользователя"""
    pass


class Label(YandexBooksModel):
    title: str
    kind: str


class Person(YandexBooksModel):
    name: str
    locale: Optional[str] = None
    uuid: Optional[str] = None
    works_count: Optional[int] = None
    image: Optional[Image] = None
    removed: Optional[bool] = None
    id: Optional[int] = None


# —————————————————————————————————————–
# Сущности API
# —————————————————————————————————————–

class User(Person):
    id: int
    login: str
    name: Optional[str] = None
    avatar: Optional[Avatar] = None
    bookshelves_count: Optional[int] = None
    cards_count: Optional[int] = None
    followers_count: Optional[int] = None
    followings_count: Optional[int] = None
    following: Optional[bool] = None
    gender: Optional[str] = None
    library_cards_count: Optional[int] = None
    background_color_hex: Optional[str] = None
    about: Optional[str] = None
    facebook: Optional[str] = None
    twitter: Optional[str] = None
    vk: Optional[str] = None
    site: Optional[str] = None
    social_networks: Optional[List[Any]] = None

    @root_validator(pre=True)
    def _warn_extra_fields(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        extra = set(values) - set(cls.__fields__)
        if extra:
            import logging, json
            logging.warning(
                f"[User] Обнаружены неизвестные поля: {extra}."  \
                f" Полный ответ: {json.dumps(values, ensure_ascii=False)}"
            )
        return values

    @classmethod
    def get(cls, user_id: int | str) -> User:
        return cls.fetch(f"/users/{user_id}", key="user")

    @classmethod
    def list_books(cls, user_id: int | str) -> List[Book]:
        return Book.fetch_list(f"/users/{user_id}/books", key="books")

    @classmethod
    def list_audiobooks(cls, user_id: int | str) -> List[Audiobook]:
        return Audiobook.fetch_list(f"/users/{user_id}/audiobooks", key="audiobooks")

    @classmethod
    def list_comics(cls, user_id: int | str) -> List[Comicbook]:
        return Comicbook.fetch_list(f"/users/{user_id}/comicbooks", key="comicbooks")

    @classmethod
    def list_bookshelves(cls, user_id: int | str) -> List[Bookshelf]:
        return Bookshelf.fetch_list(f"/users/{user_id}/bookshelves", key="bookshelves")

    @classmethod
    def list_followings(cls, user_id: int | str) -> List[User]:
        return cls.fetch_list(f"/users/{user_id}/followings", key="users")

    @classmethod
    def list_impressions(cls, user_id: int | str) -> List[Impression]:
        return Impression.fetch_list(f"/users/{user_id}/impressions", key="impressions")

    @classmethod
    def list_quotes(cls, user_id: int | str) -> List[Quote]:
        return Quote.fetch_list(f"/users/{user_id}/quotes", key="quotes")

    @classmethod
    def list_reading_achievements(cls, user_id: int | str) -> List[ReadingAchievement]:
        return ReadingAchievement.fetch_list(
            f"/users/{user_id}/reading_achievements/", key="reading_achievements"
        )

    def download_avatar(self, size: str = "large", dest: Optional[str] = None) -> str:
        url = getattr(self.avatar, size)
        dest = dest or f"avatars/{self.id}_{size}.jpg"
        return self.download_media(url, dest)


class Book(YandexBooksModel):
    uuid: str
    title: Optional[str] = None
    annotation: Optional[str] = None
    resource_type: Optional[str] = None
    cover: Optional[Image] = None
    authors_objects: Optional[List[Person]] = None

    @classmethod
    def get(cls, book_id: str) -> Book:
        return cls.fetch(f"/books/{book_id}", key="book")

    @classmethod
    def impressions(cls, book_id: str) -> List[Impression]:
        return Impression.fetch_list(f"/books/{book_id}/impressions", key="impressions")

    def download_cover(self, size: str = "large", dest: Optional[str] = None) -> str:
        url = getattr(self.cover, size)
        dest = dest or f"covers/books/{self.uuid}_{size}.jpg"
        return self.download_media(url, dest)


class Audiobook(Book):
    document_uuid: Optional[str] = None
    background_color_hex: Optional[str] = None
    bookshelves_count: Optional[int] = None
    can_be_listened: Optional[bool] = None
    duration: Optional[int] = None
    impressions_count: Optional[int] = None
    labels: Optional[List[Label]] = None
    language: Optional[str] = None
    listeners_count: Optional[int] = None
    publication_date: Optional[int] = None
    age_restriction: Optional[str] = None
    owner_catalog_title: Optional[str] = None
    editor_annotation: Optional[str] = None
    subscription_level: Optional[str] = None
    narrators: Optional[List[Person]] = None
    authors: Optional[List[Person]] = None


class Comicbook(Audiobook):
    comic_card: Optional[Any]

    @classmethod
    def get(cls, comic_id: str) -> Comicbook:
        return cls.fetch(f"/comicbooks/{comic_id}", key="comicbook")

    @classmethod
    def impressions(cls, comic_id: str) -> List[Impression]:
        return Impression.fetch_list(f"/comicbooks/{comic_id}/impressions", key="impressions")

    def download_cover(self, size: str = "large", dest: Optional[str] = None) -> str:
        url = getattr(self.cover, size)
        dest = dest or f"covers/comics/{self.uuid}_{size}.jpg"
        return self.download_media(url, dest)


class Bookshelf(YandexBooksModel):
    uuid: str
    title: str
    annotation: Optional[str]
    cover: Optional[Image]
    followers_count: Optional[int]
    books_count: Optional[int]
    following: Optional[bool]
    posts_count: Optional[int]
    creator: Optional[User]
    authors: Optional[List[Person]]


class Impression(YandexBooksModel):
    book: Optional[Book]
    comments_count: Optional[int]
    content: Optional[str]
    created_at: Optional[int]
    liked: Optional[bool]
    likes_count: Optional[int]
    resource: Optional[Audiobook]
    liker_users: Optional[List[User]]


class Quote(YandexBooksModel):
    cfi: str
    color: int
    comment: Optional[str] = None
    comments_count: int
    content: str
    created_at: int
    item_uuid: str
    finish_node_offset: int
    finish_node_xpath: str
    liked: bool
    likes_count: int
    progress: int
    start_node_offset: int
    start_node_xpath: str
    state: str
    style: str
    book: Book
    authors: Optional[str] = None
    authors_objects: Optional[List[Person]] = None
    cover: Optional[Image] = None


class ReadingChallenge(YandexBooksModel):
    promised_books_count: int
    image_url: str
    share_url: str


class ReadingAchievement(YandexBooksModel):
    finished_books_count: int
    year: int
    seconds: int
    pages: int
    last_updated: Optional[int]
    share_url: str
    reading_challenge: Optional[ReadingChallenge]
    user: User
