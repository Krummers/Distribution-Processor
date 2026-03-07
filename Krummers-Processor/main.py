import script_utilities.functions as ft

import folders as fd
import process
import upload

import Modules.enumerables as eb

def main() -> None:
    fd.generate_folders()
    
    while True:
        actions = list(eb.Action)
        display = [action.name for action in actions]
        action = ft.options_question(actions,
                                     "What action needs to be performed?",
                                     display)
        
        match action.name:
            case "Process":
                process.main()
            case "Upload":
                upload.main()
            case "Exit":
                return

if __name__ == "__main__":
    main()
