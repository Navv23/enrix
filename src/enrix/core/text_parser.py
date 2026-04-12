import urllib.request
from typing import Dict, List, Optional

from enrix.core.text_extractor import HTMLTextExtractor
from enrix.settings import (
    EMAIL_REGEX,
    PHONE_REGEX,
    LINKEDIN_REGEX,
    WHATSAPP_REGEX,
    INSTAGRAM_REGEX
)


class Enricher:
    def __init__(self, timeout: int=5, proxy: str=None):
        self.timeout = timeout
        self.proxy = proxy

    def fetch(self, url: str) -> Optional[str]:
        try:
            request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})

            if self.proxy:
                proxy_handler = urllib.request.ProxyHandler({"http": self.proxy,
                                                             "https": self.proxy})
                opener = urllib.request.build_opener(proxy_handler)
                result = opener.open(request, timeout=self.timeout)
            else:
                result = urllib.request.urlopen(request, timeout=self.timeout)

            result = result.read().decode("utf-8", errors="ignore")
            return result

        except Exception:
            return None

    def parse(self, html: str):
        parser = HTMLTextExtractor()
        parser.feed(html)
        return parser.get_text(), parser.get_links()

    def _clean_list(self, items) -> Optional[List[str]]:
        if not items:
            return None
        return sorted(set(i.strip() for i in items if i and i.strip()))

    def extract_emails(self, text: str) -> Optional[List[str]]:
        emails = EMAIL_REGEX.findall(text)
        return self._clean_list(emails)

    def extract_phones(self, text: str) -> Optional[List[str]]:
        phones = PHONE_REGEX.findall(text)
        return self._clean_list(phones)

    def extract_socials(self, links: List[str]) -> Optional[Dict[str, List[str]]]:
        socials = {"linkedin": [],
                   "instagram": [],
                   "whatsapp": [],
                   "facebook": []}

        for link in links:
            link_l = link.lower()

            if LINKEDIN_REGEX.search(link_l):
                socials["linkedin"].append(link)

            elif INSTAGRAM_REGEX.search(link_l):
                socials["instagram"].append(link)

            elif WHATSAPP_REGEX.search(link_l):
                socials["whatsapp"].append(link)

            elif "facebook.com" in link_l:
                socials["facebook"].append(link)

        cleaned = {k: self._clean_list(v) for k, v in socials.items()}

        cleaned = {k: v for k, v in cleaned.items() if v is not None}

        return cleaned if cleaned else None

    def run(self, url: str) -> Dict:
        html = self.fetch(url)

        if not html:
            return {"emails": None,
                    "phones": None,
                    "socials": None}

        text, links = self.parse(html)

        emails = self.extract_emails(text)
        phones = self.extract_phones(text)
        socials = self.extract_socials(links)

        return {"emails": emails,
                "phones": phones,
                "socials": socials}


# ---------- TEST ----------

if __name__ == "__main__":
    enricher = Enricher()

    websites = [
        "https://www.crisil.com",
        "https://www.moodys.com",
        "https://www.standardandpoors.com",
        "https://www.fitch.com",
        "https://www.rbi.org.in",
        "https://www.sebi.gov.in",
        "https://www.irdai.gov.in",
        "https://www.pib.gov.in",
        "https://www.indiabudget.gov.in",
        "https://www.gst.gov.in",
        "https://www.nse.org.in",
        "https://www.bse.org.in",
        "https://www.mcxindia.com",
        "https://www.ncdex.com",
        "https://www.icex.org.in",
        "https://www.fieo.org",
        "https://www.assocham.org",
        "https://www.ibef.org"
    ]

    for url in websites:
        result = enricher.run(url)
        print(f"{url}: {result}")