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
        distribution_section = ps.DistributionSection(text)
        entry = ps.DistributionSection.Entry(distribution, version)
        
        for x in range(len(distribution_section)):
            if entry.name == distribution_section.entries[x].name:
                distribution_section.entries[x] = entry
                break
        else:
            distribution_section += entry
        
        # article.edit_text(str(distribution_section), f"Added {distribution}.", "Distributions")
        print(f"Would edit distribution section of article {article.title} with")
        print(str(distribution_section))
        tm.sleep(5)

def main() -> None:
    tracklist = select_distribution()
    distribution = input("Name distribution on Wiiki: ")
    wiiki = setup_wiiki()
    edit_articles(wiiki, tracklist, distribution)

if __name__ == "__main__":
    main()
