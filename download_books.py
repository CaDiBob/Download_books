import argparse
import os
import requests

from bs4 import BeautifulSoup
from download_text import download_txt
from download_image import download_image
from parse_page import parse_book_page
from redirect import check_for_redirect
from tqdm import trange
from urllib.parse import urlparse


def add_argument_parser():
    parser = argparse.ArgumentParser(
        description='''Скрипт скачивает книги с сайта
        https://tululu.org в указанном диапозе id'''
    )
    parser.add_argument(
        '--start_id',
        default=1,
        type=int,
        help='Начальный id книги, по умолчанию: 1',
    )
    parser.add_argument(
        '--end_id',
        default=10,
        type=int,
        help='Конечный id книги, поумолчанию: 10',
    )
    return parser


def main():
    txt_filepath = 'books'
    img_filepath = 'images'
    parser = add_argument_parser()
    args = parser.parse_args()
    for book_id in trange(args.start_id, args.end_id+1):
        try:
            book_url = f'https://tululu.org/b{book_id}/'
            response = requests.get(book_url)
            response.raise_for_status()
            check_for_redirect(response)
            soup = BeautifulSoup(response.text, 'lxml')
            book_items = parse_book_page(soup)
            title = book_items.get('title')
            img_url = book_items.get('img_url')
            txt_url = book_items.get('txt_url')
            raw_img_path = urlparse(img_url)
            img_filename = os.path.basename(raw_img_path.path)
            txt_filename = f'{book_id}. {title}'
            download_txt(txt_url, txt_filename, txt_filepath)
            download_image(img_url, img_filename, img_filepath)
        except requests.HTTPError:
            continue


if __name__ == '__main__':
    main()
