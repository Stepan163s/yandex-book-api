#!/usr/bin/env python3
"""
Пример: Скачивание медиафайлов
Демонстрирует скачивание обложек и аватаров
"""

import os
from yandex_book import User, Book

USER_ID = "b4459480557"
BOOK_ID = "yFWxRGiT"

def main():
    print("=== Скачивание медиафайлов ===")
    
    # Создаем папки для сохранения
    os.makedirs("downloads/avatars", exist_ok=True)
    os.makedirs("downloads/covers", exist_ok=True)
    
    # 1. Скачивание аватара пользователя
    print("1. Скачивание аватара пользователя:")
    try:
        user = User.get(USER_ID)
        
        if user.avatar and user.avatar.large:
            # Скачиваем большой аватар
            avatar_path = user.download_avatar("large", "downloads/avatars/user_avatar.jpg")
            print(f"✅ Аватар сохранен: {avatar_path}")
            
            # Скачиваем маленький аватар
            if user.avatar.small:
                avatar_small_path = user.download_avatar("small", "downloads/avatars/user_avatar_small.jpg")
                print(f"✅ Маленький аватар сохранен: {avatar_small_path}")
        else:
            print("ℹ️ У пользователя нет аватара")
            
    except Exception as e:
        print(f"❌ Ошибка скачивания аватара: {e}")
    
    # 2. Скачивание обложки книги
    print("\n2. Скачивание обложки книги:")
    try:
        book = Book.get(BOOK_ID)
        
        if book.cover and book.cover.large:
            # Скачиваем большую обложку
            cover_path = book.download_cover("large", f"downloads/covers/{book.uuid}_large.jpg")
            print(f"✅ Обложка сохранена: {cover_path}")
            
            # Скачиваем маленькую обложку
            if book.cover.small:
                cover_small_path = book.download_cover("small", f"downloads/covers/{book.uuid}_small.jpg")
                print(f"✅ Маленькая обложка сохранена: {cover_small_path}")
        else:
            print("ℹ️ У книги нет обложки")
            
    except Exception as e:
        print(f"❌ Ошибка скачивания обложки: {e}")
    
    # 3. Скачивание обложек из списка книг
    print("\n3. Скачивание обложек из списка книг:")
    try:
        books = User.list_books(USER_ID)
        
        for i, book in enumerate(books[:3], 1):  # Первые 3 книги
            if book.cover and book.cover.small:
                try:
                    cover_path = book.download_cover("small", f"downloads/covers/{book.uuid}_thumb.jpg")
                    print(f"✅ {i}. Обложка {book.title or book.uuid}: {cover_path}")
                except Exception as e:
                    print(f"❌ {i}. Ошибка скачивания {book.title or book.uuid}: {e}")
            else:
                print(f"ℹ️ {i}. У книги {book.title or book.uuid} нет обложки")
                
    except Exception as e:
        print(f"❌ Ошибка получения списка книг: {e}")
    
    print(f"\n📁 Файлы сохранены в папке: {os.path.abspath('downloads')}")

if __name__ == "__main__":
    main()
