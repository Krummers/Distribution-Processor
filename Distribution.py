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
            predecessor = ds.Distribution(file, load_tracks = False)
            previous_uuid = predecessor.uuid
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
        case "D":
            mode = "pulsar"
            break
        case _:
            print("This is not an option. Please try again.")

# Remove non-SZS files and collect rel files
rel = []
if mode == "my-stuff":
    for file in os.listdir(os.path.join(cwd, "Input")):
        file = fl.File(os.path.join(cwd, "Input", file))
        if file.filename.endswith("rel"):
            rel.append(fl.REL(file.path))
            continue
        if not file.filename.endswith("szs") or not file.filename[:-4].lower() in cs.filenames:
            if not file.filename.endswith(".gitignore") and not file.filename.endswith(".rel"):
                file.delete()

if mode == "pulsar":
    for file in os.listdir(os.path.join(cwd, "Input")):
        file = fl.File(os.path.join(cwd, "Input", file))
        if file.filename.endswith("szs"):
            file.rename(f"pulsar{file.filename}")

# Process rel files
if rel and all(static == rel[0] for static in rel):
    tracklist = rel[0].tracklist()
else: # handle staticR.rel inequality
    tracklist = {}

# Compress files and create distribution.txt
print("Compressing files...")
os.chdir(os.path.join(cwd, "Input"))
sp.run(["wszst", "compress", "--szs", "--rmai", "*.szs", "-o"])
sp.run(["wszst", "distrib", "."])
os.chdir(cwd)

distribution = fl.TXT(os.path.join(cwd, "Input", "distribution.txt"))

# Write contact and distribution information
print("Writing contact and distribution information...")
for line, contact in zip(list(range(112, 127, 3)), cs.ordered_contacts):
    distribution.add_to_line(line, fl.CNT(os.path.join("Contacts", f"{contact}.cnt")).get_value())

distribution.rewrite(distribution.find("@NAME"), f"@NAME\t\t= {name}")
distribution.rewrite(distribution.find("@VERSION"), f"@VERSION\t= {version}")
distribution.rewrite(distribution.find("@AUTHORS"), f"@AUTHORS\t= {author}")
distribution.rewrite(distribution.find("@RELEASE-DATE"), f"@RELEASE-DATE\t= {date}")
distribution.rewrite(distribution.find("@PREDECESSOR"), f"@PREDECESSOR\t= {previous_uuid}")
distribution.rewrite(distribution.find("@WIIMMFI-REGION"), f"@WIIMMFI-REGION\t= {region}")
distribution.rewrite(distribution.find("@INFO-URL"), f"@INFO-URL\t= {url}")

# Remove standard SHA1s
begin = distribution.find("bt --------o -o---- 9047f6e9b77c6a44accb46c2237609b80e459fdc")
end = distribution.find("vs -----d--o -o---- 7142361ab93d3929f62aa715509fc8d1379afbd6")
distribution.remove(begin, end + 2)

# Enter track information in distribution.txt
definition = distribution.read()[distribution.find("# for racing tracks") + 2:]
for x in range(len(definition)):
    if definition[x] != "\n" and definition[x] != "":
        information = definition[x].split()
        file = fl.File(os.path.join(cwd, "Input", information[2] + ".szs"))
        if mode != "pulsar":
            track = tr.Track(information[0], information[1], filename = information[2])
        else:
            number = int(information[2][6:])
            cup = f"{number // 4 + 8}.{number % 4 + 1}"
            pulsar = information[2][6:]
            track = tr.Track(information[0], cup, slot = number + 256, filename = pulsar)
        if track.information:
            print(f"{file.filename: <30} is {track.information}.")
        else:
            print(f"{file.filename: <30} is an unknown track.")
        distribution.rewrite(begin + x, str(track))
        if track.information is None:
            file.move(os.path.join(cwd, "Output", file.filename))

# Compare distribution to predecessor
print("Checking distribution...")
distrib = ds.Distribution(os.path.join(cwd, "Input", "distribution.txt"))
if predecessors:
    print("Comparing distribution to predecessor...")
    predecessor.load_tracks()
    distrib.compare(predecessor)
else:
    distrib.check_again()

if mode == "pulsar":
    distrib.sort_tracks()

if tracklist:
    for x in range(len(distrib.tracks)):
        distrib.tracks[x].set_cup(tracklist[str(distrib.tracks[x].cup)])
    distrib.sort_tracks()

distribution.write(str(distrib).split("\n"))

# Clean repository
distribution.rename(f"{name} {version}.txt")
distribution.move(os.path.join(cwd, "Output", distribution.filename))

gitignore = fl.File(os.path.join(cwd, "Input", ".gitignore"))
gitignore.rename("tmp.gitignore")
gitignore.move_up(1)
fl.Folder(os.path.join(cwd, "Input")).empty()
gitignore.move_down(["Input"])
gitignore.rename(".gitignore")

os.system(f"start notepad++ \"{distribution.path}\"")
input("Press enter to move the file into the archive: ")
distribution.move(os.path.join(cwd, "Archive", distribution.filename))
input("All done!")
