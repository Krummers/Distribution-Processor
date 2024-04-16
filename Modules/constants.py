contacts = ["archive", "email", "platforms", "wiiki", "wiimmfi"]
ordered_contacts = ["archive", "wiimmfi", "wiiki", "platforms", "email"]

modes = ["Mario Kart Wii", "Pulsar"]

binaries = ["yes", "y", "no", "n"]

regions = {"JAP", "KOR", "PAL", "USA"}

fcups = {"beginner_course": "1.1", "farm_course": "1.2", \
        "kinoko_course": "1.3", "factory_course": "1.4", \
        "castle_course": "2.1", "shopping_course": "2.2", \
        "boardcross_course": "2.3", "truck_course": "2.4", \
        "senior_course": "3.1", "water_course": "3.2", \
        "treehouse_course": "3.3", "volcano_course": "3.4", \
        "desert_course": "4.1", "ridgehighway_course": "4.2", \
        "koopa_course": "4.3", "rainbow_course": "4.4", \
        "old_peach_gc": "5.1", "old_falls_ds": "5.2", \
        "old_obake_sfc": "5.3", "old_mario_64": "5.4", \
        "old_sherbet_64": "6.1", "old_heyho_gba": "6.2", \
        "old_town_ds": "6.3", "old_waluigi_gc": "6.4", \
        "old_desert_ds": "7.1", "old_koopa_gba": "7.2", \
        "old_donkey_64": "7.3", "old_mario_gc": "7.4", \
        "old_mario_sfc": "8.1", "old_garden_ds": "8.2", \
        "old_donkey_gc": "8.3", "old_koopa_64": "8.4", \
        "block_battle": "A1.1", "venice_battle": "A1.2", \
        "skate_battle": "A1.3", "casino_battle": "A1.4", \
        "sand_battle": "A1.5", "old_battle4_sfc": "A2.1", \
        "old_battle3_gba": "A2.2", "old_matenro_64": "A2.3", \
        "old_cookieland_gc": "A2.4", "old_house_ds": "A2.5"}

cfilenames = {value:key for key, value in fcups.items()}

filenames = set(fcups.keys())

slots = {"1.1": 8, "1.2": 1, "1.3": 2, "1.4": 4, \
         "2.1": 0, "2.2": 5, "2.3": 6, "2.4": 7, \
         "3.1": 9, "3.2": 15, "3.3": 11, "3.4": 3, \
         "4.1": 14, "4.2": 10, "4.3": 12, "4.4": 13, \
         "5.1": 16, "5.2": 20, "5.3": 25, "5.4": 26, \
         "6.1": 27, "6.2": 31, "6.3": 23, "6.4": 18, \
         "7.1": 21, "7.2": 30, "7.3": 29, "7.4": 17, \
         "8.1": 24, "8.2": 22, "8.3": 19, "8.4": 28, \
         "A1.1": 33, "A1.2": 32, "A1.3": 35, "A1.4": 34, "A1.5": 36, \
         "A2.1": 39, "A2.2": 40, "A2.3": 41, "A2.4": 37, "A2.5": 38, \
         "---": "---", "None": "---", "0.0": -1}

tracklist = {slot:slot for _, slot in fcups.items()}
