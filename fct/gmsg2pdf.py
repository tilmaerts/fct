#! /usr/bin/env python

import bs4
import fire
import subprocess


def parse(filename: str):
    def parse(filename: str) -> None:
        """
        Parse the given HTML file, downloaded from google messages for web (rightclick download the page with the thread you want as pdf) and convert the text messages into a PDF file.
        Args:
            filename (str): The path to the HTML file.
        Returns:
            None
        """

    file = open(filename, "r")

    soup = bs4.BeautifulSoup(file, "html.parser")

    messages = soup.find_all("div", class_="text-msg msg-content")
    msgparts = soup.find_all("mws-text-message-part")

    print(msgparts)

    buf = ""
    for i in msgparts:
        buf += i.get("aria-label") + "\n\n***\n\n"

    open("__tmp__.md", "w").write(buf)

    of = "sms_messages.pdf"
    subprocess.run(["pandoc", "__tmp__.md", "-o", of, "--pdf-engine=weasyprint"])
    print(f"Output file: {of}")


def main():
    fire.Fire(parse)


if __name__ == "__main__":
    main()
