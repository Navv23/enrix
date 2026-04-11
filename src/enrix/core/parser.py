import urllib.request
from html.parser import HTMLParser
from typing import Dict, List, Set
from enrix.settings import (EMAIL_REGEX, PHONE_REGEX, LINKEDIN_REGEX, WHATSAPP_REGEX, INSTAGRAM_REGEX)

class _HTMLTextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text_parts = []
        self.links = []
        
    def handle_data(self, data):
        if data.strip():
            self.text_parts.append(data.strip())

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for attr, val in attrs:
                if attr == "href" and val:
                    self.links.append(val)

    def get_text(self):
        return " ".join(self.text_parts)


class Enricher:
    def __init__(self, timeout: int = 5):
        self.timeout = timeout

    def fetch(self, url: str) -> str:
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9",
                "Referer": "https://www.google.com/",
                "Connection": "keep-alive",
            }
        )

        with urllib.request.urlopen(req, timeout=self.timeout) as res:
            return res.read().decode("utf-8", errors="ignore")

    def parse(self, html: str):
        parser = _HTMLTextExtractor()
        parser.feed(html)
        return parser.get_text(), parser.links

    def extract_emails(self, text: str) -> Set[str]:
        return set(EMAIL_REGEX.findall(text))

    def extract_phones(self, text: str) -> Set[str]:
        return set(PHONE_REGEX.findall(text))

    def extract_socials(self, links: List[str]) -> Dict[str, Set[str]]:
        socials = {
            "linkedin": set(),
            "instagram": set(),
            "facebook": set(),
            "whatsapp": set(),
        }

        for link in links:
            if LINKEDIN_REGEX.search(link):
                socials["linkedin"].add(link)

            if INSTAGRAM_REGEX.search(link):
                socials["instagram"].add(link)

            if WHATSAPP_REGEX.search(link):
                socials["whatsapp"].add(link)

        return socials

    def run(self, url: str) -> Dict:
        html = self.fetch(url)
        text, links = self.parse(html)

        return {
            "emails": list(self.extract_emails(text)),
            "phones": list(self.extract_phones(text)),
            "socials": self.extract_socials(links),
        }
    


if __name__ == "__main__":
    enricher = Enricher()
    websites = [
        "https://www.ril.com",
        "https://www.tcs.com",
        "https://www.infosys.com",
        "https://www.hdfcbank.com",
        "https://www.icicibank.com",
        "https://www.sbi.co.in",
        "https://www.airtel.in",
        "https://www.wipro.com",
        "https://www.hcltech.com",
        "https://www.larsentoubro.com",
        "https://www.tatamotors.com",
        "https://www.marutisuzuki.com",
        "https://www.mahindra.com",
        "https://www.itcportal.com",
        "https://www.hul.co.in",
        "https://www.bajajfinserv.in",
        "https://www.asianpaints.com",
        "https://www.sunpharma.com",
        "https://www.ntpc.co.in",
        "https://www.powergrid.in"
    ]
    
    for url in websites:
        try:
            result = enricher.run(url)
            print(f"{url}: {result}")
        except Exception as e:
            print(f"Error processing {url}: {e}")

    print(result)