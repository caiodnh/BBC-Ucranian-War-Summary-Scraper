import requests
import re
from datetime import date

url = "https://www.bbc.com/news/live/world-europe-60774819"
page = requests.get(url)

exp = re.compile(r"class=\"lx-c-summary-points__item\".*?>(.*?)<")

points = exp.findall(page.text)
marked_points = map(lambda x: "- " + x, points)

text = "\n\n".join(marked_points)
corrected_text = text.replace("&#x27;", "'")

header = "BBC's Summary - " + date.today().strftime("%B %d, %Y")
final = header + "\n```\n" + corrected_text + "\n```"

print(final)