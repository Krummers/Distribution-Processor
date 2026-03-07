import functools as fc
import json as js
import os

import Modules.constants as cs
import Modules.file as fl
import Modules.functions as ft

cwd = os.getcwd()

class Entry(object):
    
    def __init__(self, sha1, filename):
        self.sha1 = sha1
        self.filename = filename.lower()
        
        # Set known values
        # Define if entry is a track or battle arena
        if self.filename in list(cs.fcups.keys())[-10:]:
            self.vs = "bt"
        else:
            self.vs = "vs"
        
        # Define slot number
        if self.filename in cs.filenames:
            self.slot = cs.slots[cs.fcups[self.filename]]
            self._d = "-"
        elif self.filename.endswith("_d"):
            self.filename = self.filename[:-2]
            if self.filename in cs.filenames:
                self.slot = cs.slots[cs.fcups[self.filename]]
            self._d = "d"
        else:
            # Calculate slot location
            x, y = self.filename.split(".")
            x, y = int(x), int(y)
            self.slot = 256 + 4 * (x - 9) + (y - 1)
            self._d = "-"
        
        # Define cup location
        if self.filename in cs.filenames:
            self.cup = cs.fcups[self.filename]
        else:
            self.cup = self.filename
        
        # Set remaining empty values        
        self.boost = "-"
        self.new = "-"
        self.again = "-"
        self.update = "-"
        self.filler = "-"
        self.title = "-"
        self.hidden = "-"
        self.original = "-"
        self.track_type = "-"
        self.cup_type = "-"
        self.header = "-"
        self.track_classification = "-"
        self.alias = "-"
        self.invisible = "-"
    
    def __str__(self):
        """
        Returns a string formatted as a distribution entry.
        """
        string = ""
        string += self.vs
        string += " "
        string += self.boost
        string += self.new
        string += self.again
        string += self.update
        string += self.filler
        string += self._d
        string += self.title
        string += self.hidden
        string += self.original
        string += " "
        string += self.track_type
        string += self.cup_type
        string += self.header
        string += self.track_classification
        string += self.alias
        string += self.invisible
        string += " "
        string += self.sha1
        string += "\t"
        string += str(self.slot)
        string += "\t\t"
        string += self.cup
        string += "\t\t"
        string += self.information() if self.sha1_known() else ""
        return string
    
    @fc.lru_cache
    def json(self):
        """
        Returns a JSON with track information.
        """
        json = fl.TXT(os.path.join(cwd, "json.json"))
        ft.download(f"https://ct.wiimm.de/api/get-track-info?sha1={self.sha1}", json.path)
        information = js.loads(json.read()[0])
        json.delete()
        if information["http_status"] == 404:
            return None
        else:
            return information
    
    def sha1_known(self):
        """
        Returns a bool that represents if a SHA1 is known on ct.wiimm.de.
        """
        information = self.json()
        return bool(information)
    
    def information(self):
        """
        Returns name, version and author in a formatted string.
        """
        information = self.json()
        prefix = information["split_name"]["prefix"]
        name = information["split_name"]["name"]
        version = information["split_name"]["version"]
        authors = information["split_name"]["authors"]
        extra = information["split_name"]["extra"]
        
        string = f"{prefix} " if prefix is not None else ""
        string += f"{name} {version}"
        string += f" {{{extra}}}" if extra is not None else ""
        string += f" ({authors})"
        return string
    
    def ID(self):
        """
        Returns the ID of the track.
        """
        information = self.json()
        return information["file_id"]
    
    def family(self):
        """
        Returns the family number of the track.
        """
        information = self.json()
        return information["family"]
    
    def set_attributes(self, old_IDs, old_families, new_IDs):
        """
        Sets attributes of an entry in a distribution.
        """
        # Determine if entry is a track or battle arena
        if self.filename in list(cs.fcups.keys())[-10:]:
            self.vs = "bt"
        else:
            self.vs = "vs"
        
        # Collect information
        information = self.json()
        
        # Determine if track is boost or not
        self.boost = "B" if information["class"] == "boost" else "-"
        
        # Determine if track is new or not
        self.new = "N" if self.family() not in old_families else "-"
        
        # Determine if track has appeared before
        self.again = "A" if self.ID() in new_IDs else "-"
        
        # Determine if track has been updated
        self.update = "U" if self.family() in old_families and self.ID() not in old_IDs else "-"
        
        # Determine if track is a filler
        self.filler = "-"
        
        # Determine if track is only a title
        self.title = "-"
        
        # Determine if track is hidden
        self.hidden = "-"
        
        # Determine if track is original or not
        self.original = "o" if information["class"] == "nintendo" else "-"
        
        # LE-CODE parameters (partially unimplemented)
        # Determine if track is marked as battle arena, versus track or random
        self.track_type = "-"
        
        # Determine if track is used in original cup, custom cup or both
        self.cup_type = "-"
        
        # Determine if track is marked as group header, group member or both
        self.header = "-"
        
        # Determine if track is marked as new, texture hack or both
        self.track_classification = "-"
        
        # Determine if track is marked as alias for other track
        self.alias = "-"
        
        # Determine if track is marked as invisible
        self.invisible = "-"
        
        # Define slot number
        if self.filename in cs.filenames:
            self.slot = cs.slots[cs.fcups[self.filename]]
        else:
            # Calculate slot location
            x, y = self.filename.split(".")
            x, y = int(x), int(y)
            self.slot = 256 + 4 * (x - 9) + (y - 1)
        
        # Define cup location
        if self.filename in cs.filenames:
            self.cup = cs.fcups[self.filename]
        else:
            self.cup = self.filename
