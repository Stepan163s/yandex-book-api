#!/usr/bin/env python3
"""
Пример: Базовая работа с пользователем
Демонстрирует получение информации о пользователе
"""

from yandex_book import User

# ID пользователя для примера
USER_ID = "b4459480557"

def main():
    print("=== Получение информации о пользователе ===")
    
    # Получаем пользователя
    user = User.get(USER_ID)
    
    # Выводим основную информацию
    print(f"Логин: {user.login}")
    print(f"Имя: {user.name or 'Не указано'}")
    print(f"Подписчиков: {user.followers_count or 0}")
    print(f"Подписок: {user.followings_count or 0}")
    print(f"Полок: {user.bookshelves_count or 0}")
    
    # Проверяем наличие аватара
    if user.avatar and user.avatar.large:
        print(f"Аватар: {user.avatar.large}")
        # Можно скачать аватар
        # user.download_avatar("large", f"avatar_{user.id}.jpg")
    
    # Социальные сети
    if user.about:
        print(f"О себе: {user.about[:100]}...")
    
    if user.vk:
        print(f"VK: {user.vk}")

if __name__ == "__main__":
    main()
