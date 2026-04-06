# -*- coding: utf-8 -*-
from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path


def _has_module(name: str) -> bool:
    return importlib.util.find_spec(name) is not None


def extract_with_pypdf(pdf_path: Path) -> str:
    from pypdf import PdfReader  # type: ignore

    reader = PdfReader(str(pdf_path))
    texts = []
    for page in reader.pages:
        texts.append(page.extract_text() or "")
    return "\n".join(texts).strip()


def extract_with_pypdf2(pdf_path: Path) -> str:
    from PyPDF2 import PdfReader  # type: ignore

    reader = PdfReader(str(pdf_path))
    texts = []
    for page in reader.pages:
        texts.append(page.extract_text() or "")
    return "\n".join(texts).strip()


def extract_with_pdfplumber(pdf_path: Path) -> str:
    import pdfplumber  # type: ignore

    texts = []
    with pdfplumber.open(str(pdf_path)) as pdf:
        for page in pdf.pages:
            texts.append(page.extract_text() or "")
    return "\n".join(texts).strip()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extract text from a PDF thesis file using locally available libraries."
    )
    parser.add_argument("pdf_path", help="Path to the .pdf file")
    args = parser.parse_args()

    pdf_path = Path(args.pdf_path)

    if _has_module("pypdf"):
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8")
        print(extract_with_pypdf(pdf_path))
        return
    if _has_module("PyPDF2"):
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8")
        print(extract_with_pypdf2(pdf_path))
        return
    if _has_module("pdfplumber"):
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8")
        print(extract_with_pdfplumber(pdf_path))
        return

    sys.stderr.write(
        "PDF extraction is unavailable in the current environment. "
        "No supported library was found among: pypdf, PyPDF2, pdfplumber.\n"
    )
    raise SystemExit(2)


if __name__ == "__main__":
    main()
