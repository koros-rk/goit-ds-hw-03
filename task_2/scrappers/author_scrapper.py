from bs4 import BeautifulSoup
from entities.author import Author


class AuthorScrapper:
    def __init__(self, html: str):
        self.soup = BeautifulSoup(html, "html.parser")

    def _parse_name(self):
        selected = self.soup.select("h3.author-title")
        return selected[0].text.strip()

    def _parse_born_date(self):
        selected = self.soup.select("span.author-born-date")
        return selected[0].text.strip()

    def _pase_born_location(self):
        selected = self.soup.select("span.author-born-location")
        return selected[0].text.strip()

    def _parse_description(self):
        selected = self.soup.select("div.author-description")
        return selected[0].text.strip()

    def parse(self):
        return Author(
            fullname=self._parse_name(),
            born_date=self._parse_born_date(),
            born_location=self._pase_born_location(),
            description=self._parse_description(),
        )
