import os
import requests as rq
import subprocess as sp
from bs4 import BeautifulSoup as bs

filenames = {"beginner_course", "farm_course", \
             "kinoko_course", "factory_course", \
             "castle_course", "shopping_course", \
             "boardcross_course", "truck_course", \
             "senior_course", "water_course", \
             "treehouse_course", "volcano_course", \
             "desert_course", "ridgehighway_course", \
             "koopa_course", "rainbow_course", \
             "old_peach_gc", "old_falls_ds", \
             "old_obake_sfc", "old_mario_64", \
             "old_sherbet_64", "old_heyho_gba", \
             "old_town_ds", "old_waluigi_gc", \
             "old_desert_ds", "old_koopa_gba", \
             "old_donkey_64", "old_mario_gc", \
             "old_mario_sfc", "old_garden_ds", \
             "old_donkey_gc", "old_koopa_64", \
             "block_battle", "venice_battle", \
             "skate_battle", "casino_battle", \
             "sand_battle", "old_battle4_sfc", \
             "old_battle3_gba", "old_matenro_64", \
             "old_cookieland_gc", "old_house_ds"}

yn = ["yes", "y", "no", "n"]

def download_data(link, location):
    data = rq.get(link)
    
    with open(location, "wb") as k:
        k.write(data.content)

def track_order(static, mode_type):
    with open("output.txt", "w") as file:
        sp.run("wstrt {} \"{}\"".format(mode_type, static), stdout = file, text = True)
    
    d = {}
    info = read_file("output.txt")
    if mode_type == "tracks":
        end = 45
    if mode_type == "arenas":
        end = 18
    
    for k in range(6, end):
        if info[k][0] == "-":
            continue
        key = Slot(int(info[k][6]), int(info[k][8]), mode_type)
        value = Slot(int(info[k][11]), int(info[k][13]), mode_type)
        d[key] = value
    
    os.remove("output.txt")
    
    return d

def question(string):
    while True:
        option = str(input(string + " (Y or N): "))
        
        if option.lower() in yn[0:2]:
            return True
        elif option.lower() in yn[2:4]:
            return False
        else:
            print("This is not an option. Please try again.")

def read_file(file):
    txt = open(file, "r")
    info = txt.readlines()
    txt.close()
    return info

def read_line(file, index):
    txt = open(file, "r")
    info = txt.readlines()
    txt.close()
    return info[index - 1]

def rewrite_line(file, index, line):
    txt = open(file, "r")
    l = txt.readlines()
    txt.close()
    
    l[index - 1] = line
    
    txt = open(file, "w")
    txt.writelines(l)
    txt.close()
        
def sha1_info(sha1, editors = False, comments = False):
    try:
        txt = os.path.join(os.getcwd(), "check.txt")
        download_data("https://ct.wiimm.de/?s=" + sha1, txt)
        
        f = open("check.txt", "r")
        information = f.readlines()
        f.close()
        
        os.remove(txt)
        
        information = "".join(information)
        information = bs(information, "html.parser")
        
        s = str(information.find_all("td")[17].contents[0])
        
        if comments == False:
            pos = s.find("[")
            s = s[0:pos - 1]
            if editors == False:
                pos = s.find(",,")
                if pos != -1:
                    s = s[:pos] + ")"
        
        return s
        
    except:
        if os.path.exists(txt):
            os.remove(txt)
        return None

class Slot(object):
    
    def __init__(self, cup = 1, track = 1, mode = ""):
        if cup <= 0:
            raise ValueError("Cup 0 or lower does not exist.")
        if not (1 <= track <= 5):
            raise ValueError("Track can only be in between 1 and 5.")
        
        if mode == "tracks" or mode == " ":
            mode = ""
        elif mode == "arenas" or mode == "A":
            mode = "A"
        else:
            raise ValueError("Only tracks, arenas or A are accepted.")
        
        self.cup = cup
        self.track = track
        self.type = mode
    
    def __str__(self):
        return str(self.type) + str(self.cup) + "." + str(self.track)
    
    def __repr__(self):
        return str(self)
    
    def __lt__(self, other):
        if type(other) != Slot:
            raise TypeError("'<' not supported between instances of '{}' and '{}'".format(type(self), type(other)))
        
        if self.cup != other.cup:
            return self.cup < other.cup
        elif self.track != other.track:
            return self.track < other.track
        else:
            return False
    
    def __le__(self, other):
        if type(other) != Slot:
            raise TypeError("'<=' not supported between instances of '{}' and '{}'".format(type(self), type(other)))
        
        if self.cup != other.cup:
            return self.cup <= other.cup
        elif self.track != other.track:
            return self.track <= other.track
        else:
            return True
    
    def __eq__(self, other):
        if type(other) != Slot:
            raise TypeError("'==' not supported between instances of '{}' and '{}'".format(type(self), type(other)))
        
        return (self.cup == other.cup) and (self.track == other.track)
    
    def __gt__(self, other):
        if type(other) != Slot:
            raise TypeError("'>' not supported between instances of '{}' and '{}'".format(type(self), type(other)))
        
        if self.cup != other.cup:
            return self.cup > other.cup
        elif self.track != other.track:
            return self.track > other.track
        else:
            return False
    
    def __ge__(self, other):
        if type(other) != Slot:
            raise TypeError("'>=' not supported between instances of '{}' and '{}'".format(type(self), type(other)))
        
        if self.cup != other.cup:
            return self.cup >= other.cup
        elif self.track != other.track:
            return self.track >= other.track
        else:
            return True
    
    def __ne__(self, other):
        if type(other) != Slot:
            raise TypeError("'==' not supported between instances of '{}' and '{}'".format(type(self), type(other)))
        
        return (self.cup != other.cup) or (self.track != other.track)
    
    def __hash__(self):
        return hash(str(self))

class CustomTrackLine(object):
    
    def __init__(self, sha1, slot, name):
        self.sha1 = sha1
        self.slot = slot
        self.name = name
    
    def __str__(self):
        if self.slot.type == "A":
            sslot = "  " + str(self.slot) + "  "
        else:
            sslot = "   " + str(self.slot) + "  "
        
        return self.sha1 + sslot + self.name
    
    def __repr__(self):
        return self.sha1 + "\n" + str(self.slot) + "\n" + self.name