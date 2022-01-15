import os
import requests

from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename


def fetch_book_id():
    for book_id in range(1,11):
        fetch_link_book(book_id)


def fetch_link_book(book_id):
    url_book = f'http://tululu.org/b{book_id}'
    url_txt = f'http://tululu.org/txt.php?id={book_id}'
    get_link_book(url_txt, book_id, url_book)
    

def fetch_book_title(url_book, book_id):
    response = requests.get(url_book)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    title = soup.find('h1').text.split(':')[0]
    return title


def get_link_book(url_txt, book_id, url_book):
    response = requests.get(url_txt, allow_redirects=False)
    response.raise_for_status()
    check_for_redirect(response, folder, book_id, url_book)



def dowload_txt(response, folder, book_id, url_book):
    filename = fetch_book_title(url_book, book_id)
    filepath = f'{folder}/{book_id}. {filename}'
    with open(filepath, 'wb') as file:
        file.write(response.content)


def check_for_redirect(response, folder, book_id, url_book):
    if not response.is_redirect:
        try:
            dowload_txt(response, folder, book_id, url_book)
        except requests.HTTPError:
            raise


if __name__ == '__main__':
    folder = 'books'
    os.makedirs(folder, exist_ok=True)
    fetch_book_id()
