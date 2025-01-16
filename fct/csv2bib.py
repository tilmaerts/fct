#! /usr/bin/env python

import pandas as pd
import argparse
import re
import os
from datetime import datetime
import demoji
import yaml

REBUT_TEMPLATE = r"""
\documentclass[12pt]{article}

      \usepackage{hyperref}
      \usepackage[backend=biber,style=numeric]{biblatex}
      \addbibresource{label_table.bib}

      \usepackage[breakable]{tcolorbox}
      \usepackage[danish]{babel}

      \newcommand{\bcite}[1]{\begin{tcolorbox}[left skip=0cm,   size=fbox, arc=1mm, boxsep=0mm,left=1mm, right=1mm, top=1mm, bottom=1mm, colframe=black, colback=white,box align=base, breakable]
      {\small \cite{#1}: \fullcite{#1}}
      \end{tcolorbox}}
      \usepackage{enumitem}
      \newcounter{globalenumi}
      
      % Custom enumerate environment using the global counter
      \newenvironment{cenum}
      {
          \begin{enumerate}
              \setcounter{enumi}{\value{globalenumi}} % Set enumi to the global counter
              }
              {
              \setcounter{globalenumi}{\value{enumi}} % Save enumi back to the global counter
          \end{enumerate}
      }


\begin{document}
\section*{}
Dato: \today


\begin{cenum}
POINTS
\end{cenum}

\end{document}

"""


def replace_multiple_spaces(s):
    try:
        return re.sub(r" +", " ", s)
    except TypeError:
        print(s)
        return ""


def replace_underscores(s):
    try:
        return re.sub(r"_", " ", s)
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


def emojis_to_text(s):
    # Replace all emojis in the content
    return demoji.replace(s, "(emoji)")


def load_uuid_prefix(csv_file_path):
    # Get the directory of the CSV file
    csv_dir = os.path.dirname(csv_file_path)
    info_file_path = os.path.join(csv_dir, "info.yml")

    # Check if info.yml exists
    if os.path.exists(info_file_path):
        with open(info_file_path, "r") as info_file:
            info_data = yaml.safe_load(info_file)
            # Extract the uuid field and return the first 4 characters
            if "uuid" in info_data:
                return info_data["uuid"][:4]
    return ""


def table_to_bib(df, output_file, exclude_note, uuid_prefix=""):
    df["date"] = pd.to_datetime(df["date"], dayfirst=True, errors="coerce")

    print("Writing to", output_file)
    with open(output_file, "w") as bibtex_file:
        for index, row in df.iterrows():
            label_title = row["latex_label"]
            bibtex_entry = f"""@article{{ {label_title}  ,
    note = {{{row["note"]}}},
    title = {{{replace_underscores(replace_multiple_spaces(remove_backslash_substrings(row["quote"])))}}},
    journal = {{{replace_underscores(replace_multiple_spaces(remove_curly_brace_content(remove_backslash_substrings(row["section title"]))))}}},
    date = {{{row["date"].strftime("%Y-%m-%d") if not pd.isnull(row["date"]) else ""}}},
    }}
    """
            if exclude_note:
                bibtex_entry = bibtex_entry.replace("note =", "nonote =")
            # Write the BibTeX entry to the file
            bibtex_file.write(emojis_to_text(bibtex_entry))


def base_rebuttal(df):
    latex_body = ""
    for i, row in df.iterrows():
        latex_body += f"\t% {row['note']}\n"
        latex_body += f"\t\\item Angående citat: \\bcite{{{row['latex_label']}}} \n"

    if not os.path.exists("rebuttal.tex"):
        with open("rebuttal.tex", "w") as rebuttal_file:
            rebuttal_file.write(REBUT_TEMPLATE.replace("POINTS", latex_body))
            print("written a new rebuttal.tex")

    print("updated rebut points", latex_body)


def process_csv_files(csv_files, output_file, exclude_note):
    csvs = []
    for csv_file in csv_files:
        print(f"Loading {csv_file}")
        csvs.append(pd.read_csv(csv_file, sep=" ; ", engine="python"))
        csvs[-1]["doc"] = os.path.basename(csv_file).split("_labels")[0]

    uuid_prefix = load_uuid_prefix(csv_files[0])

    df = pd.concat(csvs)

    df["latex_label"] = [f"{uuid_prefix}:{label.strip()}" for label in df["label"]]

    df.to_excel("label_table.xlsx")

    table_to_bib(df, output_file, exclude_note, uuid_prefix=uuid_prefix)

    base_rebuttal(df)


def parse_arguments():
    p = argparse.ArgumentParser()
    p.add_argument(
        "csvs",
        nargs="*",
        help="csv/txt file to be converted to bib, sep = ",
        default="label_table.txt",
    )
    p.add_argument("-o", "--output", help="output file name", default="label_table.bib")
    p.add_argument("-n", "--nonote", help="exclude note field", action="store_true")
    return p.parse_args()


def main():
    args = parse_arguments()
    process_csv_files(args.csvs, args.output, args.nonote)


if __name__ == "__main__":
    main()
