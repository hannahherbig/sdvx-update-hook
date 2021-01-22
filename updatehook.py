import asyncio
import os
from pathlib import Path

import aiohttp
import lxml.html
from yarl import URL

WEBHOOK = os.environ.get("DISCORD_WEBHOOK_URL")

ALL_URLS = Path("urls.txt")
CURRENT_URLS = Path("current_urls.txt")


async def main():
    try:
        all_urls = ALL_URLS.read_text().split()
    except FileNotFoundError:
        all_urls = []

    async with aiohttp.ClientSession(raise_for_status=True) as session:
        async with session.get("https://p.eagate.573.jp/game/sdvx/") as response:
            html = lxml.html.fromstring(await response.text())

        urls = [
            img.attrib["data-original"] for img in html.cssselect("div.news_box img")
        ]

        for url in urls:
            if WEBHOOK and url not in all_urls:
                print(url)
                all_urls.append(url)
                async with session.get(url) as response:
                    image_data = await response.read()
                data = aiohttp.FormData()
                data.add_field("file", image_data, filename=URL(url).name)
                await session.post(WEBHOOK, data=data)

    ALL_URLS.write_text("".join(f"{url}\n" for url in all_urls))
    CURRENT_URLS.write_text("".join(f"{url}\n" for url in urls))


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
