from utils import copy_static_files, generate_page, generate_pages_recursive
 
def main():
    copy_static_files()
    generate_pages_recursive("content/", "template.html", "public/")


main()
