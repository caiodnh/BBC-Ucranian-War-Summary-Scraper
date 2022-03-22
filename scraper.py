from typing import Any, Iterable
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from functools import reduce

def read_url() -> str:
  global url

  # the last line in the file corresponds to the most recent webpage
  with open('saved_url.txt', 'r') as file:
    for line in file:
      url = line
  return url

def get_page(url : str) -> Any: # returns the page as BeatifulSoup object
  page = requests.get(url)
  soup = BeautifulSoup(page.content, "html5lib")
  return soup

def update_page(soup : Any) -> Any:
  global url
  # check if there is a new page and, in this case, updade both the file and soup object

  last_post = soup.find("li", class_ = "lx-stream__post-container placeholder-animation-finished")
  header = last_post.find("header").find("span").contents[0]

  if header == 'Our live coverage is moving':
    link = last_post.find("a")
    url = link["href"]
    soup = get_page(url)

    # save url as the last line in the file
    with open('saved_url.txt', 'a') as file:
      file.write("\n" + url)
    soup = update_page(soup)

  return soup

def get_points(soup : Any) -> Iterable[str]:
  items = soup.find_all("li", class_ = "lx-c-summary-points__item")
  return (item.contents[0] for item in items)

def render_points(points : Iterable[str]) -> str:
  global url

  marked_points = ("- " + point for point in points)
  flatten = "\n\n".join(marked_points)
  wrapped = "\n```\n" + flatten + "\n```"
  final = wrapped + "\n" + "<" + url +">"
  return final

def add_header(text : str) -> str:
  header = datetime.now().strftime("Retrived on %B %d, %Y at %H:%M:%S")
  final = header + text
  return final

def get_summary() -> str:
  url = read_url()
  funcs = [get_page, update_page, get_points, render_points]
  return reduce(lambda x, f: f(x), funcs, url)

if __name__ == "__main__":
  print(get_summary())