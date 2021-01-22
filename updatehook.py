import os
import os.path

import requests
from bs4 import BeautifulSoup

WEBHOOK = os.environ.get("DISCORD_WEBHOOK_URL")

URLS = "urls.txt"

try:
    with open(URLS, "r") as f:
        urls = f.read().strip().split()
except FileNotFoundError:
    urls = []

response = requests.get("https://p.eagate.573.jp/game/sdvx/")
response.raise_for_status()

if response.encoding == "Windows-31J":
    response.encoding = "CP932"

doc = BeautifulSoup(response.text, "lxml")
for div in reversed(doc.find_all("div", class_="news_box")):
    for img in div.find_all("img"):
        url = img["data-original"]
        if url not in urls:
            print(url)
            urls.append(url)
            r = requests.get(url, stream=True)
            files = {"file": (os.path.basename(url), r.raw)}
            if WEBHOOK:
                response = requests.post(WEBHOOK, files=files)
                response.raise_for_status()

                with open(URLS, "w") as f:
                    f.write("\n".join(urls))
