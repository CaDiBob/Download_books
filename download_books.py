import argparse
import os
import requests
import textwrap

from bs4 import BeautifulSoup
from pathvalidate import sanitize_filepath
from tqdm import trange
from time import sleep
from urllib.parse import urljoin
from urllib.parse import urlparse


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError


def download_txt(book_txt_url, params, txt_filename, folder='books/'):
    os.makedirs(folder, exist_ok=True)
    response = requests.get(book_txt_url,
                            params=params,
                            )
    response.raise_for_status()
    check_for_redirect(response)
    txt_filename = sanitize_filepath(f'{txt_filename}.txt')
    filepath = os.path.join(folder, txt_filename)
    with open(filepath, 'w')as file:
        file.write(response.text)


def download_image(img_url, folder='images/'):
    os.makedirs(folder, exist_ok=True)
    response = requests.get(img_url)
    response.raise_for_status()
    check_for_redirect(response)
    raw_img_path = urlparse(img_url)
    img_filename = os.path.basename(raw_img_path.path)
    filepath = os.path.join(folder, img_filename)
    with open(filepath, 'wb')as file:
        file.write(response.content)


def parse_book_page(soup):
    title, author = soup.select_one('h1').text.split('::')
    title = textwrap.shorten(title.strip(), width=100)
    author = author.strip()
    raw_genres = soup.select_one('span.d_book').select('a')
    genres = [genre.text for genre in raw_genres]
    path_book_img = soup.select_one('.bookimage img')['src']
    img_url = urljoin('http://tululu.org', path_book_img)
    raw_comments = soup.select('.texts>.black')
    book_comments = [comments.text for comments in raw_comments]
    return {
        'Название': title,
        'Автор': author,
        'Жанр': genres,
        'Комментарии': book_comments,
        'Ссылка на картинку': img_url,
    }


def main():
    parser = argparse.ArgumentParser(
        description='''Скрипт скачивает книги с сайта
                       https://tululu.org в указанном диапозе id'''
                       )
    parser.add_argument('start_id',
                        nargs='?',
                        default=1,
                        type=int,
                        help='Начальный id книги, по умолчанию: 1',
                        )
    parser.add_argument('end_id',
                        nargs='?',
                        default=10,
                        type=int,
                        help='Конечный id книги, поумолчанию: 10'
                        )
    args = parser.parse_args()
    for book_id in trange(args.start_id, args.end_id+1):
        try:
            params = {'id': book_id}
            book_url = f'https://tululu.org/b{book_id}/'
            book_txt_url = 'https://tululu.org/txt.php'
            response = requests.get(book_url)
            response.raise_for_status()
            check_for_redirect(response)
            soup = BeautifulSoup(response.text, 'lxml')
            page_content = parse_book_page(soup)
            title = page_content.get('Название')
            img_url = page_content.get('Ссылка на картинку')
            txt_filename = f'{book_id}. {title}'
            download_txt(book_txt_url, params, txt_filename, folder='books/')
            download_image(img_url, folder='images/')
        except requests.HTTPError:
            continue


if __name__ == '__main__':
    main()
