import dotenv as de
import os
import script_utilities.file as fl
import script_utilities.functions as ft
import time as tm
import wiiki_editor.parser as ps
import wiiki_editor.wiiki as wk

import folders as fd

archive_folder = fd.get_folder("Archive")

def select_distribution() -> str:
    files = os.listdir(archive_folder.path)
    distributions = list(set(map(lambda filename:filename[:-4], files)))
    filename = ft.options_question(distributions) + ".txt"
    return fl.TXT(os.path.join(archive_folder.path, filename))

def get_distribution_information(filename: str) -> dict[str, str]:
    pkl = fl.PKL(os.path.join(archive_folder.path, filename[:-3] + "pkl"))
    return pkl.get_value()

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
        distribution_section = ps.DistributionSection(text)
        entry = ps.DistributionSection.Entry(distribution, version)
        
        skip_line = False
        for x in range(len(distribution_section)):
            if entry.name == distribution_section.entries[x].name:
                if distribution_section.entries[x].dis_id:
                    # Skip the edit if the entry is a Distrib-ref template
                    print(f"Template:Distrib-ref present for {article.title}.")
                    skip_line = True
                
                if entry.version == distribution_section.entries[x].version:
                    # Skip the edit if the entry is identical
                    print(f"Entry would not change the distribution section for {article.title}.")
                    skip_line = True
                
                distribution_section.entries[x] = entry
                break
        else:
            distribution_section += entry
        
        if skip_line:
            continue
        
        summary = f"Added {distribution}."
        print(f"Edited {article.title}: {summary}")
        article.edit_text(str(distribution_section), summary, "Distributions")
        tm.sleep(5)

def main() -> None:
    tracklist = select_distribution()
    distribution_information = get_distribution_information(tracklist.filename)
    distribution = distribution_information["name"]
    wiiki = setup_wiiki()
    edit_articles(wiiki, tracklist, distribution)

if __name__ == "__main__":
    main()
