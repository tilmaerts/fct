#!  /usr/bin/env python3
import fire
import re
import pandas as pd
import os
import glob
import fitz
import subprocess
from rapidfuzz import process, fuzz
import numpy as np


def search_for_text_on_page(page, search_string, id, threshold=80):
    # Extract text from the page
    page_text = page.get_text("text")

    # Clean the page text and the search string
    cleaned_page_text = page_text  # clean_text(page_text)
    cleaned_search_string = search_string  # clean_text(search_string)

    # Use rapidfuzz to find the best match
    match = process.extractOne(
        cleaned_search_string,
        [
            cleaned_page_text[i : len(cleaned_search_string) + i]
            for i in range(len(cleaned_page_text) - len(cleaned_search_string))
        ],
        scorer=fuzz.partial_ratio,
        score_cutoff=threshold,
    )

    if match:
        sub = page_text[match[2] : match[2] + len(match[0])].replace("-\n", "")
        text_instances = page.search_for(sub)

        ys, ye = text_instances[0].y0, text_instances[-1].y1
        ymid = 0.5 * (ye + ys)
        points = [
            fitz.Point(page.mediabox[2] - 50, ys),  # Bottom-left
            fitz.Point(page.mediabox[2] - 40, ymid),  # Bottom-right
            fitz.Point(page.mediabox[2] - 50, ye),  # Top-right
        ]

        for i in range(len(points) - 1):
            page.draw_line(
                points[i], points[i + 1], color=(0, 0, 0), width=1
            )  # Black color, 1 pt width

        # path.finish()
        # path.draw(color=(0, 0, 0), width=1)

        c = 0
        for inst in text_instances:
            highlight = page.add_highlight_annot(inst)

            if c == 0:
                # print(page.rotation, page.transformation_matrix, page.rect, inst)
                text = page.insert_text(
                    (page.mediabox[2] - 30, ymid + 3), f"r{id}", color=(0, 0.3, 1)
                )
                # print(type(text))

            c += 1


def parse_biblatex_bbl(file_path):
    with open(file_path, "r") as file:
        content = file.read()

    # Regular expression to match each entry in the .bbl file
    entry_pattern = re.compile(
        r"\\entry{([^}]+)}{([^}]+)}{(.*?)}(.*?)\\endentry", re.DOTALL
    )
    entries = entry_pattern.findall(content)

    id = 1
    parsed_entries = []
    for entry in entries:
        cite_key = entry[0].strip()
        entry_type = entry[1].strip()
        entry_label = entry[2].strip()
        fields_content = entry[3].strip()

        fields_pattern = re.compile(r"\\field\{([^}]+)\}\{([^}]+)\}")
        fields = fields_pattern.findall(fields_content)

        flds = {field[0].strip(): field[1].strip() for field in fields}
        entry_dict = {
            "cite_key": cite_key,
            "id": id,
            "entry_type": entry_type,
            "entry_label": entry_label,
            **flds,
        }
        entry_dict["pages"] = int(entry_dict["pages"]) if "pages" in entry_dict else -1
        parsed_entries.append(entry_dict)
        id += 1

    return parsed_entries


def find_pdf_files(dir, names):
    allpdfs = glob.glob(os.path.join(dir, "*pdf"))
    opdfs = {}
    for i in names:
        if type(i) is str:
            for j in allpdfs:
                istr = i.replace("_", "").replace(" ", "")
                jstr = j.replace("_", "").replace(" ", "")
                ratio = fuzz.partial_ratio(istr, jstr)

                if ratio > 90:  # istr in jstr:
                    opdfs[i] = j

            if i not in opdfs:
                print(f"Could not find pdf for {i}")

    for i in opdfs:
        print(i, opdfs[i])

    return opdfs


def out2ex(bbl, sdir):
    entries = parse_biblatex_bbl(bbl)

    df = pd.DataFrame(entries)

    pdfs = find_pdf_files(sdir, df["journaltitle"].unique().tolist())

    loaded_pdfs = dict([(j, fitz.open(pdfs[j])) for j in pdfs])

    gr = df.groupby(["journaltitle", "pages"])

    # print(df)

    # build inclusion doc
    pg = {}
    for pdf in loaded_pdfs:
        pg1, ids1, keys = [], [], []
        for nm, g in gr:
            if nm[0] == pdf:
                pageno = nm[1]
                ids = g["id"].tolist()
                pg1.append(pageno)
                ids1.extend(ids)
                keys.extend(g["cite_key"].tolist())

        if pdf not in pg:
            pg[pdf] = {"pages": [], "ids": [], "keys": []}

        pg[pdf]["pages"].extend(pg1)
        pg[pdf]["ids"].extend(ids1)
        pg[pdf]["keys"].extend(keys)

    out = ""
    for i in pg:
        pages = set([1] + pg[i]["pages"])
        links = ""
        # print(pg[i])
        cite = ",".join(pg[i]["keys"])

        for j in pg[i]["keys"]:
            links += f"\\cite{{{j}}}"
        out += f"\\incdoc{{{{{','.join([str(j) for j in pages])}}}}}{{{i.replace(',','')}_print.pdf}}{{{i}}}{{referencer: \\cite{{{cite}}} }}\n"

    open("logs.tex", "w").write(out)

    found_ids = np.sort(np.array([id for ids in pg.values() for id in ids["ids"]]))

    all_ids = df.id.values

    for i in all_ids:
        if i not in found_ids:
            print(
                f"did not find {i} in ids, key:", df[df["id"] == i]["cite_key"].iloc[0]
            )

    # create the labelled pdfs
    for pdf in loaded_pdfs:
        # print(pdf, loaded_pdfs[pdf].metadata)
        pages = [i for i in loaded_pdfs[pdf].pages()]
        for nm, group in gr:
            if nm[0] == pdf:
                pageno = nm[1] - 1
                # print(group)
                for title, id in zip(group["title"], group["id"]):
                    search_for_text_on_page(pages[pageno], title, id)

    for i in loaded_pdfs:
        opdf = f"{i}.pdf".replace(",", "")
        loaded_pdfs[i].save(opdf)
        subprocess.call(
            ["pdftocairo", opdf, opdf.replace(".pdf", "_print.pdf"), "-pdf"]
        )


def main():
    fire.Fire(out2ex)


if __name__ == "__main__":
    main()
