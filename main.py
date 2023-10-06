import argparse
from collections import defaultdict
from datetime import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler

import pandas
from jinja2 import Environment, FileSystemLoader, select_autoescape

YEAR_OF_CREATION = 1920


def get_year_text(start_year):
    year = datetime.now().year - start_year
    if year % 10 == 1 and year % 100 != 11:
        return f"{year} год"
    elif year % 10 in range(2, 5) and year % 100 not in range(12, 15):
        return f"{year} года"

    return f"{year} лет"


def main():
    parser = argparse.ArgumentParser(
        description="Website of the author's wine store"
    )
    parser.add_argument(
        "-p",
        "--path",
        help="Path to excel document",
        default="wine.example.xlsx",
    )
    args = parser.parse_args()

    env = Environment(
        loader=FileSystemLoader("."),
        autoescape=select_autoescape(["html", "xml"])
    )
    template = env.get_template("template.html")

    categories = defaultdict(list)
    wines = pandas.read_excel(args.path, na_values=["N/A", "NA"], keep_default_na=False)
    for _, wine in wines.iterrows():
        categories[wine["Категория"]].append(wine.to_dict())

    rendered_page = template.render(
        year_text=get_year_text(YEAR_OF_CREATION),
        categories=categories
    )

    with open("index.html", "w", encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(("0.0.0.0", 8000), SimpleHTTPRequestHandler)
    server.serve_forever()



if __name__ == "__main__":
    main()
