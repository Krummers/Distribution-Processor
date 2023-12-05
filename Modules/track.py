from bs4 import BeautifulSoup as bs
import os

import Modules.constants as cs
import Modules.file as fl
import Modules.functions as ft

cwd = os.getcwd()

class Track(object):
    
    def __init__(self, sha1, cup, filename = None):
        self.sha1 = sha1
        self.slot = cs.slots[cup]
        self.cup = cup
        self.filename = filename
        self.information = Track.sha1_information(sha1)
        self.track = "A" not in cup
        self.boost = 0
        self.new = 0
        self.again = 0
        self.update = 0
        self.fill = 0
        self.multiplayer = False
        self.title = False
        self.hidden = False
        self.original = True
    
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
        string += "\t\t" + (str(self.information) if self.information is not None else self.filename)
        return string
    
    def __repr__(self):
        return str(self.information)
    
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
