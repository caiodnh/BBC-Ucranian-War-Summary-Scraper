from typing import Any, Iterable, Tuple
import requests
from bs4 import BeautifulSoup

def read_url() -> str:
  # the last line in the file corresponds to the most recent webpage
  with open('saved_urls.txt', 'r') as file:
    for line in file:
      url = line
  return url

def get_page(url : str) -> Any: # returns the page as BeatifulSoup object
  page = requests.get(url)
  soup = BeautifulSoup(page.content, "html5lib")
  return soup

def find_last_post(soup : Any) -> Any:
  post = soup.find("li", class_ = "lx-stream__post-container placeholder-animation-finished")
  header = post.find("header").find("span").contents[0]
  header = header.lower()
  if "live" in header and "moving" in header:
    return post
  else:
    return None

def update_page(url : str, soup : Any) -> Tuple[str, Any]:
  # check if there is a new page and, in this case, updade both the file and soup object

  last_post = find_last_post(soup)

  if last_post:
    link = last_post.find("a")
    url = link["href"]
    soup = get_page(url)

    # save url as the last line in the file
    with open('saved_urls.txt', 'a') as file:
      file.write("\n" + url)
      
    url, soup = update_page(url, soup)

  return url, soup

def get_points(soup : Any) -> Iterable[str]:
  items = soup.find_all("li", class_ = "lx-c-summary-points__item")
  return (item.contents[0] for item in items)

def render(points : Iterable[str], url) -> str:
  marked_points = ("- " + point for point in points)
  flatten = "\n\n".join(marked_points)
  wrapped = "\n```\n" + flatten + "\n```"
  final = wrapped + "\n" + "<" + url +">"
  return final

def get_summary() -> str:
  url = read_url()
  soup = get_page(url)
  url, soup = update_page(url, soup)
  points = get_points(soup)
  return render(points, url)

if __name__ == "__main__":
  print(get_summary())