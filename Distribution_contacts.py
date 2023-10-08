import os

import Modules.constants as cs
import Modules.file as fl
import Modules.functions as ft

cwd = os.getcwd()
contacts = fl.Folder(os.path.join(cwd, "Contacts"))

def main():
    while True:
        # Print all settings
        print("Current contact information: ")
        [print(fl.CNT(os.path.join(contacts.path, contact + ".cnt"))) for contact in cs.contacts]
        
        # Print setting selection screen
        print()
        for contact, x in zip(cs.contacts, range(len(cs.contacts))):
            print(chr(x + 65), ". ", contact, sep = "")
        print("X. Exit the menu")
        
        contact = str(input("Which piece of contact information should be edited? (Enter the corresponding letter): ")).upper()
        
        match contact:
            case "A":
                cnt = fl.CNT(os.path.join(contacts.path, "archive.cnt"))
                print("The current value is:", cnt.get_value())
                archive = str(input("Enter username on Wiimm's CT-Archive: "))
                
                cnt.set_value(archive)
                ft.clear_screen()
            case "B":
                cnt = fl.CNT(os.path.join(contacts.path, "email.cnt"))
                print("The current value is:", cnt.get_value())
                email = str(input("Enter e-mail address: "))
                
                cnt.set_value(email)
                ft.clear_screen()
            case "C":
                cnt = fl.CNT(os.path.join(contacts.path, "platforms.cnt"))
                print("The current value is:", cnt.get_value())
                platforms = str(input("Enter other usernames on different platforms in \"service=name\" format, separated by a comma: "))
                
                cnt.set_value(platforms)
                ft.clear_screen()
            case "D":
                cnt = fl.CNT(os.path.join(contacts.path, "wiiki.cnt"))
                print("The current value is:", cnt.get_value())
                wiiki = str(input("Enter username on the Custom Mario Kart Wiiki: "))
                
                cnt.set_value(wiiki)
                ft.clear_screen()
            case "E":
                cnt = fl.CNT(os.path.join(contacts.path, "wiimmfi.cnt"))
                print("The current value is:", cnt.get_value())
                wiimmfi = str(input("Enter username on Wiimmfi: "))
                
                cnt.set_value(wiimmfi)
                ft.clear_screen()
            case "X":
                break
            case _:
                print("This is not an option. Please try again.")
    
    input("All done!")

if __name__ == "__main__":
    main()
