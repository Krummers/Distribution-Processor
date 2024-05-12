import os
import subprocess as sp

import Modules.constants as cs
import Modules.distribution as ds
import Modules.entry as et
import Modules.file as fl
import Modules.functions as ft

cwd = os.getcwd()
archive = os.path.join(cwd, "Archive")
contacts = fl.Folder(os.path.join(cwd, "Contacts"))
settings = fl.Folder(os.path.join(cwd, "Settings"))

# Collect distribution information
name = str(input("Enter the name of the distribution: "))
version = str(input(f"Enter the version number of {name}: "))
author = str(input(f"Enter the author(s) of {name}: "))
date = str(input(f"Enter the release date of {version} of {name}: "))

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

# Open predecessor before continuing
if predecessors:
    os.system(f"start notepad++ \"{predecessor.file.path}\"")

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
        choice = str(input("What engine does the distribution use? (Enter the corresponding option): ")).upper()
        
        if len(choice) != 1:
            print("This is not an option. Please try again.")
        elif choice.isalpha() and ord(choice.upper()) - 65 in range(len(cs.modes)):
            choice = ord(choice.upper()) - 65
            mode = cs.modes[choice]
            break
        else:
            print("This is not an option. Please try again.")

compress = ft.question("Compress all SZS files?")

# Collect REL files and generate track listing if they exist
rel = []
for file in os.listdir(os.path.join(cwd, "Input")):
    file = fl.File(os.path.join(cwd, "Input", file))
    if file.filename.endswith("rel"):
        rel.append(fl.REL(file.path))
if rel and all(static == rel[0] for static in rel):
    tracklist = rel[0].tracklist()
else:
    tracklist = cs.tracklist

if mode == "Mario Kart Wii":
    # Rename all track files to "*tmp.szs" to avoid renaming issues
    print("Renaming regular files...")
    for file in os.listdir(os.path.join(cwd, "Input")):
        file = fl.File(os.path.join(cwd, "Input", file))
        if file.filename.endswith("szs") and file.filename[:-4].lower() in cs.filenames:
            file.rename(file.filename[:-4] + "tmp.szs")
    
    # Rename all track files to their new locations
    for file in os.listdir(os.path.join(cwd, "Input")):
        file = fl.File(os.path.join(cwd, "Input", file))
        if file.filename.endswith("szs") and file.filename[:-7].lower() in cs.filenames:
            old = cs.fcups[file.filename[:-7]]
            new = cs.cfilenames[tracklist[old]]
            file.rename(f"{new}.szs")

# Rename SZS files for proper sorting
if mode == "Pulsar":
    print("Renaming custom files...")
    for file in os.listdir(os.path.join(cwd, "Input")):
        file = fl.File(os.path.join(cwd, "Input", file))
        if file.filename.endswith("szs") and file.filename[:-4].isnumeric():
            track = int(file.filename[:-4])
            # 4 tracks per cup | Pulsar starts 8 cups ahead | Cup 0 does not exist
            cup = track // 4 + 8 + 1
            # 4 tracks per cup | Track 0 does not exist
            slot = track % 4 + 1
            file.rename(f"{cup}.{slot}.szs")

# Compress files and create distribution.txt
os.chdir(os.path.join(cwd, "Input"))
if compress:
    print("Compressing files...")
    sp.run(["wszst", "compress", "--szs", "--norm", "*.szs", "-o"])
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

# Prepare ID and family sets for distribution and predecessor
if predecessors:
    print("Loading predecessor...")
    old_families, old_IDs = predecessor.families_IDs()
else:
    old_IDs = set(x for x in range(100_000))
    old_families = set(x for x in range(100_000))
new_IDs = set()

# Collect and fill out track information in distribution file
print("Processing distribution...")
definition = distribution.read()[distribution.find("# for racing tracks") + 2:]
for x in range(len(definition)):
    if definition[x] != "\n" and definition[x] != "":
        # Split collected information
        information = definition[x].split()
        sha1 = information[0]
        try:
            filename = information[2]
        except IndexError:
            filename = information[1]
        
        # Collect and write information, and move file accordingly
        file = fl.File(os.path.join(cwd, "Input", f"{filename}.szs"))
        entry = et.Entry(sha1, filename)
        if entry.sha1_known():
            entry.set_attributes(old_IDs, old_families, new_IDs)
            new_IDs.add(entry.ID())
            
            # Enable new, again and update mode if such a track is present
            if entry.new == "N":
                distribution.new = True
                distribution.rewrite(distribution.find("@ENABLE-NEW"), "@ENABLE-NEW\t= 1")
            if entry.again == "A":
                distribution.again = True
                distribution.rewrite(distribution.find("@ENABLE-AGAIN"), "@ENABLE-AGAIN\t= 1")
            if entry.filler == "F":
                distribution.filler = True
                distribution.rewrite(distribution.find("@ENABLE-FILL"), "@ENABLE-FILL\t= 1")
            if entry.update == "U":
                distribution.update = True
                distribution.rewrite(distribution.find("@ENABLE-UPDATE"), "@ENABLE-UPDATE\t= 1")
            
            print(f"{file.filename: <30} is {entry.information()}.")
            file.delete()
        else:
            print(f"{file.filename: <30} is unknown.")
            file.move(os.path.join(cwd, "Output", file.filename))
        distribution.rewrite(begin + x, str(entry))

# Clean repository
print("Cleaning repository...")
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
