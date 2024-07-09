#!  /usr/bin/env python3
import fire
import re
import pandas as pd
import os
import glob
import fitz
import subprocess
from rapidfuzz import process, fuzz


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
        c = 0
        for inst in text_instances:
            highlight = page.add_highlight_annot(inst)
            if c == 0:
                page.insert_text(
                    (page.mediabox[2] - 25, inst[3]), f"{id}", color=(0, 0.3, 1)
                )
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

    # build inclusion doc
    pg = {}
    for pdf in loaded_pdfs:
        pg1 = []
        for nm, g in gr:
            if nm[0] == pdf:
                pageno = nm[1]
                pg1.append(pageno)

        if pdf not in pg:
            pg[pdf] = []
        pg[pdf].extend(pg1)

    out = ""
    for i in pg:
        pages = set([1] + pg[i])
        out += f"\\incdoc{{{{{','.join([str(j) for j in pages])}}}}}{{{i.replace(',','')}_print.pdf}}{{{i}}}{{}}\n"

    open("logs.tex", "w").write(out)

    # create the labelled pdfs
    for pdf in loaded_pdfs:
        pages = [i for i in loaded_pdfs[pdf].pages()]

        for nm, group in gr:
            if nm[0] == pdf:
                pageno = nm[1] - 1
                print(group)
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
