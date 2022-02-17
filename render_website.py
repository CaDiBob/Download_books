import json
import os
from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server, shell


def on_reload():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')
    rendered_page = template.render(
        items=read_json('book_items.json'),
    )
    with open('index.html', 'w', encoding="utf8") as file:
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
