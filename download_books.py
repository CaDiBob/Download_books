import argparse
import os
import requests

from bs4 import BeautifulSoup
from pathvalidate import sanitize_filepath
from urllib.parse import urljoin
from urllib.parse import urlparse


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError


def download_txt(url_txt, filename, folder='books/'):
    os.makedirs(folder, exist_ok=True)
    response = requests.get(url_txt)
    response.raise_for_status()
    check_for_redirect(response)
    filename = sanitize_filepath(f'{filename}.txt')
    filepath = os.path.join(folder, filename)
    with open(filepath, 'w')as file:
        file.write(response.text)


def download_image(url_img, folder='images/'):
    os.makedirs(folder, exist_ok=True)
    response = requests.get(url_img)
    response.raise_for_status()
    check_for_redirect(response)
    filename = urlparse(url_img)[-4].split('/')[-1]
    filepath = os.path.join(folder, filename)
    with open(filepath, 'wb')as file:
        file.write(response.content)


def parse_book_page(html_content):
    comment_book = list()
    title = html_content.find('h1').text.split('::')[0].strip()
    author = html_content.find('h1').text.split('::')[1].strip()
    genre = html_content.find('span', 'd_book').find('a')['title'].split('-')[0]
    path_book_img = html_content.find('div', class_='bookimage').find('img')['src']
    url_img = urljoin(f'http://tululu.org', f'{path_book_img}')
    comment_tags = html_content.find_all('div', 'texts')
    for comment_tag in comment_tags:
        comments = comment_tag.find_all('span', 'black')
        for comment in comments:
            comment_book.append(comment.get_text())
    return {
        'Название': title,
        'Автор': author,
        'Жанр': genre,
        'Комментарии': comment_book,
        'Ссылка на картинку': url_img,
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
    for book_id in range(args.start_id, args.end_id+1):
        try:
            url_book = f'http://tululu.org/b{book_id}/'
            url_txt = f'http://tululu.org/txt.php?id={book_id}'
            response = requests.get(url_book)
            response.raise_for_status()
            check_for_redirect(response)
            html_content = BeautifulSoup(response.text, 'lxml')
            page_content = parse_book_page(html_content)
            title = page_content['Название']
            url_img = page_content['Ссылка на картинку']
            filename = f'{book_id}. {title}'
            download_txt(url_txt, filename, folder='books/')
            download_image(url_img, folder='images/')
        except requests.HTTPError:
            continue


if __name__ == '__main__':
    main()
