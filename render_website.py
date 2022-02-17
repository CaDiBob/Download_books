import json

from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape



def read_json(book_items):
    with open(book_items, 'r') as file:
        items = file.read()
    loaded_file = json.loads(items)
    return loaded_file


def main():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    
    book_items = 'book_items.json'
    items = read_json(book_items)
    template = env.get_template('template.html')
    rendered_page = template.render(
        items=items,
    )
    
    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)
    
    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
