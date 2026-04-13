import os
import script_utilities.file as fl
import script_utilities.functions as ft

import folders as fd

archive_folder = fd.get_folder("Archive")
input_folder = fd.get_folder("Input")
output_folder = fd.get_folder("Output")

def clear_folder(folder: fl.Folder) -> None:
    for filename in os.listdir(folder.path):
        file = fl.File(os.path.join(folder.path, filename))
        file.delete()

def main() -> None:
    folders = [input_folder, output_folder]
    folder = ft.options_question(folders, "Which folder needs to be cleared?",
                                 list(map(lambda folder:folder.filename, folders)))
    clear_folder(folder)

if __name__ == "__main__":
    main()
