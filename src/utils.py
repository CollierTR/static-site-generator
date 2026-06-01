import os
import shutil
import re
from markdown_parser import markdown_to_html_node

def copy_static_files():
    target_directory_path = os.path.join("public")
    src_directory_path = os.path.join("static")

    if not os.path.exists(src_directory_path):
        raise Exception("src directory does not exist")

    if os.path.exists(target_directory_path):
        shutil.rmtree(target_directory_path)

    os.mkdir(target_directory_path)

    # recursively run for files
    recursive_copy(src_directory_path, target_directory_path)

    return

def recursive_copy(src_path, target_path):
    src_files = os.listdir(src_path)
    for file in src_files:
        if os.path.isfile(os.path.join(src_path, file)):
            shutil.copy(os.path.join(src_path, file), os.path.join(target_path, file))
            print(f"Copying {os.path.join(src_path, file)} file to {os.path.join(target_path, file)}")
        if os.path.isdir(os.path.join(src_path, file)):
            os.mkdir(os.path.join(target_path, file))
            recursive_copy(os.path.join(src_path, file), os.path.join(target_path, file))
            print(f"    Copying {os.path.join(src_path, file)} directory to {os.path.join(target_path, file)}")

def extract_title(markdown):
    match = re.search(r"^#\s+(.*)$", markdown, re.MULTILINE)
    if not match:
        raise Exception("No title in file!")
    return match.group(1)


def generate_page(from_path, template_path, dest_path, base_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    # read file from_path
    with open(from_path, encoding="utf-8") as s:
        src_file = s.read()

    # read template
    with open(template_path, encoding="utf-8") as t:
        template_file = t.read()

    html = markdown_to_html_node(src_file).to_html()
    title = extract_title(src_file)

    template_file = template_file.replace("{{ Title }}", title)
    template_file = template_file.replace("{{ Content }}", html)
    template_file = template_file.replace('href="/', f'href="{base_path}')
    template_file = template_file.replace('src="/', f'href="{base_path}')

    # ensure destination directory exists
    dest_dir = os.path.dirname(dest_path)
    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)

    # write output file
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(template_file)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, base_path):

    files = os.listdir(dir_path_content)

    for file in files:
        if os.path.isdir(os.path.join(dir_path_content, file)):
            generate_pages_recursive(os.path.join(dir_path_content, file), template_path, os.path.join(dest_dir_path, file), base_path)
        else: 
            file_name = f'{file.split(".")[0]}.html'
            generate_page(os.path.join(dir_path_content, file), template_path, os.path.join(dest_dir_path, file_name), base_path)

