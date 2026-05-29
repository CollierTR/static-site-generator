import os
import shutil

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
