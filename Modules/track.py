from bs4 import BeautifulSoup as bs
import os

import Modules.constants as cs
import Modules.file as fl
import Modules.functions as ft

cwd = os.getcwd()

class Track(object):
    
    def __init__(self, sha1, cup, flags = "---------", lecode = "------", \
                 slot = None, information = None, filename = None):
        self.sha1 = sha1
        try:
            self.slot = cs.slots[cup]
        except:
            self.slot = "---"
        self.cup = Slot(cup)
        self.filename = filename
        self.information = information
        self.track = "A" not in cup
        self.boost = False
        self.new = False
        self.again = False
        self.update = False
        self.fill = False
        self.multiplayer = False
        self.title = False
        self.hidden = False
        self.original = False
        self.ID = None
        self.family = None
        
        self.set_information()
        self.set_flag(flags)
    
    def __str__(self):
        string = ""
        string += "vs" if self.track else "bt"
        string += " "
        string += "B" if self.boost else "-"
        string += "N" if self.new else "-"
        string += "A" if self.again else "-"
        string += "U" if self.update else "-"
        string += "F" if self.fill else "-"
        string += "d" if self.multiplayer else "-"
        string += "t" if self.title else "-"
        string += "h" if self.hidden else "-"
        string += "o" if self.original else "-"
        string += " "
        string += "-o----" # LE_FLAGS are ignored for now
        string += " "
        string += str(self.sha1)
        string += "\t" + str(self.slot)
        string += "\t" + str(self.cup)
        string += "\t\t" + (str(self.information) if self.information is not None else str(self.filename))
        return string
    
    def __repr__(self):
        return str(self.information)
    
    def set_cup(self, cup):
        self.slot = cs.slots[cup]
        self.cup = Slot(cup)
        self.track = "A" not in cup
    
    def set_information(self):
        check = fl.TXT(os.path.join(cwd, "check.txt"))
        ft.download(f"https://ct.wiimm.de/?s={self.sha1}", check.path)
        html = check.read()
        check.delete()
        try:
            html = bs("".join(html), "html.parser")
            information = str(html.find_all("td")[17].contents[0])
            information = information[:information.find("[") - 1]
            information = information[:information.find(",,")] + ")"
            if self.information is None:
                self.information = information
        except:
            self.information = None
        try:
            self.family = str(html.find_all("td")[11].contents[0])
        except:
            self.family = None
        try:
            self.ID = str(html.find_all("td")[10].contents[0])
        except:
            self.ID = None
    
    def set_flag(self, flags):
        flag = [indicator for indicator in flags]
        self.boost = True if flag[0] == "B" else False
        self.new = True if flag[1] == "N" else False
        self.again = True if flag[2] == "A" else False
        self.update = True if flag[3] == "U" else False
        self.fill = True if flag[4] == "F" else False
        self.multiplayer = True if flag[5] == "d" else False
        self.title = True if flag[6] == "t" else False
        self.hidden = True if flag[7] == "h" else False
        self.original = True if flag[8] == "o" else False
    
    def set_lecode(self, lecode):
        pass
    
    def family(self):
        check = fl.TXT(os.path.join(cwd, "check.txt"))
        ft.download(f"https://ct.wiimm.de/?s={self.sha1}", check.path)
        html = check.read()
        check.delete()
        try:
            html = bs("".join(html), "html.parser")
            family = str(html.find_all("td")[11].contents[0].contents[0])
            return family
        except:
            return
    
    def ID(self):
        check = fl.TXT(os.path.join(cwd, "check.txt"))
        ft.download(f"https://ct.wiimm.de/?s={self.sha1}", check.path)
        html = check.read()
        check.delete()
        try:
            html = bs("".join(html), "html.parser")
            ID = str(html.find_all("td")[10].contents[0])
            return ID
        except:
            return
    
    def sha1_information(sha1, editors = False, comments = False):
        check = fl.TXT(os.path.join(cwd, "check.txt"))
        ft.download(f"https://ct.wiimm.de/?s={sha1}", check.path)
        html = check.read()
        check.delete()
        try:
            html = bs("".join(html), "html.parser")
            information = str(html.find_all("td")[17].contents[0])
            
            if not comments:
                information = information[:information.find("[") - 1]
            
            if not editors and ",," in information:
                information = information[:information.find(",,")] + ")"
            
            return information
        except:
            return None

class Slot(object):
    
    def __init__(self, cup):
        if cup == "---" or cup == "None":
            self.cup = 0
            self.slot = 0
            self.arena = False
            return
        information = cup.split(".")
        self.cup = int(information[0]) if "A" not in information[0] else int(information[0][1:])
        self.slot = int(information[1])
        self.arena = "A" in information[0]
    
    def __str__(self):
        string = ""
        string += "A" if self.arena else ""
        string += str(self.cup)
        string += "."
        string += str(self.slot)
        return string
    
    def __repr__(self):
        return str(self)
    
    def __lt__(self, other):
        if not isinstance(other, Slot):
            raise TypeError("'other' must be a Slot object")
        if self.arena and not other.arena:
            return True
        elif not self.arena and other.arena:
            return False
        elif self.cup < other.cup:
            return True
        elif self.cup > other.cup:
            return False
        elif self.slot < other.slot:
            return True
        else:
            return False
    
    def __le__(self, other):
        if not isinstance(other, Slot):
            raise TypeError("'other' must be a Slot object")
        return self < other or self == other
    
    def __eq__(self, other):
        if not isinstance(other, Slot):
            raise TypeError("'other' must be a Slot object")
        return self.cup == other.cup and self.slot == other.slot and self.arena == other.arena
    
    def __ne__(self, other):
        if not isinstance(other, Slot):
            raise TypeError("'other' must be a Slot object")
        return self.cup != other.cup or self.slot != other.slot or self.arena != other.arena
    
    def __ge__(self, other):
        if not isinstance(other, Slot):
            raise TypeError("'other' must be a Slot object")
        return self > other or self == other
    
    def __gt__(self, other):
        if not isinstance(other, Slot):
            raise TypeError("'other' must be a Slot object")
        if not self.arena and other.arena:
            return True
        elif self.arena and not other.arena:
            return False
        elif self.cup > other.cup:
            return True
        elif self.cup < other.cup:
            return False
        elif self.slot > other.slot:
            return True
        else:
            return False
