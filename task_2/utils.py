import json
import os
import sys
import logging
from pathlib import Path

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from httpx import AsyncClient

from scrappers.author_scrapper import AuthorScrapper
from scrappers.posts_scrapper import PostsScrapper

logger = logging.getLogger("ts2")
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")

handler.setFormatter(formatter)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)


load_dotenv()
DOMAIN = os.getenv("SCRAPPING_DOMAIN")


async def fetch_posts(page: int) -> tuple[list, str | None]:
    if not DOMAIN:
        logger.error("SCRAPPING_DOMAIN is not set")
        return [], None
    try:
        async with AsyncClient(follow_redirects=True, base_url=DOMAIN) as client:
            logger.info(f"Scrapping page {page}...")
            response = await client.get(f"/page/{page}")
            posts = PostsScrapper(response.text).parse()
            return posts, response.text
    except Exception as e:
        logger.error(f"Unable to scrap page {page}: {e}")
        return [], None


async def fetch_author(author_link: str):
    if not DOMAIN:
        logger.error("SCRAPPING_DOMAIN is not set")
        return None
    try:
        async with AsyncClient(follow_redirects=True, base_url=DOMAIN) as client:
            logger.info(f"Scrapping author {author_link}...")
            response = await client.get(f"{DOMAIN}{author_link}")
            return AuthorScrapper(response.text).parse()
    except Exception as e:
        logger.error(f"Unable to scrap author {author_link}: {e}")
        return None


def dump_to_json(data: list, filename: str):
    try:
        path = Path(filename)

        with open(filename, "w") as f:
            raw_json = json.dumps(data, indent=4)
            f.write(raw_json)
            logger.info(f"Dumped to {filename}")
    except Exception as e:
        logger.error(f"Unable to dump to json: {e}")


def has_next_page(html: str | None):
    if html:
        soup = BeautifulSoup(html, "html.parser")
        return len(soup.select("li.next a")) != 0
    return False
