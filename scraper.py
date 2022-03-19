from typing import Any, Iterable
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def read_url() -> str:
  # the last line in the file corresponds to the most recent webpage
  with open('saved_url.txt', 'r') as file:
    for line in file:
      url = line
  return url

def update_page(soup : Any) -> Any:
  # check if there is a new page and, in this case, updade both the file and soup object

  last_post = soup.find("li", class_ = "lx-stream__post-container placeholder-animation-finished")
  found_link = last_post.find("a", alt = "this webpage here")

  if found_link:
    new_url = found_link["href"]

    # new soup object
    new_page = requests.get(new_url)
    soup = BeautifulSoup(new_page.content, "html5lib")

    # save url as the last line in the file
    with open('saved_url.txt', 'a') as file:
      file.write(new_url)

  return soup

def get_page() -> Any: # returns the page as BeatifulSoup object
  
  url = read_url()
  page = requests.get(url)
  soup = BeautifulSoup(page.content, "html5lib")
  new_soup = update_page(soup)
  return new_soup

def get_points(soup : Any) -> Iterable[str]:
  items = soup.find_all("li", class_ = "lx-c-summary-points__item")
  return (item.contents[0] for item in items)

def flatten_points(points : Iterable[str]) -> str:
  marked_points = ("- " + point for point in points)

  text = "\n\n".join(marked_points)
  return text

def add_header(text : str) -> str:
  header = datetime.now().strftime("BBC's Summary - %B %d, %Y at %H:%M:%S")
  final = header + "\n```\n" + text + "\n```"
  return final

text = add_header(flatten_points(get_points(get_page())))

print(text)