import csv
from typing import Iterator


class FileReader:
    def __init__(self, file_path: str, website_column: str = "websites"):
        self.file_path = file_path
        self.website_column = website_column

    def read_urls(self) -> Iterator[str]:
        with open(self.file_path, "r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                url = row.get(self.website_column)
                if url:
                    yield url.strip()