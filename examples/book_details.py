#!/usr/bin/env python3
"""
Пример: Детальная информация о книге
Демонстрирует получение информации о конкретной книге
"""

from yandex_book import Book

BOOK_ID = "yFWxRGiT"

def main():
    print("=== Детальная информация о книге ===")
    
    # Получаем книгу
    book = Book.get(BOOK_ID)
    
    print(f"Название: {book.title}")
    print(f"UUID: {book.uuid}")
    
    # Аннотация
    if book.annotation:
        # Убираем HTML теги для красивого вывода
        annotation = book.annotation.replace('<p>', '').replace('</p>', '\n')
        annotation = annotation.replace('<br>', '\n')
        print(f"Аннотация: {annotation[:200]}{'...' if len(annotation) > 200 else ''}")
    
    # Авторы
    if book.authors_objects:
        authors = [author.name for author in book.authors_objects]
        print(f"Авторы: {', '.join(authors)}")
    
    # Обложка
    if book.cover:
        if book.cover.small:
            print(f"Обложка (маленькая): {book.cover.small}")
        if book.cover.large:
            print(f"Обложка (большая): {book.cover.large}")
        
        # Скачивание обложки
        # book.download_cover("large", f"covers/{book.uuid}.jpg")
    
    # Впечатления
    print("\n=== Впечатления ===")
    impressions = Book.impressions(BOOK_ID)
    print(f"Всего впечатлений: {len(impressions)}")
    
    for i, impression in enumerate(impressions[:3], 1):
        if impression.content:
            print(f"{i}. {impression.content[:100]}{'...' if len(impression.content) > 100 else ''}")
            print(f"   Лайков: {impression.likes_count or 0}")

if __name__ == "__main__":
    main()
