#! /usr/bin/env python

import pandas as pd
import argparse
import re
import os
from datetime import datetime


def replace_multiple_spaces(s):
    try:
        return re.sub(r" +", " ", s)
    except TypeError:
        print(s)
        return ""


def remove_curly_brace_content(s):
    try:
        return re.sub(r"\{.*?\}", "", s).replace(".06em", "")
    except TypeError:
        print(s)
        return ""


def remove_backslash_substrings(s):
    try:
        return re.sub(r"\\[^ ]*", "", s)
    except TypeError:
        print(s)
        return ""


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument(
        "csvs",
        nargs="*",
        help="csv/txt file to be converted to bib, sep = ",
        default="label_table.txt",
    )
    p.add_argument("-o", "--output", help="output file name", default="label_table.bib")
    args = p.parse_args()
    # Read CSV file into a pandas DataFrame

    csvs = []
    for i in args.csvs:
        print(f"Loading {i}")
        csvs.append(pd.read_csv(i, sep=" ; ", engine="python"))
        csvs[-1]["doc"] = os.path.basename(i).split("_labels")[0]

    df = pd.concat(csvs)
    df["date"] = pd.to_datetime(df["date"], dayfirst=True, format="mixed")
    of = args.output
    print("Writing to", of)
    # Open a file to write the BibTeX entries
    with open(of, "w") as bibtex_file:
        for index, row in df.iterrows():
            bibtex_entry = f"""@article{{ {row["label"]}  ,
    note = {{{row["note"]}}},
    title = {{{replace_multiple_spaces(remove_backslash_substrings(row["quote"]))}}},
    journal = {{{replace_multiple_spaces(remove_curly_brace_content( remove_backslash_substrings( row["section title"])))}}},
    year = {{{row["date"].year}}}, 
    month = {{{row["date"].month}}},
    day = {{{row["date"].day}}},
    }}
    """
            # Write the BibTeX entry to the file
            bibtex_file.write(bibtex_entry)
