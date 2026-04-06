# -*- coding: utf-8 -*-
from __future__ import annotations

import argparse
import json
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}


def extract_paragraphs(docx_path: Path) -> list[str]:
    with zipfile.ZipFile(docx_path) as zf:
        xml = zf.read("word/document.xml")
    root = ET.fromstring(xml)
    paragraphs: list[str] = []
    for p in root.findall(".//w:body/w:p", NS):
        text = "".join(node.text or "" for node in p.findall(".//w:t", NS)).strip()
        if text:
            paragraphs.append(text)
    return paragraphs


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract paragraph text from a DOCX thesis file.")
    parser.add_argument("docx_path", help="Path to the .docx file")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of plain text")
    args = parser.parse_args()

    docx_path = Path(args.docx_path)
    paragraphs = extract_paragraphs(docx_path)
    if args.json:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8")
        print(json.dumps(paragraphs, ensure_ascii=False, indent=2))
    else:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8")
        print("\n".join(paragraphs))


if __name__ == "__main__":
    main()
