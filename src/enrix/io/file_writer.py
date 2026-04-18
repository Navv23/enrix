import csv
import os
from typing import List, Dict


class FileWriter:
    def __init__(self, output_path: str):
        self.output_path = output_path

    def write(self, data: List[Dict]):
        if not data:
            return

        fieldnames = list(data[0].keys())

        file_exists = os.path.exists(self.output_path)
        file_empty = not file_exists or os.path.getsize(self.output_path) == 0

        with open(self.output_path, "a", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)

            if file_empty:
                writer.writeheader()

            writer.writerows(data)