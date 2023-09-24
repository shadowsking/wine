from collections import defaultdict
from datetime import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler

import pandas
from jinja2 import Environment, FileSystemLoader, select_autoescape


def get_year_text(start_year):
    year = datetime.now().year - start_year
    if year % 10 == 1 and year % 100 != 11:
        return f"{year} год"
    elif year % 10 in range(2, 5) and year % 100 not in range(12, 15):
        return f"{year} года"

    return f"{year} лет"


env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

categories = defaultdict(list)
wines = pandas.read_excel("wine.xlsx", na_values=['N/A', 'NA'], keep_default_na=False)
for index, row in wines.iterrows():
    categories[row.get("Категория")].append(row.to_dict())

rendered_page = template.render(
    year_text=get_year_text(1920),
    categories=categories
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
