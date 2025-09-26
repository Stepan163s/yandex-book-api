#!/usr/bin/env python3
"""
Пример: Работа с цитатами пользователя
Демонстрирует получение списка цитат
"""

from yandex_book import User
from datetime import datetime

USER_ID = "b4459480557"

def main():
    print("=== Цитаты пользователя ===")
    
    # Получаем список цитат
    quotes = User.list_quotes(USER_ID)
    
    print(f"Всего цитат: {len(quotes)}")
    print("\nПоследние 5 цитат:")
    
    for i, quote in enumerate(quotes[:5], 1):
        print(f"{i}. \"{quote.content[:80]}{'...' if len(quote.content) > 80 else ''}\"")
        
        # Дата создания
        if quote.created_at:
            date = datetime.fromtimestamp(quote.created_at)
            print(f"   Дата: {date.strftime('%d.%m.%Y %H:%M')}")
        
        # Прогресс чтения
        print(f"   Прогресс: {quote.progress}%")
        
        # Лайки
        print(f"   Лайков: {quote.likes_count}")
        
        # Стиль выделения
        print(f"   Стиль: {quote.style}")
        
        print()

if __name__ == "__main__":
    main()
