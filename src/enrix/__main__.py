import argparse
from typing import List
from enrix.jobs.job import EnrichmentProcessor
from enrix.io.file_reader import FileReader
from enrix.io.file_writer import FileWriter


def main():
    '''
    Main function to handle command-line arguments and handle the enrichment process
    '''
    parser = argparse.ArgumentParser()

    parser.add_argument("--url", help="Single website URL")
    parser.add_argument("-i", "--input", help="CSV input file")
    parser.add_argument("-o", "--output", help="Output CSV file (optional)")

    args = parser.parse_args()

    processor = EnrichmentProcessor()

    results: List[dict] = []


    if args.url:
        result = processor.process_single(args.url)
        results.append(result)

    elif args.input:
        reader = FileReader(args.input)
        urls = list(reader.read_urls())

        results = processor.process_multithreading(urls)

    else:
        raise ValueError("Provide either --url or --input")

    if args.output:
        writer = FileWriter(args.output)
        writer.write(results)
    else:
        for r in results:
            print(r)


if __name__ == "__main__":
    main()