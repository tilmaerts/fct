#! /usr/bin/env python3
import fire
import os
import fitz


def convert(pdf_file):
    # Get the base name of the PDF file without the extension
    base_name = os.path.splitext(os.path.basename(pdf_file))[0]

    # Open the PDF file
    with fitz.open(pdf_file) as doc:
        # Get the text from each page of the PDF
        text = ""
        for page in doc:
            text += page.get_text()

    # Create the .tex file with the section title
    oname = base_name.replace(" ", "_").lower()
    tex_file = f"{oname}.tex"
    with open(tex_file, "w") as file:
        file.write(f"\\section{{{base_name}}}\n\n{text}")

    print(f"Successfully converted {pdf_file} to {tex_file}")


if __name__ == "__main__":
    fire.Fire(convert)
