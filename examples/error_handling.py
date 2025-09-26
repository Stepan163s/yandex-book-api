#!/usr/bin/env python3
"""
Пример: Обработка ошибок
Демонстрирует правильную обработку ошибок API
"""

from yandex_book import User, Book
import requests

def main():
    print("=== Обработка ошибок ===")
    
    # 1. Обработка несуществующего пользователя
    print("1. Поиск несуществующего пользователя:")
    try:
        user = User.get("nonexistent_user")
        print(f"Пользователь найден: {user.name}")
    except requests.HTTPError as e:
        if e.response.status_code == 404:
            print("❌ Пользователь не найден")
        else:
            print(f"❌ Ошибка API: {e.response.status_code}")
    except Exception as e:
        print(f"❌ Неожиданная ошибка: {e}")
    
    # 2. Обработка несуществующей книги
    print("\n2. Поиск несуществующей книги:")
    try:
        book = Book.get("nonexistent_book")
        print(f"Книга найдена: {book.title}")
    except requests.HTTPError as e:
        if e.response.status_code == 404:
            print("❌ Книга не найдена")
        else:
            print(f"❌ Ошибка API: {e.response.status_code}")
    except Exception as e:
        print(f"❌ Неожиданная ошибка: {e}")
    
    # 3. Обработка сетевых ошибок
    print("\n3. Обработка сетевых ошибок:")
    try:
        # Временно изменяем базовый URL для демонстрации
        original_url = User._BASE_URL
        User._BASE_URL = "https://nonexistent-api.example.com"
        
        user = User.get("test")
    except requests.ConnectionError:
        print("❌ Ошибка подключения к серверу")
    except requests.Timeout:
        print("❌ Превышено время ожидания")
    except Exception as e:
        print(f"❌ Сетевая ошибка: {e}")
    finally:
        # Восстанавливаем оригинальный URL
        User._BASE_URL = original_url
    
    # 4. Безопасная работа с опциональными полями
    print("\n4. Безопасная работа с данными:")
    try:
        user = User.get("b4459480557")
        
        # Безопасный доступ к полям
        name = user.name or "Не указано"
        followers = user.followers_count or 0
        
        print(f"✅ Пользователь: {name}")
        print(f"✅ Подписчиков: {followers}")
        
        # Проверка наличия аватара
        if user.avatar and user.avatar.large:
            print(f"✅ Аватар: {user.avatar.large}")
        else:
            print("ℹ️ Аватар не установлен")
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    main()
