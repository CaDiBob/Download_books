import argparse
import json
import os


from more_itertools import distribute, chunked, divide
from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server, shell


def add_argument_parser():
    parser = argparse.ArgumentParser(
        description='''Скрипт публикует на локальном сервере
        книги жанра "научная фантастика" скаченные
        с сайта https://tululu.org'''
    )
    parser.add_argument(
        '--json_path',
        default='',
        help='Путь к .json файлу с результатами',
    )
    parser.add_argument(
        '--column_size',
        default=10,
        type=int,
        help='Определяет количество книг в одной колонке, по умолчанию 10'
        )
    return parser


def on_reload():
    parser = add_argument_parser()
    args = parser.parse_args()
    json_path = os.path.join(args.json_path, 'book_items.json')
    with open(json_path, 'r') as file:
        book_items = json.loads(file.read())
    path = 'pages'
    os.makedirs(path, exist_ok=True)
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    number_column_books = args.column_size
    template = env.get_template('template.html')
    group_1, group_2 = distribute(2, book_items)
    column_size_1 = list(chunked(group_1, number_column_books))
    column_size_2 = list(chunked(group_2, number_column_books))

    for number, books_group in enumerate(zip(column_size_1, column_size_2), 1):
        books_group_1, books_group_2 = books_group
        rendered_page = template.render(
            pages_number=len(column_size_1),
            current_page=number,
            books_group_1=books_group_1,
            books_group_2=books_group_2,
        )
        with open(
            os.path.join(path, f'index{number}.html'), 'w', encoding="utf8"
            ) as file:
            file.write(rendered_page)


def main():
    on_reload()
    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='.')


if __name__ == '__main__':
    main()
