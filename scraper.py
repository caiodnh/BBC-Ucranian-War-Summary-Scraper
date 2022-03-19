import requests
from datetime import date
from typing import List

from bs4 import BeautifulSoup

def get_points() -> List[str]:
  url = "https://www.bbc.com/news/live/world-europe-60802572"
  page = requests.get(url)

  soup = BeautifulSoup(page.content, 'html5lib')
  items = soup.find_all("li", class_ = "lx-c-summary-points__item")
  return [item.contents[0] for item in items]

def flatten_points(points : List[str]) -> str:
  marked_points = map(lambda x: "- " + x, points)

  text = "\n\n".join(marked_points)
  return text

def add_header(text : str) -> str:
  header = "BBC's Summary - " + date.today().strftime("%B %d, %Y")
  final = header + "\n```\n" + text + "\n```"
  return final

text = add_header(flatten_points(get_points()))

print(text)