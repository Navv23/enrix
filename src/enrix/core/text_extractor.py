from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse
from typing import List, Set

class HTMLTextExtractor(HTMLParser):
    def __init__(self, base_url: str = ""):
        super().__init__()
        
        self.base_url = base_url
        
        self.text_parts: List[str] = []
        self.links: Set[str] = set()

        self._skip_stack: List[str] = []
        self._skip_tags = {"script", "style", "noscript", "svg", "img"}
        self._min_text_len = 3

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()

        if tag in self._skip_tags:
            self._skip_stack.append(tag)
            return

        if tag == "a":
            href = None
            for attr, val in attrs:
                if attr == "href":
                    href = val
                    break

            if href:
                full_url = urljoin(self.base_url, href)
                if self._is_valid_link(full_url):
                    self.links.add(full_url)

    def handle_endtag(self, tag):
        tag = tag.lower()

        if self._skip_stack and self._skip_stack[-1] == tag:
            self._skip_stack.pop()


    def handle_data(self, data):
        if self._skip_stack:
            return

        text = data.strip()

        if (len(text) >= self._min_text_len and
            not text.isdigit()):
            self.text_parts.append(text)

    def _is_valid_link(self, url: str) -> bool:
        parsed = urlparse(url)

        if parsed.scheme not in {"http", "https"}:
            return False

        if any(x in url.lower() for x in ["javascript:", "#", "mailto:"]):
            return False

        return True

    def get_text(self) -> str:
        seen = set()
        clean = []

        for t in self.text_parts:
            if t not in seen:
                seen.add(t)
                clean.append(t)

        return " ".join(clean)

    def get_links(self) -> List[str]:
        return list(self.links)