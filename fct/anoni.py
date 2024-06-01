#! /usr/bin/env python3

import fire
import yaml
import re


# Function to load mappings from a YAML file
def load_mappings(yaml_file):
    with open(yaml_file, "r") as file:
        mappings = yaml.safe_load(file)
    return mappings


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
    """
    Process a text file by applying mappings from a configuration file to anonymize its content.

    Args:
        text_file (str): The path to the text file to be processed.
        config_file (str): The path to the configuration file containing the mappings.

    Returns:
        None

    Raises:
        FileNotFoundError: If either the text file or the configuration file does not exist.
        IOError: If there is an error reading or writing the files.
    """
    mappings = load_mappings(config_file)
    with open(text_file, "r", encoding="utf-8") as file:
        content = file.read()

    modified_content = apply_mappings(content, mappings)

    # Option: Write to a file or just print it out
    # For this example, I'm printing the output
    # print(modified_content)
    fname = text_file.replace(".txt", "_anon.txt")
    open(fname, "w", encoding="utf-8").write(modified_content)
    print(f"Anonymized version of {text_file} has been written to {fname}")
    print(
        "Note, this is not a guarantee that all identifying information was caught, please update your .yml file until all personal information is caught!"
    )


def main():
    fire.Fire(process_text_file)


# Fire CLI
if __name__ == "__main__":
    main()
