import os
import requests

from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
# from random import randint


def fetch_link_book():
    # book_ids = [randint(32200, 32300) for _ in range(10)]
    for book_id in range(10):
        url = f"http://tululu.org/txt.php?id={book_id}"
        filename = f'id{book_id}.txt'
        response = requests.get(url, allow_redirects=False)
        response.raise_for_status()
        check_for_redirect(response, filename)


def save_book(filename, book):
    filepath = f'{books_dir}/{filename}'
    with open(filepath, 'wb') as file:
        file.write(book)


def check_for_redirect(response, filename):
        if not response.is_redirect:
            try:
                book = response.content
                save_book(filename, book)
            except requests.HTTPError:
                raise


if __name__ == '__main__':
    books_dir = 'books'
    os.makedirs(books_dir, exist_ok=True)
    fetch_link_book()