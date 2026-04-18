import random
from typing import Dict

class HeaderManager:
    USER_AGENTS = [# Chrome on Windows
                   "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                   # Chrome on macOS
                   "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
                   # Firefox on Windows
                   "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
                   # Safari on macOS
                   "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2.1 Safari/605.1.15",
                   # Edge on Windows
                   "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0"]

    @classmethod
    def get_headers(cls) -> Dict[str, str]:
        ua = random.choice(cls.USER_AGENTS)
        
        headers = {"User-Agent": ua,
                   "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                   "Accept-Language": random.choice(["en-US,en;q=0.9", "en-GB,en;q=0.8", "en-US,en;q=0.5"]),
                   "Accept-Encoding": "gzip, deflate, br",
                   "Connection": "keep-alive",
                   "Upgrade-Insecure-Requests": "1",
                   "Sec-Fetch-Dest": "document",
                   "Sec-Fetch-Mode": "navigate",
                   "Sec-Fetch-Site": "none",
                   "Cache-Control": "max-age=0"}
        
        return headers