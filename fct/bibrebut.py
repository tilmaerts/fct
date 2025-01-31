#! /usr/bin/env python
import bibtexparser as bib
import argparse
import os

REBUT_TEMPLATE = r"""\documentclass[12pt]{article}
    \usepackage{tabularx}
    \usepackage{hyperref}
    \usepackage[backend=biber,style=numeric,sorting=none]{biblatex}
    \addbibresource{BIBPATH}
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
\noindent\begin{tabularx}{\textwidth}{l|X}
      \textbf{Emne}   &       \\
      \textbf{Sagsnr}&        \\
      \textbf{Parter}&        \\
      \textbf{Dato}  & \today \\
\end{tabularx}

\begin{cenum}
POINTS
\end{cenum}

\printbibliography[title={Referencer}]

\end{document}
"""


def base_rebuttal(bibfile):
    bibdb = bib.load(open(bibfile))

    latex_body = ""
    for row in bibdb.entries:
        latex_body += (
            f"\t% prompt: {row['nonote'] if 'nonote' in row else row['nonote']}\n"
        )
        latex_body += f"\t\\item Angående citat: \\bcite{{{row['ID']}}} \n"

    rebuttal_body = REBUT_TEMPLATE.replace("POINTS", latex_body).replace(
        "BIBPATH", os.path.abspath(bibfile)
    )
    print("\n\n\n", rebuttal_body)
    return rebuttal_body


def write_rebuttal(body, output_file):
    if not os.path.exists(output_file):
        with open(output_file, "w") as rebuttal_file:
            rebuttal_file.write(body)
            print(f"Written a new {output_file}")
    else:
        print(f"{output_file} already exists. Not overwriting.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("bibfile", help="The bib file to use")
    parser.add_argument(
        "-o",
        "--output",
        default="rebut.tex",
        help="The output file (default: rebut.tex)",
    )
    args = parser.parse_args()
    rebuttal = base_rebuttal(args.bibfile)
    write_rebuttal(rebuttal, args.output)


if __name__ == "__main__":
    main()
