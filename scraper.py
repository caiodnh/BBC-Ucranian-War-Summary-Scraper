from typing import Any, Callable, Iterable, Tuple
import re
import requests
from bs4 import BeautifulSoup

class LiveNews:
  def __init__(self,
              main_url : str,
              liveblog_url_pattern : str,
              get_points : Callable[[str], Iterable[str]]):
    self.main_url = main_url
    self.liveblog_url_pattern = liveblog_url_pattern
    self.get_points = get_points

def bbc_get_points(url : str) -> Iterable[str]:
  page = requests.get(url)
  soup = BeautifulSoup(page.content, "html5lib")
  items = soup.find_all("li", class_ = "lx-c-summary-points__item")
  return (item.contents[0] for item in items)

bbc = LiveNews("https://www.bbc.com",
              r"/news/live/world-europe-.*",
              bbc_get_points)

def aljazeera_get_points(url : str) -> Iterable[str]:
  page = requests.get(url)
  soup = BeautifulSoup(page.content, "html5lib")
  block = soup.find(class_="wysiwyg wysiwyg--all-content css-1ck9wyi")
  items = block.find_all("li")

  def point_content(point):
    if isinstance(point, str):
      return point
    else: # point must be a link
      return point.contents[0]

  def flatten_item(item):
    return " ".join(point_content(point) for point in item)

  return (flatten_item(item) for item in items)

aljazeera = LiveNews("https://www.aljazeera.com",
                    r"/news/.*-liveblog",
                    aljazeera_get_points)

def find_liveblog_url(live_news : LiveNews) -> str:
  page = requests.get(live_news.main_url)
  soup = BeautifulSoup(page.content, "html5lib")
  links = soup.find_all("a")
  
  pat = re.compile(live_news.liveblog_url_pattern)
  for link in links:
    url = link["href"]
    if pat.fullmatch(url):
      return live_news.main_url + url

  raise ValueError("No link to a liveblog found on the frontpage.")

def render(points : Iterable[str], url : str) -> str:
  marked_points = ("- " + point for point in points)
  flatten = "\n\n".join(marked_points)
  wrapped = "\n```\n" + flatten + "\n```"
  final = wrapped + "\n" + "<" + url +">"
  return final

def get_summary(live_news : LiveNews) -> str:
  liveblog_url = find_liveblog_url(live_news)
  points = live_news.get_points(liveblog_url)
  return render(points, liveblog_url)

if __name__ == "__main__":
  print(get_summary(bbc))
  print(get_summary(aljazeera))