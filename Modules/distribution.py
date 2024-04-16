import os

import Modules.entry as et
import Modules.file as fl
import Modules.track as tr

cwd = os.getcwd()
contacts = fl.Folder(os.path.join(cwd, "Contacts"))

class Distribution(object):
    
    def __init__(self, filename, load_tracks = True):
        information = fl.TXT(filename).read()
        
        self.file = fl.TXT(filename)
        
        self.name = Distribution.find_information("@NAME", information)
        self.version = Distribution.find_information("@VERSION", information)
        self.author = Distribution.find_information("@AUTHOR", information)
        self.release = Distribution.find_information("@RELEASE-DATE", information)
        self.tag = Distribution.find_information("@REFERENCE-NAME", information)
        self.keywords = Distribution.find_information("@KEYWORDS", information)
        self.predecessor = Distribution.find_information("@PREDECESSOR", information)
        self.wiimmfi = Distribution.find_information("@WIIMMFI-REGION", information)
        self.text = Distribution.find_information("@INFO-TEXT", information)
        self.url = Distribution.find_information("@INFO-URL", information)
        self.display = int(Distribution.find_information("@DISPLAY-MODE", information))
        self.database = bool(int(Distribution.find_information("@DATABASE-NAME", information)))
        self.comment = bool(int(Distribution.find_information("@VIEW-COMMENT", information)))
        self.new = bool(int(Distribution.find_information("@ENABLE-NEW", information)))
        self.again = bool(int(Distribution.find_information("@ENABLE-AGAIN", information)))
        self.filler = bool(int(Distribution.find_information("@ENABLE-FILL", information)))
        self.update = bool(int(Distribution.find_information("@ENABLE-UPDATE", information)))
        self.boost = bool(int(Distribution.find_information("@ENABLE-BOOST", information)))
        self.uuid = Distribution.find_information("@UUID", information)
        self.wszst_version = Distribution.find_information("@WSZST-VERSION", information)
        self.wszst_revision = Distribution.find_information("@WSZST-REVISION", information)
        self.first_creation = Distribution.find_information("@FIRST-CREATION", information)
        self.last_update = Distribution.find_information("@LAST-UPDATE", information)
        
        self.tracks = []
        if load_tracks:
            self.load_tracks()
    
    def __repr__(self):
        return f"{self.name} {self.version} ({self.author})"
    
    def __contains__(self, ID):
        for track in self.tracks:
            if track.ID == ID:
                return True
    
    def check_again(self):
        for x in range(len(self.tracks)):
            for y in range(x + 1, len(self.tracks)):
                if self.tracks[x].ID is None or self.tracks[y].ID is None:
                    continue
                if self.tracks[x].ID == self.tracks[y].ID:
                    self.tracks[y].again = True
                    self.again = True
    
    def check_update(self, predecessor):
        if not isinstance(predecessor, Distribution):
            raise TypeError("predecessor must be a 'Distribution' object")
        for x in range(len(self.tracks)):
            for y in range(len(predecessor.tracks)):
                track = self.tracks[x]
                course = predecessor.tracks[y]
                if track.family == course.family and track.ID != course.ID:
                    self.tracks[x].update = True
                    self.update = True
    
    def check_new(self, predecessor):
        if not isinstance(predecessor, Distribution):
            raise TypeError("predecessor must be a 'Distribution' object")
        for x in range(len(self.tracks)):
            if self.tracks[x].ID is None:
                continue
            if self.tracks[x].ID not in predecessor and not self.tracks[x].update:
                self.tracks[x].new = True
                self.new = True
    
    def compare(self, predecessor):
        if not isinstance(predecessor, Distribution):
            raise TypeError("predecessor must be a 'Distribution' object")
        self.check_again()
        self.check_update(predecessor)
        self.check_new(predecessor)
    
    def __str__(self):
        clean = fl.TXT(os.path.join(cwd, "Modules", "clean.txt")).read()
        
        string = ""
        string += "\n".join(clean[:28]) + "\n"
        string += f"@NAME\t\t= {self.name}\n"
        string += f"@VERSION\t= {self.version}\n"
        string += f"@AUTHORS\t= {self.author}\n"
        string += "\n".join(clean[31:33]) + "\n"
        string += f"@RELEASE-DATE\t= {self.release}\n"
        string += "\n".join(clean[34:37]) + "\n"
        string += f"@KEYWORDS\t= {self.keywords}\n"
        string += "\n".join(clean[38:40]) + "\n"
        string += f"@PREDECESSOR\t= {self.predecessor}\n"
        string += "\n".join(clean[41:43]) + "\n"
        string += f"@WIIMMFI-REGION\t= {self.wiimmfi}\n"
        string += f"@INFO-TEXT\t= {self.text}\n"
        string += f"@INFO-URL\t= {self.url}\n"
        string += "\n".join(clean[46:58]) + "\n"
        string += f"@DISPLAY-MODE\t= {self.display}\n"
        string += "\n".join(clean[59:64]) + "\n"
        string += f"@DATABASE-NAME\t= {int(self.database)}\n"
        string += "\n".join(clean[65:70]) + "\n"
        string += f"@VIEW-COMMENT\t= {int(self.comment)}\n"
        string += "\n".join(clean[71:78]) + "\n"
        string += f"@ENABLE-NEW\t= {int(self.new)}\n"
        string += f"@ENABLE-AGAIN\t= {int(self.again)}\n"
        string += f"@ENABLE-FILL\t= {int(self.filler)}\n"
        string += f"@ENABLE-UPDATE\t= {int(self.update)}\n"
        string += "\n".join(clean[82:87]) + "\n"
        string += f"@ENABLE-BOOST\t= {int(self.boost)}\n"
        string += "\n".join(clean[88:111]) + "\n"
        archive = fl.CNT(os.path.join("Contacts", "archive.cnt")).get_value()
        string += f"@USER-CT-WIIMM\t= {archive}\n"
        string += "\n".join(clean[112:114]) + "\n"
        wiimmfi = fl.CNT(os.path.join("Contacts", "wiimmfi.cnt")).get_value()
        string += f"@USER-WIIMMFI\t= {wiimmfi}\n"
        string += "\n".join(clean[115:117]) + "\n"
        wiiki = fl.CNT(os.path.join("Contacts", "wiiki.cnt")).get_value()
        string += f"@USER-CT-WIIKI\t= {wiiki}\n"
        string += "\n".join(clean[118:120]) + "\n"
        platforms = fl.CNT(os.path.join("Contacts", "platforms.cnt")).get_value()
        string += f"@USER-MISC\t= {platforms}\n"
        string += "\n".join(clean[121:123]) + "\n"
        email = fl.CNT(os.path.join("Contacts", "email.cnt")).get_value()
        string += f"@MAIL\t\t= {email}\n"
        string += "\n".join(clean[124:135]) + "\n"
        string += f"@UUID\t\t= {self.uuid}\n"
        string += "\n".join(clean[136:138]) + "\n"
        string += f"@WSZST-VERSION\t= {self.wszst_version}\n"
        string += f"@WSZST-REVISION\t= {self.wszst_revision}\n"
        string += "\n".join(clean[140:142]) + "\n"
        string += f"@FIRST-CREATION\t= {self.first_creation}\n"
        string += f"@LAST-UPDATE\t= {self.last_update}\n"
        string += "\n".join(clean[144:186])
        for x in range(len(self.tracks)):
            if x != 0 and self.tracks[x].cup.cup > self.tracks[x - 1].cup.cup:
                string += "\n"
            string += str(self.tracks[x]) + "\n"
        return string
    
    def sort_tracks(self):
        self.tracks = sorted(self.tracks, key = lambda track:track.cup)
        return self.tracks
    
    def load_tracks(self):
        self.tracks = []
        information = self.file.read()
        begin = self.file.find("# for racing tracks")
        definition = information[begin + 2:]
        
        for x in range(len(definition)):
            if definition[x] != "\n" and definition[x] != "":
                line = definition[x].split(maxsplit = 6)
                track = line[0]
                flags = line[1]
                lecode = line[2]
                sha1 = line[3]
                slot = line[4]
                cup = line[5]
                information = line[6]
                track = tr.Track(sha1, cup, flags, lecode, slot, information)
                self.tracks.append(track)
    
    def families_IDs(self):
        families = set()
        IDs = set()
        information = self.file.read()
        begin = self.file.find("# for racing tracks")
        definition = information[begin + 2:]
        
        for entry in definition:
            if entry == "\n" or entry == "":
                continue
            entry = entry.split()
            sha1 = entry[3]
            slot = entry[5]
            entry = et.Entry(sha1, slot)
            if entry.sha1_known():
                print(f"Loaded {entry.information()}.")
                families.add(entry.family())
                IDs.add(entry.ID())
        
        return families, IDs
    
    def find_information(variable, information):
        for line in information:
            if line.startswith(variable):
                line = line.split("= ")
                return line[-1]