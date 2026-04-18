from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict
from enrix.core.company_enricher import CompanyEnricher
from enrix.settings import (
    MAX_WORKERS
)

class EnrichmentProcessor:
    def __init__(self, max_workers: int = MAX_WORKERS):
        self.max_workers = max_workers
        self.enricher = CompanyEnricher()

    def _handle_success(self, data: Dict) -> Dict:
        print(f"[{data['status'].upper()}] {data['url']}")
        return data

    def _handle_error(self, url: str, error: Exception) -> Dict:
        '''
        Logs the error and returns a standardized error dict
        '''
        print(f"CRITICAL ERROR for {url}: {error}")
        return {"url": url,
                "emails": None,
                "phones": None,
                "socials": None,
                "status": "error"}

    def process_single(self, url: str) -> Dict:
        '''
        Processes a single website URL and returns the enriched data
        '''
        try:
            data = self.enricher.run(url)
            return self._handle_success(data)
        except Exception as e:
            return self._handle_error(url, e)

    def process_multithreading(self, websites: List[str]) -> List[Dict]:
        '''
        Processes multiple websites concurrently using ThreadPoolExecutor
        '''
        results: List[Dict] = []

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_url = {executor.submit(self.enricher.run, url): url
                             for url in websites}

            for future in as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    data = future.result()
                    results.append(self._handle_success(data))
                except Exception as e:
                    results.append(self._handle_error(url, e))

        return results