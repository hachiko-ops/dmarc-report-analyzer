#!/usr/bin/env python3
from pathlib import Path
import zipfile
import gzip
import shutil
from datetime import datetime

import xml.etree.ElementTree as ET
from typing import List, Dict

from collections import defaultdict

def extract_archives(input_dir: Path, output_dir: Path) -> None:
    # Creo la cartella output se non esiste, se esiste non lancia l'errore
    output_dir.mkdir(parents=True, exist_ok=True)

    for archive in input_dir.iterdir():
        # archive.suffix -> estensione file
        # archive.stem -> solo nome file
        if( archive.suffix == ".zip"):
            with zipfile.ZipFile(archive, "r") as zip_ref: #Apre il file in lettura
                zip_ref.extractall(output_dir) #Estrae tutti i file che ci sono dentro
        
        elif archive.suffix == ".gz":
            output_file = output_dir / archive.stem 
            with gzip.open(archive, "rb") as gz_file: #Apre il file in lettura binaria
                with open(output_file, "wb") as out_file: #Apre il file in scrittura binaria
                    shutil.copyfileobj(gz_file, out_file)

def parse_dmarc_xml(xml_file: Path) -> Dict[str, List[Dict]]:
    tree = ET.parse(xml_file)
    root = tree.getroot()

    report = {
        "failures": [],
        "failuresDkim": [],
        "failuresSPF": [],
    }

    report_meta = root.find("report_metadata")
    for record in root.findall("record"):
        row = record.find("row")
        policy = row.find("policy_evaluated")

        disposition = policy.findtext("disposition")   
        testDkim = policy.findtext("dkim")
        testSPF = policy.findtext("spf")
        if( disposition == "quarantine" ):
            # aggiungo il nodo record completo (puoi tenerlo come Element o come stringa)
            report["failures"].append({
                "report_meta": report_meta,  # oggetto Element
                "record": record             # oggetto Element
            })
        elif ( testDkim == 'fail' ):
            report["failuresDkim"].append({
                "report_meta": report_meta,  # oggetto Element
                "record": record             # oggetto Element
            }) 
        elif ( testSPF == 'fail' ):
            report["failuresSPF"].append({
                "report_meta": report_meta,  # oggetto Element
                "record": record             # oggetto Element
            }) 
    
    return report
    

def aggregate_failures(xml_dir: Path) -> Dict[str, Dict]:
    aggregated = {
        "failures": [],
        "failuresDkim": [],
        "failuresSPF": [],
    }

    
    for xml_file in xml_dir.glob("*.xml"):
        report = parse_dmarc_xml(xml_file)

        for key in aggregated.keys():
            for failure in report[key]:
                aggregated[key].append({
                    "report_meta": ET.tostring(failure["report_meta"], encoding="unicode"),
                    "record":ET.tostring(failure["record"], encoding="unicode")
                })

    return aggregated        

def generate_report(aggregated_data: Dict[str, list], output_file: Path) -> None:
    with open(output_file, "w", encoding="utf-8") as report:
        report.write("DMARC Quarantine Failures\n")
        report.write(":" * 50 + "\n\n")

        for category, items in aggregated_data.items():
            report.write(f"Category {category}\n\n")
            for item in items:
                report.write(f"Report Meta:\n{item['report_meta']}\n\n")
                report.write(f"Record:\n{item['record']}\n")
                report.write("-" * 50 + "\n\n")
            
            report.write("=" * 50 + "\n\n")

def main():
    base_dir = Path(__file__).parent

    archives_dir = base_dir / "input" / "archives"
    extracted_dir = base_dir / "work" / "extracted"
    report_file = base_dir / "reports" / f"daily_report{datetime.now().strftime('%Y-%m-%d')}.txt"

    extract_archives(archives_dir, extracted_dir)
    aggregated = aggregate_failures(extracted_dir)
    generate_report(aggregated, report_file)    

if __name__ == "__main__":
    main()