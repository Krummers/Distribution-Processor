import json as js
import os
import pathvalidate as pv
import script_utilities.file as fl
import script_utilities.functions as ft
import subprocess as sp

import folders as fd

archive_folder = fd.get_folder("Archive")
input_folder = fd.get_folder("Input")
output_folder = fd.get_folder("Output")

def collect_information() -> dict[str, str]:
    name = str(input("Enter the name of the distribution: "))
    version = str(input("Enter the version of the distribution: "))
    author = str(input("Enter the author(s) of the distribution: "))
    
    filename = f"{name} {version}.txt"
    
    while True:
        try:
            pv.validate_filename(filename)
        except pv.ValidationError:
            print(f"The name '{filename}' is not valid as a filename.")
            filename = str(input("Enter the filename for the track listing: "))
            filename += ".txt"
        else:
            break
    
    distribution_information = dict()
    distribution_information["name"] = name
    distribution_information["version"] = version
    distribution_information["author"] = author
    distribution_information["filename"] = filename
    return distribution_information

def compress_files() -> None:
    os.chdir(input_folder.path)
    sp.run(["wszst", "compress", "--szs", "--norm", "*.szs", "-o"])
    os.chdir(input_folder.folder)

def download_szslibrary(sha1: str, filename: str) -> None:
    url = f"https://szslibrary.com/api/api.php?sha1={sha1}"
    json = fl.File(os.path.join(output_folder.path, filename))
    
    try:
        ft.download(url, json.path)
    except TimeoutError:
        pass

def get_information(path: str) -> dict[str, bool | str]:
    try:
        with open(path, "r", encoding = "utf-8") as file:
            data = js.load(file)
    except js.JSONDecodeError:
        return dict()
    
    information = dict()
    
    information["is_track"] = bool(data["track_info"]["track_customtrack"])
    information["is_nintendo"] = bool(data["track_info"]["track_nintendo"])
    information["is_texture"] = bool(data["track_info"]["track_texturehack"])
    information["is_edit"] = bool(data["track_info"]["track_change"])
    
    information["curid"] = data["track_info"]["track_wiki"]
    prefix = data["track_info"]["prefix"]
    information["prefix"] = prefix if prefix else ""
    information["name"] = data["track_info"]["trackname"]
    information["author"] = data["track_info"]["track_author"]
    editor = data["track_info"]["track_editor"]
    information["editor"] = editor if editor else ""
    information["family"] = data["track_info"]["track_family"]
    version = data["track_info"]["track_version"]
    version_extra = data["track_info"]["track_version_extra"]
    
    if version_extra == "":
        version_extra = None
    
    if version_extra is not None:
        version += f"-{version_extra}"
    
    information["version"] = version
    
    information["sha1"] = data["track_info"]["track_sha1"]
    information["date"] = data["track_info"]["track_created"]
    speed = data["track_info"]["track_speed"]
    information["speed"] = float(speed) if speed else 1.0
    laps = data["track_info"]["track_laps"]
    information["laps"] = int(laps) if laps else 3
    
    return information

def create_track_list(mode: str) -> None:
    tracklist = fl.TXT(os.path.join(output_folder.path, "tracklist.txt"))
    
    ordered_files = list(map(lambda x:x[0],
                             sorted(map(lambda file:(file, int(file[:-4])),
                                        os.listdir(input_folder.path)),
                                    key = lambda x:x[1])))
    
    for file in ordered_files:
        file = fl.File(os.path.join(input_folder.path, file))
        
        track = int(file.filename[:-4])
        # 4 tracks per cup | Pulsar starts 8 cups ahead | Cup 0 does not exist
        cup = track // 4 + 8 + 1
        # 4 tracks per cup | Track 0 does not exist
        slot = track % 4 + 1
        # file.rename(f"{cup}.{slot}.szs")
        result = sp.check_output(["wszst", "sha1", f"Input/{file.filename}"])
        sha1 = result.split()[0].decode()
        
        json = fl.File(os.path.join(output_folder.path, f"{track}.json"))
        download_szslibrary(sha1, json.path)
        information = get_information(json.path)
        
        if not information:
            print(f"Track with SHA1 {sha1} is unknown.")
            tracklist.append(sha1)
            file.move(os.path.join(output_folder.path, file.filename))
            json.delete()
            continue
        
        prefix = information["prefix"]
        name = information["name"]
        name = f"{prefix} {name}" if prefix else name
        author = information["author"]
        version = information["version"]
        curid = information["curid"]
        
        print(f"Track with SHA1 {sha1} is {name} ({author}) {version}.")
        tracklist.append(f"{name}|{author}|{version}|{curid}")
    
    return tracklist

def store_information(tracklist: fl.File, distribution_information: dict[str, str]) -> None:
    filename = distribution_information["filename"]
    tracklist.move(os.path.join(archive_folder.path, tracklist.filename))
    tracklist.rename(filename)
    
    del distribution_information["filename"]
    pkl = fl.PKL(os.path.join(archive_folder.path, filename[:-3] + "pkl"))
    pkl.set_value(distribution_information)

def main() -> None:
    distribution_information = collect_information()
    compress = ft.question("Compress the files?")
    
    if compress:
        compress_files()
    
    tracklist = create_track_list("Pulsar") # ct engine mode is currently Pulsar by default
    store_information(tracklist, distribution_information)

if __name__ == "__main__":
    main()
