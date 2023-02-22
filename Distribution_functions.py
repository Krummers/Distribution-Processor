import os
import requests as rq
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
             "old_CookieLand_gc", "old_House_ds"}

yn = ["yes", "y", "no", "n"]

def download_data(link, location):
    data = rq.get(link)
    
    with open(location, "wb") as k:
        k.write(data.content)

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
        return False