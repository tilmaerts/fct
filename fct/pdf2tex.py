#! /usr/bin/env python

import fire
import os
import glob
from tqdm import tqdm


def convert_pdf(pdffile, lan="dan"):
    bname = os.path.basename(pdffile).split(".")[0]
    print("converting pdf to tiff...")
    os.system(f"pdftoppm -tiff -r 300 {pdffile} {bname}")
    outputfiles = sorted(glob.glob(f"{bname}*.tif"))

    buffer = f"\\section{{{bname}}}\n"

    # Add tqdm progress bar
    for i in tqdm(outputfiles, desc="Converting to text"):
        os.system(f"tesseract {i} {i[:-4]} -l {lan}")
        buffer += "\n" + open(f"{i[:-4]}.txt", "r").read()

    # for n, i in enumerate(outputfiles):
    #     os.system(f"tesseract {i} {i[:-4]} -l {lan}")
    #     buffer += "\n" + open(f"{i[:-4]}.txt", "r").read()

    open(f"{bname}.tex", "w").write(buffer)
    print(f"** saved to {bname}.tex")


if __name__ == "__main__":
    fire.Fire(convert_pdf)
