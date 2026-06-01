from utils import copy_static_files, generate_page, generate_pages_recursive
from sys import argv
from os import path

 
def main():

    base_path = "/"

    if argv[1]:
        base_path = argv[1]

    copy_static_files()
    generate_pages_recursive("content/", "template.html", "docs/", base_path)


main()
