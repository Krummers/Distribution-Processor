import os
import requests as rq
from bs4 import BeautifulSoup as bs

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
        
def sha1_info(sha1):
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
        pos = s.find("[")
        
        return s[0:pos - 1]
        
    except:
        if os.path.exists(txt):
            os.remove(txt)
        return False