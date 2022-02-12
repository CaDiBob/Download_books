import json
import os
import requests
import textwrap

from bs4 import BeautifulSoup
from pathvalidate import sanitize_filepath
from urllib.parse import urljoin
from tqdm import trange


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError


def download_txt(book_id, txt_filename, folder='books/'):
    book_txt_url = 'https://tululu.org/txt.php'
    params = {'id': book_id}
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


def get_book_soup(book_url):
    response = requests.get(book_url)
    response.raise_for_status()
    book_soup = BeautifulSoup(response.text, 'lxml')
    return book_soup


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


def save_items(items):
    if os.path.exists('book_items.json'):
        return add_to_json(items, filename='book_items.json')
    else:
        return save_json(items, filename='book_items.json')


def add_to_json(items, filename):
    with open(filename, 'r+') as file:
        content = json.load(file)
        content.append(items)
        file.seek(0)
        json.dump(content, file, indent=4, ensure_ascii=False)


def save_json(items, filename):
    book_items = [items]
    with open(filename, 'w') as fp:
        json.dump(book_items, fp, indent=4, ensure_ascii=False)


def main():    
    for page in trange(1,10):
        url = f'http://tululu.org/l55/{page}'
        response = requests.get(url)
        response.raise_for_status()
        check_for_redirect(response)
        page_soup = BeautifulSoup(response.text, 'lxml')
        page_tags = page_soup.select('.d_book')
        try:
            for tag in page_tags:
                path_url = tag.select_one('a')['href']
                path_book = path_url.split('/b')
                book_url = urljoin('http://tululu.org', path_url)
                book_soup = get_book_soup(book_url)
                book_items = parse_book_page(book_soup)
                title = book_items.get('Название')
                img_url = book_items.get('Ссылка на картинку')
                txt_filename = title
                trash, book_id = path_book
                save_items(book_items)
                download_txt(book_id, txt_filename, folder='books/')
                download_image(img_url, folder='images/')
        except requests.HTTPError:
            continue


if __name__ == '__main__':
    main()
