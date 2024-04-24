#! /usr/bin/env python3
import fire
import os
import pandas as pd
from email import policy
from email.parser import BytesParser
from email.utils import parsedate_to_datetime


def pretty_print_message(message_text):
    lines = message_text.split("\n")
    msg = {}
    for line in lines:
        ll = line.lstrip(">")
        num_prefix = len(line) - len(ll)  # count the number of ">" prefixes
        ll = ll.strip()  # remove leading and trailing whitespace
        if num_prefix not in msg:
            msg[num_prefix] = []
        msg[num_prefix].append(ll)
    for key in msg:
        msg[key] = "\n".join(msg[key])
    return msg


def load_and_parse_eml(eml_path):
    with open(eml_path, "rb") as f:
        msg = BytesParser(policy=policy.default).parse(f)
    return msg


def convert_eml_to_parquet(eml_path):
    bname = os.path.splitext(eml_path)[0]
    oname = bname.lower().replace(" ", "_")

    msg = load_and_parse_eml(eml_path)
    dt = parsedate_to_datetime(msg["Date"])
    dtb = dt.strftime("%d-%m-%Y")
    sender = msg["From"]
    recipients = msg["To"]
    subject = msg["Subject"]
    thread_name = os.path.basename(eml_path)

    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                email_content = part.get_payload(decode=True).decode(
                    "utf-8", errors="replace"
                )
                email_content = pretty_print_message(email_content)
    else:
        email_content = msg.get_payload(decode=True).decode("utf-8", errors="replace")
        email_content = pretty_print_message(email_content)

    print(email_content)

    df = pd.DataFrame(
        [[dtb, sender, recipients, subject, thread_name, email_content[0]]],
        columns=["Date", "Sender", "Recipients", "Subject", "Thread Name", "Body"],
    )

    of = f"{oname}.parquet"
    df.to_parquet(of)

    print(f"Saved to {of}")


if __name__ == "__main__":
    fire.Fire(convert_eml_to_parquet)
