#!/usr/bin/env python3
"""
Пример: Работа с книгами пользователя
Демонстрирует получение списка книг пользователя
"""

from yandex_book import User

USER_ID = "b4459480557"

def main():
    print("=== Книги пользователя ===")
    
    # Получаем список книг
    books = User.list_books(USER_ID)
    
    print(f"Всего книг: {len(books)}")
    print("\nПервые 5 книг:")
    
    for i, book in enumerate(books[:5], 1):
        print(f"{i}. {book.title or '[Без названия]'}")
        print(f"   UUID: {book.uuid}")
        
        # Информация об авторах
        if book.authors_objects:
            authors = [author.name for author in book.authors_objects]
            print(f"   Авторы: {', '.join(authors)}")
        
        # Скачивание обложки
        if book.cover and book.cover.small:
            print(f"   Обложка: {book.cover.small}")
            # book.download_cover("small", f"covers/{book.uuid}_small.jpg")
        
        print()
    
    if len(books) > 5:
        print(f"... и ещё {len(books) - 5} книг")

if __name__ == "__main__":
    main()
