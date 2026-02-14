# DMARC Report Analyzer

A simple Python tool to extract, parse and analyze DMARC aggregate reports (XML, ZIP, GZ) and generate a human-readable summary of authentication failures.

## 🚀 Features

- Extracts `.zip` and `.gz` DMARC reports
- Parses DMARC aggregate XML files
- Identifies:
  - Quarantine dispositions
  - DKIM failures
  - SPF failures
- Aggregates results across multiple reports
- Generates a plain text summary report

## 📂 Project Structure
input/archives # Place DMARC reports (.zip / .gz) here
work/extracted # Extracted XML files
reports/ # Generated summary report
dmarc-report-analyzer.py

## ⚙️ Requirements

- Python 3.9+
- No external dependencies (standard library only)

## 🧠 How It Works

1. Extract compressed DMARC reports
2. Parse XML files
3. Collect authentication failures
4. Generate a daily aggregated report

## ▶️ Usage

1. Clone the repository:

```bash
git clone https://github.com/hachiko-ops/dmarc-report-analyzer.git
cd dmarc-report-analyzer
```

2. Create the required directories:
```bash
mkdir input/archives
```
3. Place your DMARC aggregate reports (.zip or .gz) inside:
input/archives

5. Run the script:
```bash
python3 dmarc_report_analyzer.py
```

The script will:
Extract the archives
Parse the XML reports
Generate a summary file inside:
reports/daily_reportYYYY-MM-DD.txt


