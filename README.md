# Enrix: Company Enrichment Tool  

Enrix is a CLI tool for extracting structured company intelligence (emails, phone numbers, social links) from websites at scale.

---


## Workflow
<img src="src/enrix/data/enrix_logo.png" alt="Enrix Workflow" width="300"/>


## Workflow
<img src="src/enrix/data/enrix_workflow.png" alt="Enrix Workflow" width="900"/>


## Features

- Extracts:
  - Emails  
  - Phone numbers  
  - Social media links  
- Supports:
  - Single URL processing  
  - Bulk processing via CSV  
- Multithreaded execution for speed  
- Clean CSV output support  
- Modular architecture (CLI, processor, IO separated)  

---

## Quick Start

### Install

```bash
pip install -e .
```

---

### Run from CLI

#### Get Help to see available arguments
```bash
enrix --help
```

#### Process Single URL
```bash
enrix --url https://example.com
```

#### Read from an Input File
```bash
enrix --input websites.csv
```
`Note:` Without -o argument, you get the output in your terminal


#### Write to an Output File
```bash
enrix --input websites.csv --output results.csv
```

---

## CSV Format

Input CSV must contain:

```csv
websites
https://company1.com
https://company2.com
```

---

## CLI Arguments

| Argument   | Description                 | Required | Example                  |
|------------|----------------------------|----------|--------------------------|
| `--url`    | Process Single URL         | No       | https://example.com      |
| `--input`  | CSV file with URLs         | No       | websites.csv             |
| `--output` | Output CSV file            | No       | results.csv              |

> Provide either `--url` or `--input`

---

## Example Usage

```bash
enrix --url "https://openai.com"
```

```bash
enrix --input "companies.csv" --output "enriched.csv"
```

---

## Output Format

```csv
websites,emails,phones,socials,status
https://example.com,["a@b.com"],["+91xxxx"],["linkedin.com/..."],success
```

---

## Testing

`Note`: to be added

---

## Features to be added

- Add javascript support
- Add retry mechanism 
- Add test cases

---


## Project Structure

```
src/enrix/
├── core/        # Company enrichment logic
├── io/          # Reader / Writer
├── jobs/         # CLI entrypoint
├── utils/       # Helpers
└── tests/       # Unit tests
__main__.py
settings.py
```

---

## Notes

- Multithreading improves speed for bulk processing  
- Ensure input CSV has correct column (`websites`)  
- Output schema remains consistent across runs  

---

## Author

Navaneethan.ghanti@gmail.com  

For issues or contributions, please open a GitHub issue or PR.
