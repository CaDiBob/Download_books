import json
import os


from more_itertools import distribute, chunked
from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server, shell


def on_reload():
    path = 'pages'
    os.makedirs(path, exist_ok=True)
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')
    book_items = read_json('book_items.json')
    items_1, items_2 = distribute(2, book_items)
    items_1 = list(chunked(items_1, 20))
    items_2 = list(chunked(items_2, 20))

    for number, items in enumerate(zip(items_1, items_2), 1):
        itms_1, itms_2 = items
        rendered_page = template.render(
            number_pages=len(items_1),
            current_page=number,
            itms_1=itms_1,
            itms_2=itms_2,
        )
        with open(os.path.join(path, f'index{number}.html'), 'w', encoding="utf8") as file:
            file.write(rendered_page)


def read_json(book_items):
    with open(book_items, 'r') as file:
        items = file.read()
    loaded_items = json.loads(items)
    return loaded_items


def main():
    on_reload()
    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='.')


if __name__ == '__main__':
    main()
