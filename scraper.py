from typing import Any, Callable, List
import re
import requests
from bs4 import BeautifulSoup

Soup = Any # There is no type hints for BeautifulSoup, but we pretend

def get_soup(url: str) -> Soup:
  page = requests.get(url)
  return BeautifulSoup(page.content, "html5lib")

class LiveNews:
  def __init__(self,
              home_url : str,
              find_liveblog : Callable[[Soup], str],
              get_points : Callable[[Soup], List[str]]):
    self.home_url = home_url
    self.find_liveblog = find_liveblog
    self.get_points = get_points

  def set_liveblog_url(self) -> None:
    soup_home = get_soup(self.home_url)
    self.liveblog_url = self.home_url + self.find_liveblog(soup_home)

  def summary_points(self) -> List[str]:
    self.set_liveblog_url()
    soup_liveblog = get_soup(self.liveblog_url)
    return self.get_points(soup_liveblog)

  def render_summary_points(self) -> str:
    points = self.summary_points()

    marked_points = ["- " + point for point in points]
    flattened_points = "\n\n".join(marked_points)
    wrapped = "```\n" + flattened_points + "\n```"

    final = wrapped + "\n" + "<" + self.liveblog_url +">"

    return final

def bbc_find_liveblog(soup : Soup) -> str:
  links = soup.find_all("a")
  
  pat = re.compile(r"/news/live/world-europe-.*")
  for link in links:
    url = link["href"]
    if pat.fullmatch(url):
      link_name = link.contents[0]
      if "Ukraine" in link_name or "Russia" in link_name or "Zelensky" in link_name or "Putin" in link_name:
        return url
  raise ValueError("Couldn't find a liveblog on BBC's frontpage")

def bbc_get_points(soup : Soup) -> List[str]:
  items = soup.find_all("li", class_ = "lx-c-summary-points__item")
  return [item.contents[0] for item in items]

bbc = LiveNews("https://www.bbc.com",
              bbc_find_liveblog,
              bbc_get_points)


def aljazeera_find_liveblog(soup : Any) -> str:
  soup = get_soup(aljazeera.home_url)

  fte_articles = soup.find_all("li", class_ = "fte-featured-articles-list__item")

  liveblogs = []
  for article in fte_articles:
    try:
      post_label = article.strong
      if post_label.contents[0] == "Live updates":
        url = article.a["href"]
        liveblogs.append(url)
    except:
      pass

  for url in liveblogs:
    if "ukraine" in url:
      return url
  raise ValueError("Couldn't find a liveblog about Ukraine on Aljazeera's frontpage")

def aljazeera_get_points(soup : Soup) -> List[str]:
  block = soup.find(class_="wysiwyg wysiwyg--all-content css-1ck9wyi")
  items = block.find_all("li")

  def point_content(point):
    if isinstance(point, str):
      return point
    else: # point must be a link
      return point.contents[0]

  def flatten_item(item):
    return "".join(point_content(point) for point in item)

  return [flatten_item(item) for item in items]

aljazeera = LiveNews("https://www.aljazeera.com",
                    aljazeera_find_liveblog,
                    aljazeera_get_points)

def aljazeera_get_map() -> str:
  aljazeera.set_liveblog_url()
  soup = get_soup(aljazeera.liveblog_url)
  content = soup.find(class_="wysiwyg wysiwyg--all-content css-1ck9wyi")

  image_tag = content.find("img")
  image_src = aljazeera.home_url + image_tag["src"]
  clean_src = re.search(r"^.*(?=\?)", image_src).group(0)

  return clean_src

aljazeera.get_map = aljazeera_get_map

if __name__ == "__main__":
  # print (bbc.render_summary_points())
  print(aljazeera.get_map())