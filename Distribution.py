import Distribution_functions as dis
import os
import subprocess as sp
from bs4 import BeautifulSoup as bs

cwd = os.getcwd()
contact = os.path.join(cwd, "contact.txt")
distribution = os.path.join(cwd, "distribution.txt")

# Defines contact information
if os.path.exists(contact):
    while True:
        contact_option = str(input("Should new contact information be created? (Y or N): ")).lower()
        
        if contact_option in dis.yn:
            if contact_option in dis.yn[0:2]:
                os.remove(contact)
            break
        else:
            print("This is not an option. Please try again.")
else:
    contact_option = "yes"

if contact_option in dis.yn[0:2]:    
    # Defines usernames
    archive_name = str(input("Enter username on Wiimms CT-Archive: "))
    wiimmfi_name = str(input("Enter username on Wiimmfi: "))
    wiiki_name = str(input("Enter username on the Wiiki: "))
    other_names = str(input("Enter other usernames on different platforms in \"service=name\" format, separated by a comma: "))
    mail = str(input("Enter e-mail address: "))
    
    # Creates contact.txt
    f = open(contact, "w")
    f.write("@USER-CT-WIIMM\t= {}\n".format(archive_name))
    f.write("@USER-WIIMMFI\t= {}\n".format(wiimmfi_name))
    f.write("@USER-CT-WIIKI\t= {}\n".format(wiiki_name))
    f.write("@USER-MISC\t= {}\n".format(other_names))
    f.write("@MAIL\t\t= {}\n".format(mail))
    f.close()

# Stores distribution information
dis_name = str(input("Enter the name of the distribution: "))
dis_version = str(input("Enter the version number of {}: ".format(dis_name)))
dis_author = str(input("Enter the author(s) of {}: ".format(dis_name)))
dis_date = str(input("Enter the release date of {}: ".format(dis_name)))
dis_tag = str(input("Enter the distribution tag of {}: ".format(dis_name)))

v = dis.question("Does {} have a predecessor?".format(dis_name))
if v:
    dis_pre = str(input("Enter the UUID of the previous version of {}: ".format(dis_name)))
else:
    dis_pre = ""

v = dis.question("Does {} have a Wiimmfi region?".format(dis_name))
if v:
    dis_region = str(input("Enter the region number of {}: ".format(dis_name)))
else:
    dis_region = ""

dis_url = str(input("Enter the URL of {}: ".format(dis_name)))

# Filters szs files for tracks only and locates StaticR.rel
szs = []
static = None
for file in os.listdir():
    if file.endswith(".szs"):
        szs.append(file)

for track in szs:
    if track[:-4].lower() not in dis.filenames:
        os.remove(track)

# Compresses files and creates distribution.txt
print("Compressing files...")
os.chdir(cwd)
sp.run("wszst compress --szs --norm --rmai *.szs -o")
sp.run("wszst distrib .")
os.chdir(cwd)

# Writes contact information
f = open(contact, "r")
info = f.readlines()
f.close()

print("Writing contact information...")
dis.rewrite_line(distribution, 42, info[0])
dis.rewrite_line(distribution, 45, info[1])
dis.rewrite_line(distribution, 48, info[2])
dis.rewrite_line(distribution, 51, info[3])
dis.rewrite_line(distribution, 54, info[4])

# Writes distribution information
print("Writing distribution information...")
dis.rewrite_line(distribution, 68, "@NAME\t\t= {}\n".format(dis_name))
dis.rewrite_line(distribution, 69, "@VERSION\t= {}\n".format(dis_version))
dis.rewrite_line(distribution, 70, "@AUTHORS\t= {}\n".format(dis_author))
dis.rewrite_line(distribution, 73, "@RELEASE-DATE\t= {}\n".format(dis_date))
dis.rewrite_line(distribution, 77, "@REFERENCE-NAME\t= {}\n".format(dis_tag))

if dis_pre != "":
    dis.rewrite_line(distribution, 84, "@PREDECESSOR\t= {}\n".format(dis_pre))

if dis_region != "":
    dis.rewrite_line(distribution, 87, "@WIIMMFI-REGION\t= {}\n".format(dis_region))

dis.rewrite_line(distribution, 89, "@INFO-URL\t= {}\n".format(dis_url))

# Removes standard SHA1s
f = open(distribution, "r")
info = f.readlines()
f.close()

for k in range(87):
    info.pop(189)

f = open(distribution, "w")
f.writelines(info)
f.close()

# Identifies tracks
for k in range(190, len(info)):
    if info[k] != "\n":
        sha1 = dis.sha1_info(info[k][0:40])
        if sha1 != None:
            dis.rewrite_line(distribution, k + 1, info[k][0:48] + sha1 + "\n")
            print("Track information found: {}".format(sha1))
        else:
            print("Unidentified track!")

# Sorts tracks based on StaticR.rel
if static:
    pass

# Cleanup
name = dis_name + " " + dis_version + ".txt"
os.rename(distribution, os.path.join(cwd, name))

input("All done!")