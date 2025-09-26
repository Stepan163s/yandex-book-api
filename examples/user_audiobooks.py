#!/usr/bin/env python3
"""
Пример: Работа с аудиокнигами пользователя
Демонстрирует получение списка аудиокниг
"""

from yandex_book import User

USER_ID = "b4459480557"

def main():
    print("=== Аудиокниги пользователя ===")
    
    # Получаем список аудиокниг
    audiobooks = User.list_audiobooks(USER_ID)
    
    print(f"Всего аудиокниг: {len(audiobooks)}")
    print("\nПервые 3 аудиокниги:")
    
    for i, audiobook in enumerate(audiobooks[:3], 1):
        print(f"{i}. {audiobook.title or '[Без названия]'}")
        
        # Авторы
        if audiobook.authors:
            authors = [author.name for author in audiobook.authors]
            print(f"   Авторы: {', '.join(authors)}")
        
        # Чтецы
        if audiobook.narrators:
            narrators = [narrator.name for narrator in audiobook.narrators]
            print(f"   Чтецы: {', '.join(narrators)}")
        
        # Длительность
        if audiobook.duration:
            hours = audiobook.duration // 3600
            minutes = (audiobook.duration % 3600) // 60
            print(f"   Длительность: {hours}ч {minutes}м")
        
        # Язык
        if audiobook.language:
            print(f"   Язык: {audiobook.language}")
        
        # Метки
        if audiobook.labels:
            labels = [label.title for label in audiobook.labels]
            print(f"   Метки: {', '.join(labels)}")
        
        print()

if __name__ == "__main__":
    main()
