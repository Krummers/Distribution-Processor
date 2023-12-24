import Modules.file as fl
import Modules.track as tr

class Distribution(object):
    
    def __init__(self, filename):
        information = fl.TXT(filename).read()
        
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
        self.fill = bool(int(Distribution.find_information("@ENABLE-FILL", information)))
        self.update = bool(int(Distribution.find_information("@ENABLE-UPDATE", information)))
        self.boost = bool(int(Distribution.find_information("@ENABLE-BOOST", information)))
        self.uuid = Distribution.find_information("@UUID", information)
        
        definition = information[191 - 1:]
        self.tracks = []
        
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
    
    def sort_tracks(self):
        self.tracks = sorted(self.tracks, key = lambda track:track.cup)
        return self.tracks
    
    def find_information(variable, information):
        for line in information:
            if line.startswith(variable):
                line = line.split("= ")
                return line[-1]