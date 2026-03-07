import os
import script_utilities.file as fl

def get_folder(name: str) -> fl.Folder:
    cwd = os.getcwd()
    folder = fl.Folder(os.path.join(cwd, name))
    return folder

def generate_folders() -> None:
    for folder in ["Archive", "Input", "Output"]:
        folder = get_folder(folder)
        if not bool(folder):
            os.mkdir(folder.path)
