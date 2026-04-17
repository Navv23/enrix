import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List, Optional

from enrix.core.text_extractor import HTMLTextExtractor
from enrix.core.header_factory import HeaderFactory
from enrix.settings import (
    EMAIL_REGEX, PHONE_REGEX, LINKEDIN_REGEX, 
    WHATSAPP_REGEX, INSTAGRAM_REGEX, FACEBOOK_REGEX
)

class Enricher:
    def __init__(self, timeout: int = 10, proxy: str = None, max_retries: int = 3):
        self.timeout = timeout
        
        self.session = requests.Session()
        
        retry_strategy = Retry(total=max_retries,
                               backoff_factor=1, 
                               status_forcelist=[429, 500, 502, 503, 504],
                               allowed_methods=["GET"])
        
        adapter = HTTPAdapter(pool_connections=20, pool_maxsize=20, max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

        if proxy:
            self.session.proxies = {"http": proxy, "https": proxy}

    def fetch(self, url: str) -> Optional[str]:
        '''
        Fetches HTML using requests with auto-decoding and decompression
        '''
        try:
            headers = HeaderFactory.get_headers()
            
            response = self.session.get(url, 
                                        headers=headers, 
                                        timeout=self.timeout, 
                                        allow_redirects=True)
            
            response.raise_for_status()
            return response.text
                
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None

    def _clean_list(self, items) -> Optional[List[str]]:
        if not items: return None
        res = sorted(set(i.strip() for i in items if i and i.strip()))
        return res if res else None

    def extract_socials(self, links: List[str]) -> Optional[Dict[str, List[str]]]:
        socials = {"linkedin": [], "instagram": [], "whatsapp": [], "facebook": []}
        patterns = {"linkedin": LINKEDIN_REGEX, 
                    "instagram": INSTAGRAM_REGEX,
                    "whatsapp": WHATSAPP_REGEX, 
                    "facebook": FACEBOOK_REGEX}
        
        for link in links:
            link_l = link.lower()
            for platform, pattern in patterns.items():
                if len(socials[platform]) < 3:
                    match = pattern.search(link_l) if hasattr(pattern, 'search') else (pattern in link_l)
                    if match:
                        socials[platform].append(link)
                        break

        cleaned = {k: self._clean_list(v) for k, v in socials.items()}
        return {k: v for k, v in cleaned.items() if v} or None

    def run(self, url: str) -> Dict:
        html = self.fetch(url)
        
        if not html:
            return {"url": url, "emails": None, "phones": None, "socials": None, "status": "error"}

        parser = HTMLTextExtractor()
        parser.feed(html)
        text, links = parser.get_text(), parser.get_links()

        return {"url": url,
                "emails": self._clean_list(EMAIL_REGEX.findall(text)),
                "phones": self._clean_list(PHONE_REGEX.findall(text)),
                "socials": self.extract_socials(links),
                "status": "success"}

def process_sites(websites: List[str], max_workers: int = 10):
    enricher = Enricher(timeout=10)
    results = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_url = {executor.submit(enricher.run, url): url for url in websites}
        
        for future in as_completed(future_to_url):
            try:
                data = future.result()
                print(f"[{data['status'].upper()}] {data['url']}")
                results.append(data)
            except Exception as e:
                print(f"CRITICAL ERROR for {future_to_url[future]}: {e}")

    return results

if __name__ == "__main__":
    websites = websites = [
    "https://www.zoho.com",
    "https://www.flipkart.com",
    "https://www.paytm.com",
    "https://www.snapdeal.com",
    "https://www.myntra.com",
    "https://www.bigbasket.com",
    "https://www.irctc.co.in",
    "https://www.redbus.in",
    "https://www.olaelectric.com",
    "https://www.olacabs.com",
    "https://www.swiggy.com",
    "https://www.zomato.com",
    "https://www.policybazaar.com",
    "https://www.bankbazaar.com",
    "https://www.dream11.com",
    "https://www.byjus.com",
    "https://www.unacademy.com",
    "https://www.upgrad.com",
    "https://www.freshworks.com",
    "https://www.razorpay.com",
    "https://www.cleartax.in",
    "https://www.groww.in",
    "https://www.zerodha.com",
    "https://www.phonepe.com",
    "https://www.naukri.com",
    "https://www.99acres.com",
    "https://www.magicbricks.com",
    "https://www.indiamart.com",
    "https://www.tradeindia.com",
    "https://www.justdial.com"
]
    all_data = process_sites(websites)
    
    print(all_data, end="\n\n")