#Python Main optmize

from constants import all_stats, artifact_slots, Base_Multiplier
from artifacts import all_sets
from weapons import swords as weapons
from characters import Kaeya
from Build import Build
from fit_functions import generic_dmg_function
import json
import time

weapons = {name:{"Name":name, "Lv":90, **weapon} for (name,weapon) in weapons.items()}

characters = {"Kaeya": Kaeya}

constraints = {
    "EM": {"minimum":None, "maximum": None},
    "ER": {"minimum":100, "maximum": None}
}

all_stats = {k:0.0 for k in all_stats}

def my_fit_function(sheet):
    return (1.09 * (1+burst_dmg/100.0)) * generic_dmg_function(sheet, dmg_type="CRYO_DMG")

##### Generate All builds and optmize them
builds = {}
start_time = time.time()
for (char_name,char_data) in characters.items():
    char_data = {**all_stats, **char_data} 
    for (weapon_name,weapon_data) in weapons.items():
        weapon_data = {**all_stats, **weapon_data}
        for (set_name,set_data) in all_sets.items():
            set_data = {**all_stats, **set_data}
            for sands in artifact_slots['SANDS']:
                for goblet in artifact_slots['GOBLET']:
                    for circlet in artifact_slots['HEAD']:
                        build = Build(Weapon=weapon_data, 
                                            Character=char_data, 
                                            Set=set_data, 
                                            Sands_main=sands, 
                                            Goblet_main=goblet, 
                                            Circlet_main=circlet, 
                                            constraints=constraints,
                                             fit_function=my_fit_function)
                        build.optimize_build()
                        build_id = char_name+"_"+weapon_name+"_"+set_name+"_"+sands+"_"+goblet+"_"+circlet
                        builds[build_id] = build.to_dict()
print("Total Time --- %s seconds ---" % (time.time() - start_time))

builds_df = pd.DataFrame(builds).transpose()
builds_df

builds_df["Percentage of Best DMG"] = builds_df["Final DMG"]*100.0/builds_df["Final DMG"].max()
best_set_art_weapon = builds_df.sort_values("Final DMG", ascending=False).drop_duplicates(['Weapon']).filter(["Weapon", "Sands", "Goblet", "Circlet", "Final ATK", "Final CRATE", "Final CDMG", "Final DMG", "Percentage of Best DMG"])

#best_set_art_weapon.to_excel("all_builds.xlsx")
best_set_art_weapon.to_csv("all_builds.csv")

#best_set_art_weapon.to_excel("results.xlsx")
#best_set_art_weapon.to_csv("results.csv")