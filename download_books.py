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
    filename = urlparse(url_img)[-4].split('/')[-1]
    filepath = os.path.join(folder, filename)
    with open(filepath, 'wb')as file:
        file.write(response.content)


def get_title_book(url_book):
    response = requests.get(url_book)
    soup = BeautifulSoup(response.text, 'lxml')
    title = soup.find('h1').text.split('::')[0].strip()
    return title


def get_url_book_img(url_book):
    response = requests.get(url_book)
    response.raise_for_status()
    check_for_redirect(response)
    soup = BeautifulSoup(response.text, 'lxml')
    path_book_img = soup.find('div', class_='bookimage').find('img')['src']
    url_img = urljoin(f'http://tululu.org', f'{path_book_img}')
    return url_img


def parse_book_comment(url_book):
    response =  requests.get(url_book)
    response.raise_for_status()
    check_for_redirect(response)
    soup = BeautifulSoup(response.text, 'lxml')
    comment_tags = soup.find_all('div', 'texts')
    for comment_tag in comment_tags:
        comments = comment_tag.find_all('span', 'black')
        for comment in comments:
            print(comment.get_text())


def parse_book_genre(url_book):
    response = requests.get(url_book)
    response.raise_for_status()
    check_for_redirect(response)
    soup = BeautifulSoup(response.text, 'lxml')
    genre = soup.find('span', 'd_book').find('a')['title'].split('-')[0]
    return genre

def main():
    for book_id in range(1, 11):
        try:
            url_book = f'http://tululu.org/b{book_id}/'
            url_img = get_url_book_img(url_book)
            filename = f'{book_id}. {get_title_book(url_book)}'
            url_txt = f'http://tululu.org/txt.php?id={book_id}'
            download_txt(url_txt, filename, folder='books/')
            download_image(url_img, folder='images/')
            print(get_title_book(url_book))
            print(parse_book_genre(url_book))
            parse_book_comment(url_book)
            print()
        except requests.HTTPError:
            continue
            

if __name__ == '__main__':
    main()
