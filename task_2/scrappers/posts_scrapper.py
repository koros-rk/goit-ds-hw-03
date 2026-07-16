import requests

from pprint import pprint
from bs4 import BeautifulSoup, Tag

from entities import author
from entities.post import Post


class PostsScrapper:
    def __init__(self, html: str):
        self.soup = BeautifulSoup(html, "html.parser")

    @classmethod
    def _parse_text(cls, tag: Tag):
        selected = tag.select("span.text")
        return selected[0].text.strip()

    @classmethod
    def _parse_author_name(cls, tag: Tag):
        selected = tag.select("small.author")
        return selected[0].text.strip()

    @classmethod
    def _parse_author_link(cls, tag: Tag):
        selected = tag.select("small.author")
        if parent := selected[0].parent:
            if anchor := parent.select("a"):
                return anchor[0]["href"]

        return None

    @classmethod
    def _parse_tags(cls, tag: Tag):
        selected = tag.select("div.tags a.tag")
        return [tag.text.strip() for tag in selected]

    def _get_next_page_link(self):
        selected = self.soup.select("li.next a")
        return selected[0]["href"] if selected else None

    @classmethod
    def _parse_post(cls, tag: Tag):
        return Post(
            author_name=cls._parse_author_name(tag),
            author_link=cls._parse_author_link(tag),
            quote=cls._parse_text(tag),
            tags=cls._parse_tags(tag),
        )

    def parse(self):
        return [self._parse_post(tag) for tag in self.soup.select("div.quote")]


if __name__ == "__main__":
    response = requests.get("https://quotes.toscrape.com/page/1/")
    html = response.text

    scrapper = PostsScrapper(html)
    pprint(scrapper.parse())
