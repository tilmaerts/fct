import os
import shutil
import importlib.util


def main():
    destination = os.path.join(os.getcwd(), "examples")
    module_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "fct_examples")
    )

    print(module_path)
    if os.path.exists(destination):
        print(f"Directory {destination} already exists.")
        return

    spec = importlib.util.spec_from_file_location("module_name", module_path)

    print(spec)

    shutil.copytree(module_path, destination)
    print(f"Examples directory created at {destination}")
