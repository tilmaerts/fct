#! /usr/bin/env python3

import fire
import yaml
import re


# Function to load mappings from a YAML file
def load_mappings(yaml_file):
    with open(yaml_file, "r") as file:
        mappings = yaml.safe_load(file)
    return mappings


# Function to apply mappings to the text content
# def apply_mappings(text, mappings):
#     for pattern, replacement in mappings.items():
#         wildcard_pattern = re.compile(re.escape(pattern).replace(r"\*", ".*"))
#         text = wildcard_pattern.sub(replacement, text)
#     return text


def apply_mappings(text, mappings):
    for pattern, replacement in mappings.items():
        # Replace * with .*, and ? with .
        wildcard_pattern = re.compile(
            re.escape(pattern).replace(r"\*", ".*").replace(r"\?", ".")
        )
        text = wildcard_pattern.sub(replacement, text)
    return text


# Main function for the CLI
def process_text_file(text_file, config_file):
    mappings = load_mappings(config_file)
    with open(text_file, "r", encoding="utf-8") as file:
        content = file.read()

    modified_content = apply_mappings(content, mappings)

    # Option: Write to a file or just print it out
    # For this example, I'm printing the output
    print(modified_content)
    fname = text_file.replace(".txt", "_anon.txt")
    open(fname, "w", encoding="utf-8").write(modified_content)
    print(f"Anonimized version of {text_file} has been written to {fname}")
    print("Please check the file to make sure all personal information was caught!")


def main():
    fire.Fire(process_text_file)


# Fire CLI
if __name__ == "__main__":
    main()
