import argparse
import json
import os
import requests
import textwrap

from bs4 import BeautifulSoup
from pathlib import Path
from pathvalidate import sanitize_filepath
from urllib.parse import urljoin
from urllib.parse import urlparse


def add_argument_parser():
    parser = argparse.ArgumentParser(
        description='''Скрипт скачивает книги жанра "научная фантастика"
        с сайта https://tululu.org в указанном диапозе страниц'''
    )
    parser.add_argument(
        '--start_page',
        default=1,
        type=int,
        help='Начальный номер страницы, по умолчанию: 1',
    )
    parser.add_argument(
        '--end_page',
        default=701+1,
        type=int,
        help='Конечный номер страницы, по умолчанию: 701',
    )
    parser.add_argument(
        '--dest_folder',
        help='Путь к каталогу "куда скачивать"',
    )
    parser.add_argument(
        '--skip_imgs',
        action='store_true',
        default=False,
        help='Не скачивать картинки',
    )
    parser.add_argument(
        '--skip_txt',
        action='store_true',
        default=False,
        help='Не скачивать книги',
    )
    parser.add_argument(
        '--json_path',
        help='Путь к .json файлу с результатами',
    )
    return parser


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError


def download_txt(book_url, txt_filename, txt_filepath):
    os.makedirs(txt_filepath, exist_ok=True)
    response = requests.get(book_url)
    response.raise_for_status()
    check_for_redirect(response)
    txt_filename = sanitize_filepath(txt_filename)
    filepath = os.path.join(txt_filepath, txt_filename)
    with open(filepath, 'w')as file:
        file.write(response.text)


def download_image(img_url, img_filename, img_filepath):
    os.makedirs(img_filepath, exist_ok=True)
    response = requests.get(img_url)
    response.raise_for_status()
    check_for_redirect(response)
    filepath = os.path.join(img_filepath, img_filename)
    with open(filepath, 'wb')as file:
        file.write(response.content)


def get_book_page(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    return soup


def parse_book_page(soup):
    title, author = soup.select_one('h1').text.split('::')
    title = textwrap.shorten(title.strip(), width=100)
    author = author.strip()
    raw_genres = soup.select_one('span.d_book').select('a')
    genres = [genre.text for genre in raw_genres]
    img_tag_url = soup.select_one('.bookimage img')['src']
    img_url = urljoin('http://tululu.org', img_tag_url)
    book_tag_url = soup.select_one('[href^="/txt.php?id="]')['href']
    book_url = urljoin('http://tululu.org', book_tag_url)
    raw_comments = soup.select('.texts>.black')
    book_comments = [comments.text for comments in raw_comments]
    return {
        'title': title,
        'author': author,
        'genres': genres,
        'comments': book_comments,
        'img_url': img_url,
        'txt_url': book_url,
    }


def is_json(items, json_filepath):
    if os.path.exists(f'{json_filepath}/book_items.json'):
        return add_to_json(items, json_filepath, filename='book_items.json')
    else:
        return save_to_json(items, json_filepath, filename='book_items.json')


def add_to_json(items, json_filepath, filename):
    with open(f'{json_filepath}/{filename}', 'r+') as file:
        content = json.load(file)
        content.append(items)
        file.seek(0)
        json.dump(content, file, indent=4, ensure_ascii=False)


def save_to_json(items, json_filepath, filename):
    book_items = [items]
    with open(f'{json_filepath}/{filename}', 'w') as file:
        json.dump(book_items, file, indent=4, ensure_ascii=False)


def get_page(start, end):
    pages = list()
    for page in range(start, end):
        url = f'http://tululu.org/l55/{page}'
        response = requests.get(url)
        response.raise_for_status()
        check_for_redirect(response)
        page_soup = BeautifulSoup(response.text, 'lxml')
        page_tags = page_soup.select('.d_book')
        pages.extend(get_urk_book(page_tags))
    return pages


def get_urk_book(page_tags):
    urls = list()
    for tag in page_tags:
        path_url = tag.select_one('a')['href']
        path_book = path_url.split('/b')
        book_url = urljoin('http://tululu.org', path_url)
        urls.append(book_url)
    return urls


def main():
    parser = add_argument_parser()
    args = parser.parse_args()
    skip_imgs = args.skip_imgs
    skip_txt = args.skip_txt
    json_path = args.json_path
    folder = args.dest_folder
    start = args.start_page
    end = args.end_page
    urls = get_page(start, end)
    if folder:
        txt_filepath = f'{folder}/books/'
        img_filepath = f'{folder}/images/'
        json_filepath = folder
    else:
        txt_filepath = 'books/'
        img_filepath = 'images/'
        json_filepath = os.getcwd()
    if json_path:
        json_filepath = json_path
    for url in urls:
        try:
            soup = get_book_page(url)
            book_items = parse_book_page(soup)
            title = book_items.get('title')
            img_url = book_items.get('img_url')
            raw_img_path = urlparse(img_url)
            img_filename = os.path.basename(raw_img_path.path)
            txt_filename = f'{title}.txt'
            txt_url = book_items.get('txt_url')
            if not skip_txt:
                download_txt(txt_url, txt_filename, txt_filepath)
            if not skip_imgs:
                download_image(img_url, img_filename, img_filepath)
            book_items.update(
                book_path=f'{txt_filepath}/{txt_filename}',
                img_src=f'{img_filepath}/{img_filename}',
            )
            is_json(book_items, json_filepath)
            exit()
        except requests.HTTPError:
            continue
        except TypeError:
            continue


if __name__ == '__main__':
    main()
