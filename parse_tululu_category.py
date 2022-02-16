import argparse
import json
import os
import requests

from bs4 import BeautifulSoup
from download_text import download_txt
from download_image import download_image
from parse_page import parse_book_page
from redirect import check_for_redirect
from urllib.parse import urljoin
from urllib.parse import urlparse


def get_last_page():
    url = 'http://tululu.org/l55'
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    last_page = int(soup.select_one('.npage:last-child').text)
    return last_page


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
        default=get_last_page()+1,
        type=int,
        help='Конечный номер страницы, по умолчанию: 701',
    )
    parser.add_argument(
        '--dest_folder',
        default='',
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


def save_to_json(items, json_filepath):
    json_filepath = os.path.join(json_filepath, 'book_items.json')
    with open(json_filepath, 'w') as file:
        json.dump(items, file, indent=4, ensure_ascii=False)


def get_urls(start, end):
    urls = list()
    for page in range(start, end):
        url = f'http://tululu.org/l55/{page}'
        response = requests.get(url)
        response.raise_for_status()
        page_soup = BeautifulSoup(response.text, 'lxml')
        page_tags = page_soup.select('.d_book')
        urls.extend(get_book_urls(page_tags))
    return urls


def get_book_urls(page_tags):
    urls = list()
    for tag in page_tags:
        path_book_url = tag.select_one('a')['href']
        book_url = urljoin('http://tululu.org', path_book_url)
        urls.append(book_url)
    return urls


def main():
    items = list()
    parser = add_argument_parser()
    args = parser.parse_args()
    start = args.start_page
    end = args.end_page
    txt_filepath = os.path.join(args.dest_folder, 'books')
    img_filepath = os.path.join(args.dest_folder, 'images')
    json_filepath = args.dest_folder
    urls = get_urls(start, end)
    if args.json_path:
        json_filepath = args.json_path
    for url in urls:
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'lxml')
            book_items = parse_book_page(soup)
            title = book_items.get('title')
            img_url = book_items.get('img_url')
            raw_img_path = urlparse(img_url)
            img_filename = os.path.basename(raw_img_path.path)
            txt_filename = f'{title}.txt'
            txt_url = book_items.get('txt_url')
            if not args.skip_txt:
                download_txt(txt_url, txt_filename, txt_filepath)
                book_items.update(
                    book_path=os.path.join(txt_filepath, txt_filename)
                )
            if not args.skip_imgs:
                download_image(img_url, img_filename, img_filepath)
                book_items.update(
                    img_src=os.path.join(img_filepath, img_filename)
                )
            items.append(book_items)
        except requests.HTTPError:
            continue
    save_to_json(items, json_filepath)

if __name__ == '__main__':
    main()
