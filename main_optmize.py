#Python Main optmize

from constants import all_stats, artifact_slots, Base_Multiplier
from artifacts import all_sets
from weapons import claymores as weapons
from characters import Diluc
from Build import Build
import json
import time

weapons = {name:{"Name":name, "Lv":90, **weapon} for (name,weapon) in weapons.items()}
    
characters = {"Diluc": Diluc}

constraints = {
    "EM": {"minimum":None, "maximum": None},
    "ER": {"minimum":100, "maximum": None}
}

all_stats = {k:0.0 for k in all_stats}

def my_fit_function(sheet):
    b_atk = sheet["BATK"]
    p_atk = sheet["ATK%"]
    atk = sheet["ATK"]
    edmg = sheet["DMG"] + sheet["ELE_DMG"] + sheet["PYRO_DMG"]
    pdmg = sheet["DMG"] + sheet["PHYS_DMG"]
    normal_dmg = sheet["NORM_DMG"]
    skill_dmg = sheet["ELE_SKILL_DMG"]
    burst_dmg = sheet["BURST_DMG"]
    c_rate = min(sheet["CRATE"],100)
    c_dmg = sheet["CDMG"]
    em = sheet["EM"]
    react_dmg = sheet["REACT_DMG"]
    # 2.78 for melt/vap or 6.67 for everything else
    reaction_type_multiplier = 2.78
    # 1.5 for reverse vap, reverse melt; 2 for vap/melt
    # For everything else: Base Multiplier × Character Level Multiplier
    # Base Multiplier up there. Level Multiplier: 80 -> 946.4, 90 -> 1202.8, 100 -> 1674.8
    react_multiplier = 1.5
    # for vap/melt
    react_final_multiplier = react_multiplier * (1+(em/(1400+em))*reaction_type_multiplier + react_dmg/100.0)
    #QAAAEAAAEAAAEAAA (vap on Q and E)
    #return 1.51*(b_atk*(1.0+p_atk/100.0) + atk) *  (edmg/100.0 + 1.0) * (min(c_rate/100.0,1) * c_dmg/100.0 + 1.0)
    return (((326 + 96*3)/100.0*(1+burst_dmg/100.0) * react_final_multiplier + 4*472/100.0*(1+normal_dmg/100.0) + (151 + 156 + 206)/100.0*(1+skill_dmg/100.0)* react_final_multiplier)
            *(b_atk*(1.0+p_atk/100.0) + atk) *  (edmg/100.0 + 1.0) * (min(c_rate/100.0,1) * c_dmg/100.0 + 1.0))/(4+3*4)

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