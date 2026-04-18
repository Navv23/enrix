from lxml import html
from urllib.parse import urljoin, urlparse
from typing import List, Set
from enrix.settings import (
    MIN_TEXT_LEN
)                        

class TextParser:
    def __init__(self, url: str = ""):
        self.url = url
        self._skip_tags = {"script", "style", "noscript", "svg", "img"}
        self.text_parts: List[str] = []
        self._links: Set[str] = set()

    def parse(self, html_content: str):
        '''
        Parses HTML content, extracting text and links while skipping certain tags
        '''
        tree = html.fromstring(html_content)

        for tag in self._skip_tags:
            for el in tree.xpath(f"//{tag}"):
                el.drop_tree()

        for text in tree.xpath("//text()"):
            find_text = text.strip()
            if len(find_text) >= MIN_TEXT_LEN and not find_text.isdigit():
                self.text_parts.append(find_text)

        for el in tree.xpath("//a[@href]"):
            href = el.get("href")
            if href:
                full_url = urljoin(self.url, href)
                if self._is_valid_link(full_url):
                    self._links.add(full_url)

    def _is_valid_link(self, url: str) -> bool:
        '''
        Basic validation to filter out non-HTTP links and common junk
        '''
        parsed = urlparse(url=url)

        if parsed.scheme not in ("http", "https"):
            return False

        if any(x in url.lower() for x in ["javascript:", "#", "mailto:"]):
            return False

        return True

    def get_text(self) -> str:
        '''
        Returns cleaned, deduplicated text content
        '''
        seen = set()
        clean = []

        for text in self.text_parts:
            if text not in seen:
                seen.add(text)
                clean.append(text)

        return " ".join(clean)

    def get_links(self) -> List[str]:
        '''
        Returns the list of extracted links
        '''
        return list(self._links)