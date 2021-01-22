import os
import os.path

import lxml.html
import requests

WEBHOOK = os.environ.get("DISCORD_WEBHOOK_URL")

URLS = "urls.txt"

try:
    with open(URLS, "r") as f:
        prev_urls = f.read().strip().split()
except FileNotFoundError:
    prev_urls = []

response = requests.get("https://p.eagate.573.jp/game/sdvx/")
response.raise_for_status()

if response.encoding == "Windows-31J":
    response.encoding = "CP932"

doc = lxml.html.fromstring(response.text)

urls = [img.attrib["data-original"] for img in dic.cssselect("div.news_box > a > img")]

for url in urls:
    if url not in prev_urls:
        print(url)
        urls.append(url)
        r = requests.get(url, stream=True)
        files = {"file": (os.path.basename(url), r.raw)}
        if WEBHOOK:
            response = requests.post(WEBHOOK, files=files)
            response.raise_for_status()

with open(URLS, "w") as f:
    f.write("\n".join(urls))
