import os
import requests

from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename


BASE_URL = 'https://tululu.org/'


def fetch_book_id():
    for book_id in range(1,11):
        fetch_link_book(book_id, BASE_URL)


def fetch_link_book(book_id, BASE_URL):
    url_book = f'{BASE_URL}b{book_id}'
    url_txt = f'{BASE_URL}txt.php?id={book_id}'
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
    check_for_redirect(response, books_folder, book_id, url_book)



def dowload_txt(response, books_folder, book_id, url_book):
    filename = fetch_book_title(url_book, book_id)
    filepath = f'{books_folder}/{book_id}. {filename}'
    with open(filepath, 'wb') as file:
        file.write(response.content)


def fetch_link_bookimage(BASE_URL, images_folder):
    for page_id in range(5,11):
        response = requests.get(f'{BASE_URL}b{page_id}')
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')
        link_bookimage = soup.find('div', class_='bookimage').find('img')['src']
        dowload_image(link_bookimage, images_folder, page_id, BASE_URL)



def dowload_image(link_bookimage, images_folder, page_id, BASE_URL):
    response = requests.get(f'{BASE_URL}{link_bookimage}')
    response.raise_for_status()
    save_image(response, images_folder, page_id)


def save_image(response, images_folder, page_id):
    filename = f'{page_id}'
    filepath = f'{images_folder}/{filename}'
    with open(filepath, 'wb') as file:
        file.write(response.content)

def check_for_redirect(response, books_folder, book_id, url_book):
    if not response.is_redirect:
        try:
            dowload_txt(response, books_folder, book_id, url_book)
        except requests.HTTPError:
            raise


if __name__ == '__main__':
    images_folder = 'images'
    books_folder = 'books'
    os.makedirs(images_folder, exist_ok=True)
    os.makedirs(books_folder, exist_ok=True)
    fetch_book_id()
    fetch_link_bookimage(BASE_URL, images_folder)
