#! /usr/bin/env python

import fire

# import pylatexenc

from pylatexenc.latexencode import unicode_to_latex


def remove_unicode(tex):
    txt = open(tex, "r").read()

    buf = ""
    for i in txt:
        try:
            ch = i.encode("utf-8")
            buf += i
        except UnicodeEncodeError:
            print(f"Unicode character found: {i}")
            # txt = txt.replace(i, "")
            buf += " "

    print(txt)

    # tex_body = unicode_to_latex(txt)

    # with open(tex.replace(".tex", "_utf8.tex"), "w") as outfile:
    #     outfile.write(tex_body)

    # print(f"Saved to {tex.replace('.tex', '_utf8.tex')}")


# def remove_unicode(tex):
#     txt = open(tex, "r").read()

#     tex_body = unicode_to_latex(txt)

#     with open(tex.replace(".tex", "_utf8.tex"), "w") as outfile:
#         outfile.write(tex_body)

#     print(f"Saved to {tex.replace('.tex', '_utf8.tex')}")


def main():
    fire.Fire(remove_unicode)


if __name__ == "__main__":
    main()
