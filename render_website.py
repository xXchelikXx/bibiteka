from jinja2 import Environment, FileSystemLoader, select_autoescape
import json
from livereload import Server
import os
from more_itertools import chunked


def on_reload():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    with open("meta_data.json", "r", encoding="utf-8") as meta_data_file:
        meta_data_json = meta_data_file.read()

    books = json.loads(meta_data_json)

    os.makedirs("pages", exist_ok=True)

    template = env.get_template('template.html')

    books_pages = list(chunked(books, 10))

    for number, book_page in enumerate(books_pages, 1):

        rendered_page = template.render(
            books=book_page,
            pages_count=len(books_pages),
            current_page=number
        )

        with open(f'./pages/index{number}.html', 'w', encoding="utf8") as file:
            file.write(rendered_page)


on_reload()

server = Server()

server.watch('template.html', on_reload)

server.serve(root='.', default_filename="../pages/index.html")

