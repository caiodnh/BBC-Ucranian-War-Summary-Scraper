import requests
import re
from datetime import date
from typing import List

def get_points() -> List[str]:
  url = "https://www.bbc.com/news/live/world-europe-60802572"
  page = requests.get(url)

  exp = re.compile(r"class=\"lx-c-summary-points__item\".*?>(.*?)<")
  return exp.findall(page.text)

def flatten_points(points : List[str]) -> str:
  marked_points = map(lambda x: "- " + x, points)

  text = "\n\n".join(marked_points)
  corrected_apostrophes = text.replace("&#x27;", "'")
  return corrected_apostrophes

def add_header(text : str) -> str:
  header = "BBC's Summary - " + date.today().strftime("%B %d, %Y")
  final = header + "\n```\n" + text + "\n```"
  return final

text = add_header(flatten_points(get_points()))

print(text)