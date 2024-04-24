#! /usr/bin/env python3
from email import policy
from email.parser import BytesParser
from email.utils import parsedate_to_datetime
import os
import argparse


def pretty_print_message(message_text):
    lines = message_text.split("\n")
    msg = {}
    key = 0
    for line in lines:
        ll = line.replace(" >", ">")
        if ll.startswith(">"):
            key = len(ll.split()[0])

        if key not in msg:
            msg[key] = []

        msg[key].append(ll[key + (key > 0) :].strip() + "\n")  # + "\n"

    buf = ""
    for i in msg:
        buf += f"\\begin{{addmargin}}[{i*(2./len(msg))}cm]{{0cm}}\n"
        for j in msg[i]:
            if not (buf.endswith("\n\n") and j.startswith("\\newline")):
                buf += j
        buf += "\\end{addmargin}\n"

    return buf


def load_and_parse_eml(eml_path):
    with open(eml_path, "rb") as f:
        msg = BytesParser(policy=policy.default).parse(f)
    return msg


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("eml_path", help="Path to .eml file")
    args = p.parse_args()
    eml_path = args.eml_path
    bname = os.path.splitext(eml_path)[0]
    oname = bname.lower().replace(" ", "_")

    msg = load_and_parse_eml(eml_path)
    dt = parsedate_to_datetime(msg["Date"])
    dtb = dt.strftime("%d-%m-%Y")
    out = f"\section{{Email tråd: {os.path.split(bname)[-1]} {dtb} }}\label{{sec:email_{os.path.split(oname)[-1]}}}\n".replace(
        "_", "\_"
    )
    out += "\sdate{" + dtb + "}\n"
    out += f'{msg["From"]}  skrev: \\newline \n'
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                email_content = part.get_payload(decode=True).decode(
                    "utf-8", errors="replace"
                )
                out += pretty_print_message(email_content)
    else:
        email_content = msg.get_payload(decode=True).decode("utf-8", errors="replace")
        out += pretty_print_message(email_content)

    out = (
        out.replace(">", "\\textgreater ").replace("<", "\\textless ").replace("%", "")
    )
    of = f"{oname}.tex"
    open(of, "w").write(out)
    print(f"Saved to {of}")
