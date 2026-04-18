import requests
from typing import Dict, List, Optional

from enrix.core.text_parser import TextParser
from enrix.core.header_manager import HeaderManager
from enrix.settings import (
    EMAIL_REGEX, PHONE_REGEX, LINKEDIN_REGEX, TIMEOUT,
    WHATSAPP_REGEX, INSTAGRAM_REGEX, FACEBOOK_REGEX, SCRAPE_LIMIT
)


class CompanyEnricher:
    def __init__(self, timeout: int=TIMEOUT, proxy: str=None):
        self.timeout = timeout
        
        if proxy:
            self.session.proxies = {"http": proxy, "https": proxy}

    def fetch(self, url: str) -> Optional[str]:
        '''
        Fetches HTML using requests with auto-decoding and decompression
        '''
        try:
            headers = HeaderManager.get_headers()
            
            response = requests.get(url, 
                                        headers=headers, 
                                        timeout=self.timeout, 
                                        allow_redirects=True)
            
            response.raise_for_status()
            return response.text
                
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None

    def _clean_list(self, items) -> Optional[List[str]]:
        '''
        Cleans and deduplicates lists of emails, phones, or links
        '''
        if not items: return None
        res = sorted(set(i.strip() for i in items if i and i.strip()))
        return res if res else None

    def extract_socials(self, links: List[str]) -> Optional[Dict[str, List[str]]]:
        '''
        Extracts social media links based on regex patterns
        '''
        socials = {"linkedin": [], "instagram": [], "whatsapp": [], "facebook": []}
        patterns = {"linkedin": LINKEDIN_REGEX, 
                    "instagram": INSTAGRAM_REGEX,
                    "whatsapp": WHATSAPP_REGEX, 
                    "facebook": FACEBOOK_REGEX}
        
        for link in links:
            link_lowercase = link.lower()
            for platform, pattern in patterns.items():
                if len(socials[platform]) < SCRAPE_LIMIT:
                    match = pattern.search(link_lowercase) if hasattr(pattern, 'search') else (pattern in link_lowercase)
                    if match:
                        socials[platform].append(link)
                        break

        cleaned = {k: self._clean_list(v) for k, v in socials.items()}
        return {k: v for k, v in cleaned.items() if v} or None

    def run(self, url: str) -> Dict:
        '''
        Main method to fetch, parse, and extract data from a website
        '''
        html = self.fetch(url)
        
        if not html:
            return {"url": url,
                    "emails": None,
                    "phones": None,
                    "socials": None,
                    "status": "error"}

        parser = TextParser(url=url)
        parser.parse(html)

        text = parser.get_text()
        links = parser.get_links()

        return {"url": url,
                "emails": self._clean_list(EMAIL_REGEX.findall(text)),
                "phones": self._clean_list(PHONE_REGEX.findall(text)),
                "socials": self.extract_socials(links),
                "status": "success"}