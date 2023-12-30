import os
import subprocess as sp

import Modules.constants as cs
import Modules.distribution as ds
import Modules.file as fl
import Modules.functions as ft
import Modules.track as tr

cwd = os.getcwd()
archive = os.path.join(cwd, "Archive")
contacts = fl.Folder(os.path.join(cwd, "Contacts"))
settings = fl.Folder(os.path.join(cwd, "Settings"))

# Collect distribution information
name = str(input("Enter the name of the distribution: "))
version = str(input(f"Enter the version number of {name}: "))
author = str(input(f"Enter the author(s) of {name}: "))
date = str(input(f"Enter the release date of {name}: "))
tag = str(input(f"Enter the distribution tag of {name}: "))

predecessors = []

for file in os.listdir(archive):
    if file.startswith(name):
        file = os.path.basename(file)
        file = file.replace(f"{name} ", "")
        file = file.replace(".txt", "")
        predecessors.append(file)

if predecessors:
    for x in range(len(predecessors)):
        print(chr(x + 65), ". ", predecessors[x], sep = "")
    
    while True:
        choice = str(input("Which version is the predecessor? (Enter the corresponding option): "))
        
        if len(choice) != 1:
            print("This is not an option. Please try again.")
        elif choice.isalpha() and ord(choice.upper()) - 65 in range(len(predecessors)):
            choice = ord(choice.upper()) - 65
            file = os.path.join(archive, f"{name} {predecessors[choice]}.txt")
            distribution = ds.Distribution(file)
            previous_uuid = distribution.uuid
            break
        else:
            print("This is not an option. Please try again.")
else:
    v = ft.question(f"Does {name} have a predecessor?")
    if v:
        previous_uuid = str(input(f"Enter the UUID of the previous version of {name}: "))
    else:
        previous_uuid = ""

v = ft.question(f"Does {name} have a Wiimmfi region?")
if v:
    region = str(input(f"Enter the region number of {name}: "))
else:
    region = ""

url = str(input(f"Enter the Wiiki article URL of {name}: "))

# Define process mode
for mode, x in zip(cs.modes, range(len(cs.modes))):
    print(f"{chr(x + 65)}. {mode}")

while True:
    mode = str(input("How should the files be processed? (Enter the corresponding letter): ")).upper()
    
    match mode:
        case "A":
            mode = "all-files"
            break
        case "B":
            mode = "my-stuff"
            break
        case "C":
            mode = "le-code"
            break
        case _:
            print("This is not an option. Please try again.")

# Remove non-SZS files
if mode == "my-stuff":
    for file in os.listdir(os.path.join(cwd, "Input")):
        file = fl.File(os.path.join(cwd, "Input", file))
        if not file.filename.endswith("szs") or not file.filename[:-4] in cs.filenames:
            if not file.filename.endswith(".gitignore"):
                file.delete()

# Compress files and create distribution.txt
print("Compressing files...")
os.chdir(os.path.join(cwd, "Input"))
sp.run(["wszst", "compress", "--szs", "--rmai", "*.szs", "-o"])
sp.run(["wszst", "distrib", "."])
os.chdir(cwd)

distribution = fl.TXT(os.path.join(cwd, "Input", "distribution.txt"))

# Write contact and distribution information
print("Writing contact and distribution information...")
ordered_contacts = ["archive", "wiimmfi", "wiiki", "platforms", "email"]
for line, contact in zip([42, 45, 48, 51, 54], ordered_contacts):
    distribution.add_to_line(line, fl.CNT(os.path.join("Contacts", f"{contact}.cnt")).get_value())

distribution.rewrite(68, f"@NAME\t\t= {name}")
distribution.rewrite(69, f"@VERSION\t= {version}")
distribution.rewrite(70, f"@AUTHORS\t= {author}")
distribution.rewrite(73, f"@RELEASE-DATE\t= {date}")
distribution.rewrite(77, f"@REFERENCE-NAME\t= {tag}")
distribution.rewrite(84, f"@PREDECESSOR\t= {previous_uuid}")
distribution.rewrite(87, f"@WIIMMFI-REGION\t= {region}")
distribution.rewrite(89, f"@INFO-URL\t= {url}")

# Remove standard SHA1s
distribution.remove(191, 277)

# Enter track information in distribution.txt
definition = distribution.read()[191 - 1:]
for x in range(len(definition)):
    if definition[x] != "\n" and definition[x] != "":
        information = definition[x].split()
        file = fl.File(os.path.join(cwd, "Input", information[2] + ".szs"))
        track = tr.Track(information[0], information[1], filename = information[2])
        if track.information:
            print(f"{file.filename: <30} is {track.information}.")
        else:
            print(f"{file.filename: <30} is an unknown track.")
        distribution.rewrite(191 + x, str(track))
        if track.information is None:
            file.move(os.path.join(cwd, "Output", file.filename))

# Clean repository
distribution.rename(f"{name} {version}.txt")
distribution.move(os.path.join(cwd, "Output", distribution.filename))

gitignore = fl.File(os.path.join(cwd, "Input", ".gitignore"))
gitignore.rename("tmp.gitignore")
gitignore.move_up(1)
fl.Folder(os.path.join(cwd, "Input")).empty()
gitignore.move_down(["Input"])
gitignore.rename(".gitignore")

input("All done!")
os.system(f"start notepad++ \"{distribution.path}\"")
