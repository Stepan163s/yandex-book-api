import logging
from typing import List
from yandex_book import User, Book, Audiobook, Comicbook, Impression, Quote, ReadingAchievement

# Параметры для примера
USER_ID = "b4459480557"
BOOK_ID = "yFWxRGiT"
COMIC_ID = "AZZLnqqN"



def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s"
    )


def example_user():
    logging.info("=== USER INFO ===")
    user = User.get(USER_ID)
    print(f"Login: {user.login}")
    print(f"Name: {user.name or 'N/A'}")
    print(f"Followers: {user.followers_count}")
    print(f"Following: {user.followings_count}")
    print(f"Bookshelves: {user.bookshelves_count}\n")


def example_books():
    logging.info("=== USER BOOKS ===")
    books: List[Book] = User.list_books(USER_ID)
    for i, b in enumerate(books[:5], 1):
        print(f"{i}. {b.title or '[no title]'} (UUID: {b.uuid})")
    if len(books) > 5:
        print(f"... and {len(books)-5} more books\n")
    else:
        print()


def example_audiobooks():
    logging.info("=== USER AUDIOBOOKS ===")
    audio: List[Audiobook] = User.list_audiobooks(USER_ID)
    for ab in audio[:3]:
        authors = [p.name for p in ab.authors] if ab.authors else []
        print(f"- {ab.title} by {', '.join(authors)} [{ab.duration//60} min]")
    print()


def example_comics():
    logging.info("=== USER COMICBOOKS ===")
    comics: List[Comicbook] = User.list_comics(USER_ID)
    for cb in comics[:3]:
        print(f"- {cb.title} ({cb.uuid}), pages: {cb.pages_count if hasattr(cb, 'pages_count') else 'N/A'}")
    print()


def example_book_details():
    logging.info("=== BOOK DETAILS ===")
    book = Book.get(BOOK_ID)
    print(f"Title: {book.title}")
    print(f"Annotation: {book.annotation[:80]}...")
    imps: List[Impression] = Book.impressions(BOOK_ID)
    print(f"Total impressions: {len(imps)}\n")


def example_comic_details():
    logging.info("=== COMIC DETAILS ===")
    comic = Comicbook.get(COMIC_ID)
    print(f"Title: {comic.title}")
    print(f"Pages: {comic.pages_count if hasattr(comic, 'pages_count') else 'N/A'}")
    imps: List[Impression] = Comicbook.impressions(COMIC_ID)
    print(f"Total impressions: {len(imps)}\n")


def example_quotes():
    logging.info("=== USER QUOTES ===")
    quotes: List[Quote] = User.list_quotes(USER_ID)
    if not quotes:
        print("No quotes found")
        return
    for q in quotes[:5]:
        print(f'- "{q.content[:60]}" (at {q.created_at})')
    if len(quotes) > 5:
        print(f"... and {len(quotes)-5} more quotes")
    print()


def example_achievements():
    logging.info("=== READING ACHIEVEMENTS ===")
    ach: List[ReadingAchievement] = User.list_reading_achievements(USER_ID)
    for a in ach:
        print(f"Year {a.year}: books finished={a.finished_books_count}, pages={a.pages}")
    print()


def main():
    setup_logging()
    example_user()
    example_books()
    example_audiobooks()
    example_comics()
    example_book_details()
    example_comic_details()
    example_quotes()
    example_achievements()

if __name__ == "__main__":
    main()
