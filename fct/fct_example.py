import os
import shutil
import importlib.util


def main():
    destination = os.path.join(os.getcwd(), "examples")
    destinationr = os.path.join(os.getcwd(), "examples", "fct_resources")

    module_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "fct_examples")
    )
    module_path_resources = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "fct_resources")
    )

    # print(module_path)
    if os.path.exists(destination):
        print(f"Directory {destination} already exists.")
        return

    # spec = importlib.util.spec_from_file_location("module_name", module_path)

    # print(spec)

    shutil.copytree(module_path, destination)
    shutil.copytree(module_path_resources, destinationr)
    print(f"Examples directory created at {destination}")
