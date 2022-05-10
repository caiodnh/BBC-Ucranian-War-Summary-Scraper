from abc import ABC, abstractmethod
from typing import Any, List, Optional
import re
import requests
from bs4 import BeautifulSoup

Soup = Any # There is no type hints for BeautifulSoup, but we pretend

def get_soup(url: str) -> Soup:
  page = requests.get(url)
  return BeautifulSoup(page.content, "html5lib")

class LiveNews(ABC):
  # These 3 attributes that should be specified by subclasses
  @property
  @abstractmethod
  def home_url(cls) -> str:
    pass

  @abstractmethod
  def find_liveblog(cls, soup : Soup) -> str:
    pass

  @abstractmethod
  def get_points(cls, soup : Soup) -> List[str]:
    pass

  # What follows will be the same for all subclasses:
  @classmethod
  def get_liveblog_url(cls) -> None:
    soup_home = get_soup(cls.home_url)
    return cls.home_url + cls.find_liveblog(soup_home)

  @classmethod
  def summary_points(cls, url : Optional[str] = None) -> List[str]:
    if url is None:
      url = cls.get_liveblog_url()
    soup_liveblog = get_soup(url)
    return cls.get_points(soup_liveblog)

  @classmethod
  def render_summary_points(cls) -> str:
    liveblog_url = cls.get_liveblog_url()
    points = cls.summary_points(url = liveblog_url)

    marked_points = ["- " + point for point in points]
    flattened_points = "\n\n".join(marked_points)
    wrapped = "```\n" + flattened_points + "\n```"

    final = wrapped + "\n" + "<" + liveblog_url +">"

    return final

class BBC(LiveNews):
    home_url = "https://www.bbc.com"

    @staticmethod
    def find_liveblog(soup : Soup) -> str:
      links = soup.find_all("a")
      
      pat = re.compile(r"/news/live/world-europe-.*")
      for link in links:
        url = link["href"]
        if pat.fullmatch(url):
          link_name = link.contents[0]
          key_words = (["Ukraine",
                        "Russia",
                        "Zelensky",
                        "Putin",
                        "Kyiv",
                        "Moscow",
                        "Donbas",
                        "Mariupol",
                        "Donestk",
                        "Luhansk"])
          if any(key_word in link_name for key_word in key_words):
            return url
      raise ValueError("Couldn't find a liveblog on BBC's frontpage")

    @staticmethod
    def get_points(soup : Soup) -> List[str]:
      items = soup.find_all("li", class_ = "lx-c-summary-points__item")
      return [item.contents[0] for item in items]

class Aljazeera(LiveNews):
    home_url = "https://www.aljazeera.com"

    @staticmethod
    def find_liveblog(soup : Any) -> str:
      fte_articles = soup.find_all("div", class_ = "fte-article__title")

      liveblogs = []
      for article in fte_articles:
        try:
          post_label = article.strong
          if post_label.contents[0] == "Live updates":
            url = article.a["href"]
            liveblogs.append(url)
        except:
          pass
      
      key_words = (["ukraine",
                    "russia",
                    "zelensky",
                    "putin",
                    "kyiv",
                    "moscow",
                    "donbas",
                    "mariupol",
                    "donestk",
                    "luhansk"])
      for url in liveblogs:
        if any(key_word in url for key_word in key_words):
          return url
      raise ValueError("Couldn't find a liveblog about Ukraine on Aljazeera's frontpage")

    @staticmethod
    def get_points(soup : Soup) -> List[str]:
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

    @classmethod
    def get_map(cls) -> str:
      liveblog_url = cls.get_liveblog_url()
      soup = get_soup(liveblog_url)
      content = soup.find(class_="wysiwyg wysiwyg--all-content css-1ck9wyi")

      image_tag = content.find("img")
      image_src = cls.home_url + image_tag["src"]
      clean_src = re.search(r"^.*(?=\?)", image_src).group(0)

      return clean_src

if __name__ == "__main__":
  print (BBC.render_summary_points())