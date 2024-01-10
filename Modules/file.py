import os
import pickle as pk
import shutil as sh
import subprocess as sp

cwd = os.getcwd()

class File(object):
    
    def __init__(self, path):
        self.path = path
        self.folder = os.path.dirname(path)
        self.filename = os.path.basename(path)
    
    def __repr__(self):
        return self.path
    
    def rename(self, filename):
        new_path = os.path.join(self.folder, filename)
        os.rename(self.path, new_path)
        self.__init__(new_path)
    
    def move(self, path):
        if self.filename != os.path.basename(path):
            raise ValueError("filename must match its previous one")
        os.rename(self.path, path)
        self.__init__(path)
    
    def move_down(self, folders, create_folders = True):
        if not isinstance(folders, list):
            raise TypeError("folder names can only be in a list")
        new_folder = self.folder
        for folder in folders:
            new_folder = os.path.join(new_folder, folder)
        if not os.path.exists(new_folder) and not create_folders:
            raise FileNotFoundError("directory does not exist")
        if not os.path.exists(new_folder):
            os.makedirs(new_folder)
        new_path = os.path.join(new_folder, self.filename)
        os.rename(self.path, new_path)
        self.__init__(new_path)
    
    def move_up(self, amount):
        if not isinstance(amount, int):
            raise TypeError("'amount' must be an integer")
        for x in range(amount):
            self.move(os.path.join(os.path.dirname(self.folder), self.filename))
    
    def exists(self):
        return os.path.exists(self.path)
    
    def delete(self):
        os.remove(self.path)

class Folder(File):
    
    def delete(self):
        sh.rmtree(self.path)
    
    def empty(self):
        self.delete()
        os.mkdir(self.path)

class TXT(File):
    
    def read(self):
        with open(self.path, "r", encoding = "utf-8") as file:
            lines = file.readlines()
        for x in range(len(lines) - 1):
            lines[x] = lines[x][:-1]
        return lines

    def write(self, lines):
        with open(self.path, "w", encoding = "utf-8") as file:
            file.writelines("\n".join(lines))

    def rewrite(self, index, line):
        lines = self.read()
        lines[index - 1] = line
        self.write(lines)
    
    def find(self, string):
        lines = self.read()
        for x in range(len(lines)):
            if lines[x].startswith(string):
                return x + 1
    
    def remove(self, begin, end):
        lines = self.read()
        for x in range(begin - 1, end):
            lines.pop(begin - 1)
        self.write(lines)
    
    def add_to_line(self, index, addition):
        lines = self.read()
        lines[index - 1] += addition
        self.write(lines)

class CFG(File):
    
    def __init__(self, path):
        if not path.endswith("cfg"):
            raise ValueError("not a cfg file")
        self.path = path
        self.folder = os.path.dirname(path)
        self.filename = os.path.basename(path)
        self.name = self.filename[:-4]
        self.create()
    
    def __str__(self):
        return self.name + " - " + str(self.get_value())
    
    def __repr__(self):
        return f"{self.name} (self.get_value())"
    
    def file_exists(self):
        return True if os.path.exists(self.path) else False
    
    def exists(self):
        return False if self.get_value() is None else True
    
    def create(self):
        if not os.path.exists(self.folder):
            os.makedirs(self.folder)
        if not self.file_exists():
            file = open(self.path, "x")
            file.close()
            self.set_value(None)
    
    def set_value(self, value):
        with open(self.path, "wb") as file:
            pk.dump(value, file)
    
    def get_value(self):
        if not self.file_exists():
            return None
        with open(self.path, "rb") as setting:
            return pk.load(setting)

class REL(File):
    
    def tracklist(self):
        output = sp.run(f"wstrt tracks \"{self.path}\" --no-header", \
                        capture_output = True).stdout
        tracks = str(output).split("\\n")[2:-2]
        tracks = [line.split() for line in tracks]
        output = sp.run(f"wstrt arenas \"{self.path}\" --no-header", \
                        capture_output = True).stdout
        arenas = str(output).split("\\n")[2:-2]
        arenas = [line.split() for line in arenas]
        tracklist = {}
        tracklist |= {tracks[x][2]:tracks[x][1] for x in range(len(tracks))}
        tracklist |= {"A" + arenas[x][2]:"A" + arenas[x][1] for x in range(len(arenas))}
        return tracklist
    
    def __eq__(self, other):
        if not isinstance(other, REL):
            raise TypeError("'other' must be a 'REL' object")
        return self.tracklist() == other.tracklist()
    
    def __neq__(self, other):
        if not isinstance(other, REL):
            raise TypeError("'other' must be a 'REL' object")
        return self.tracklist() != other.tracklist()

class CHC(CFG):
    
    def __init__(self, path):
        if not path.endswith("chc"):
            raise ValueError("not a chc file")
        self.path = path
        self.folder = os.path.dirname(path)
        self.filename = os.path.basename(path)
        self.name = self.filename[:-4]
        self.create()

class CNT(CFG):
    
    def __init__(self, path):
        if not path.endswith("cnt"):
            raise ValueError("not a cnt file")
        self.path = path
        self.folder = os.path.dirname(path)
        self.filename = os.path.basename(path)
        self.name = self.filename[:-4]
        self.create()
