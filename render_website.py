import argparse
import json
import os


from more_itertools import distribute, chunked
from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server, shell


def add_argument_parser():
    parser = argparse.ArgumentParser(
        description='''Скрипт скачивает книги жанра "научная фантастика"
        с сайта https://tululu.org в указанном диапозе страниц'''
    )
    parser.add_argument(
        '--json_path',
        default='',
        help='Путь к .json файлу с результатами',
    )
    return parser


def on_reload():
    parser = add_argument_parser()
    args = parser.parse_args()
    json_items = os.path.join(args.json_path, 'book_items.json')
    path = 'pages'
    os.makedirs(path, exist_ok=True)
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')
    book_items = get_book_items(json_items)
    column_items_1, column_items_2 = distribute(2, book_items)
    column_items_1 = list(chunked(column_items_1, 20))
    column_items_2 = list(chunked(column_items_2, 20))

    for number, items in enumerate(zip(column_items_1, column_items_2), 1):
        items_1, items_2 = items
        rendered_page = template.render(
            number_pages=len(column_items_1),
            current_page=number,
            items_1=items_1,
            items_2=items_2,
        )
        with open(
            os.path.join(
                path,
                f'index{number}.html'
                ),
                'w',
                encoding="utf8"
                ) as file:
            file.write(rendered_page)


def get_book_items(json_items):
    with open(json_items, 'r') as file:
        items = file.read()
    book_items = json.loads(items)
    return book_items


def main():
    on_reload()
    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='.')


if __name__ == '__main__':
    main()
