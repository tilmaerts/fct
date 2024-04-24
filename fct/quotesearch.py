#! /usr/bin/env python3
import bibtexparser
import fitz  # PyMuPDF
import numpy as np

import re

from unidecode import unidecode
import argparse
from rapidfuzz import fuzz
import os


def load_bibtex_titles(bibtex_file):
    """
    Loads titles from a BibTeX file.

    Args:
    - bibtex_file (str): The path to the BibTeX file.

    Returns:
    - A list of titles (str) found in the BibTeX file.
    """
    with open(bibtex_file) as bibtex_file:
        bibtex_str = bibtex_file.read()

    bib_database = bibtexparser.loads(bibtex_str)
    # titles = [entry["title"] for entry in bib_database.entries]
    # return titles
    return bib_database


def normalize_text(text):
    """
    Normalize text by removing punctuation, spaces, and making it lowercase.
    """
    # Remove LaTeX formatting, punctuation, spaces, and make lowercase
    return re.sub(r"\W+", "", text).lower()


def search_titles_in_pdfs(bib_database, pdf_files, output="output.bib"):
    """
    Searches for titles in a list of PDF files and prints the file name and page number where each title is found.

    Args:
    - titles (list): A list of titles (str) to search for.
    - pdf_files (list): A list of PDF file paths.
    """
    global docs, titles, pages

    docs = [fitz.open(pdf_file) for pdf_file in pdf_files]

    titles = [normalize_text(entry["title"]) for entry in bib_database.entries]

    pages = [
        (doc.name, page_num + 1, normalize_text(page.get_text()))
        for doc in docs
        for page_num, page in enumerate(doc)
    ]

    for n, t in enumerate(titles):
        for p in pages:
            pct = fuzz.partial_ratio(t, p[2])

            if pct > 85.0 and len(p[2]) > len(t) * 0.8:
                # print(pct, len(p[2]), p[2])
                # print(t, p[2])
                print(f'Title "{t}" found in {p[0]} on page {p[1]} ({pct}%)')
                bib_database.entries[n]["journal"] = unidecode(
                    (os.path.basename(p[0]).replace("_", " ").replace(".pdf", ""))
                )
                bib_database.entries[n]["pages"] = str(p[1])
                break

    for e in bib_database.entries:
        if "note" in e:
            del e["note"]

    bibtexparser.dump(bib_database, open(output, "w"))
    print(f"Output written to {output}")


def main():
    parser = argparse.ArgumentParser(
        description="Search for titles in a bibtex file in a series of pdf files. Add the page numbers to the bibtex file. "
    )
    parser.add_argument("bibtex_file", help="Path to the BibTeX file")
    parser.add_argument("pdf_files", nargs="+", help="Paths to the PDF files")
    parser.add_argument(
        "--output",
        "-o",
        default="output.bib",
        help="Path to the output BibTeX file (default: output.bib)",
    )
    args = parser.parse_args()

    bibtex_file = args.bibtex_file
    pdf_files = args.pdf_files

    bibtex = load_bibtex_titles(bibtex_file)
    bdb = search_titles_in_pdfs(bibtex, pdf_files, args.output)


if __name__ == "__main__":
    main()
