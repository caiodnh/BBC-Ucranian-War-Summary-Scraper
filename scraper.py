from typing import Any, Callable, Iterable, Tuple
import re
import requests
from bs4 import BeautifulSoup

class LiveNews:
  def __init__(self,
              main_url : str,
              liveblog_url_pattern : str,
              get_points : Callable[[str], Iterable[str]],
              header : str):
    self.main_url = main_url
    self.liveblog_url_pattern = liveblog_url_pattern
    self.get_points = get_points
    self.header = header

def bbc_get_points(url : str) -> Iterable[str]:
  page = requests.get(url)
  soup = BeautifulSoup(page.content, "html5lib")
  items = soup.find_all("li", class_ = "lx-c-summary-points__item")
  return (item.contents[0] for item in items)

bbc = LiveNews("https://www.bbc.com/",
              r"/news/live/world-europe-.*",
              bbc_get_points,
              "BBC's summary:")

# aljazeera = LiveNews("https://www.aljazeera.com/",
#                     r"https://www.aljazeera.com/news/.*-liveblog",
#                     undefined,
#                     "Al Jazeera's summary:")

def find_liveblog_url(live_news : LiveNews) -> str:
  page = requests.get(live_news.main_url)
  soup = BeautifulSoup(page.content, "html5lib")
  links = soup.find_all("a")
  
  pat = re.compile(live_news.liveblog_url_pattern)
  for link in links:
    url = link["href"]
    if pat.fullmatch(url):
      return "https://www.bbc.com" + url

  raise ValueError("No link to a liveblog found on the frontpage.")

def render(points : Iterable[str], header : str, url : str) -> str:
  marked_points = ("- " + point for point in points)
  flatten = "\n\n".join(marked_points)
  wrapped = "\n```\n" + flatten + "\n```"
  final = header + "\n" + wrapped + "\n" + "<" + url +">"
  return final

def get_summary(live_news : LiveNews) -> str:
  liveblog_url = find_liveblog_url(live_news)
  points = live_news.get_points(liveblog_url)
  return render(points, live_news.header, liveblog_url)

if __name__ == "__main__":
  print(get_summary(bbc))