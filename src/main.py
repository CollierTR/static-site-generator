from utils import copy_static_files, generate_page, generate_pages_recursive
from sys import argv
from os import path

 
def main():

    base_path = argv[1].rstrip("/") if len(argv) > 1 else "/"

    print(f"base_path = {base_path}")

    copy_static_files()
    generate_pages_recursive("content/", "template.html", "docs/", base_path)


main()
