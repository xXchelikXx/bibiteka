import os

import json 

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked
from dotenv import load_dotenv
load_dotenv()


def on_reload():
    env = Environment(
        loader=FileSystemLoader("."),
        autoescape=select_autoescape(["html", "xml"])
    )

    with open(os.getenv("META_DATA"), encoding="utf-8") as meta_data_file:
        books = json.load(meta_data_file)

    os.makedirs("pages", exist_ok=True)

    template = env.get_template("template.html")

    books_per_page = 10
    books_pages = list(chunked(books, books_per_page))

    for number, book_page in enumerate(books_pages, 1):
        rendered_page = template.render(
            books=book_page,
            pages_count=len(books_pages),
            current_page=number
        )

        with open(f"./pages/index{number}.html", "w", encoding="utf8") as file:
            file.write(rendered_page)


def main():
    on_reload()

    server = Server()
    server.watch("template.html", on_reload)
    server.serve(root=".", default_filename="../pages/index.html")


if __name__ == "__main__":
    main()