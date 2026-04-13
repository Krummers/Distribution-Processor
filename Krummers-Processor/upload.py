import dotenv as de
import os
import script_utilities.file as fl
import script_utilities.functions as ft
import time as tm
import wiiki_editor.wiiki as wk

import common as cm
import folders as fd

archive_folder = fd.get_folder("Archive")

def select_distribution() -> str:
    distributions = os.listdir(archive_folder.path)
    filename = ft.options_question(distributions)
    return fl.TXT(os.path.join(archive_folder.path, filename))

def setup_wiiki() -> wk.Wiiki:
    cwd = os.getcwd()
    secret_path = os.path.join(cwd, ".env")
    secrets = dict(de.dotenv_values(secret_path))
        
    return wk.Wiiki(secrets["USERNAME"], secrets["PASSWORD"], secrets["API"])

def edit_articles(wiiki: wk.Wiiki, tracklist: fl.TXT, distribution: str) -> None:
    tracks = tracklist.read()
    for line in tracks:
        arguments = line.split("|")
        if len(arguments) != 4:
            continue
        name, author, version, curid = arguments
        curid = int(curid.strip()) #handle edge case that will be fixed later
        
        article = wiiki.article(curid)
        text = article.get_text("Distributions")
        body = text[:text.find("distribution]]s:\n") + 17]
        ctd = cm.CustomTrackDistributions(text)
        entry = cm.CustomTrackDistributions.Line(distribution, version, None, None)
        
        for x in range(len(ctd.distributions)):
            if entry.name == ctd.distributions[x].name:
                ctd.distributions[x] = entry
                break
        else:
            ctd.distributions.append(entry)
        
        ctd.sort_by_name()
        new_text = body + str(ctd)
        section_index = article.get_sections().index("Distributions")
        article.edit_text(new_text, f"Added {distribution}.", section_index)
        print(f"Would edit distribution section of article {article.title} with")
        print(new_text)
        tm.sleep(5)

def main() -> None:
    tracklist = select_distribution()
    distribution = input("Name distribution on Wiiki: ")
    wiiki = setup_wiiki()
    edit_articles(wiiki, tracklist, distribution)

if __name__ == "__main__":
    main()
