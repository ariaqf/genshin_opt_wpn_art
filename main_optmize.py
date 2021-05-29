#Python Main optmize

from Build import Build
import json
import time

allStats = ["BATK", "BDEF", "BHP", "PYRO_DMG", "CRYO_DMG", "HYDRO_DMG", "GEO_DMG", "ELEC_DMG", "ANEMO_DMG", 
            "ELE_DMG", "PHYS_DMG", "REACT_DMG", "DMG", "HP", "ATK", "DEF", "HP%", "ATK%", "DEF%", "EM", "ER", 
            "CRATE", "CDMG", "NORM_DMG", "CHARGE_DMG", "ELE_SKILL_DMG", "BURST_DMG"]

artifact_set_2pc = {
    "BC": {"PHYS_DMG":25},
    "GF": {"ATK%":18},
    "WT": {"EM":80},
    "PF": {"PHYS_DMG":25},
    #"TF": {"ELEC_DMG":15},#, "DT": "Electro" },
    #"VV": {"ANEMO_DMG":15},#, "DT": "Anemo"  },
    #"AP": {"GEO_DMG":15},#, "DT": "Geo"},
    "CW": {"PYRO_DMG":15},#, "DT": "Pyro"},
    #"BS": {"CRYO_DMG":15},#, "DT": "Cryo"},
    #"HD": {"HYDRO_DMG":15},#, "DT": "Hydro", },
    "NO": {"BURST_DMG":20},#, "T": "Burst"},
    #"TM": {"HP%": 20}
}
artifact_set_4pc = {
    "BC": {"PHYS_DMG":25},
    "GF": {"ATK%":18},#, "AT": "Normal", "WT": ["Claymore", "Polearm", "Sword},
    "GF!": {"ATK%":18, "NOMR_DMG": 35, "CHARGE_DMG": 35},#, "AT": "Normal", "WT": ["Claymore", "Polearm", "Sword},
    "WT!": {"EM":80, "CHARGE_DMG": 35}, #"AT": "Charge", "WT": ["Bow", "Catalyst},
    "WT": {"EM":80}, #"AT": "Charge", "WT": ["Bow", "Catalyst},
    "RT!": {"NORM_DMG": 40, "CHARGE_DMG": 40},#, "AT": ["Charge","Normal},
    "TS": {"DMG": 35},
    "LW": {"DMG": 35},
    "PF": {"PHYS_DMG":25},
    "PF!": {"PHYS_DMG":50, "ATK%": 18},
    #"TF": {"ELEC_DMG":15, "REACT_DMG":40},#, "DT": "Electro" },
    #"VV": {"ANEMO_DMG":15, "REACT_DMG":60},#, "DT": "Anemo"  },
    #"AP": {"GEO_DMG":15},#, "DT": "Geo"},
    #"AP!": {"GEO_DMG":15, "ELE_DMG":35},#, "DT": "Geo"}
    "CW": {"PYRO_DMG":15, "REACT_DMG":40},#, "DT": "Pyro"},
    "CW!": {"PYRO_DMG":37.5, "REACT_DMG":40},#, "DT": "Pyro"},
    #"BS": {"CRYO_DMG":15, "CRATE": 20},#, "DT": "Cryo"},
    #"BS!": {"CRYO_DMG":15, "CRATE": 40},#, "DT": "Cryo"},
    #"HD": {"HYDRO_DMG":15},#, "DT": "Hydro", },
    "NO": {"BURST_DMG":20},#, "T": "Burst"},
    "NO!": {"BURST_DMG":20, "ATK%": 20},#, "T": "Burst"},
    #"TM": {"HP%": 20},
    #"TM!": {"HP%": 20, "ATK%": 20}    
}

sets_4pc = {k:v for (k,v) in artifact_set_4pc.items()}

for (i,v1) in artifact_set_2pc.items():
    for (j,v2) in artifact_set_2pc.items():
        if (i!=j):
            sets_4pc[i+j] = {**v1, **v2}


for (k,v) in sets_4pc.items():
    sec_stats = {k:0.0 for k in allStats}
    sets_4pc[k] = {**sec_stats,**v}
    
sets_4pc = {name:{"Name":name, **_set} for (name,_set) in sets_4pc.items()}

artifact_slots = {
    #"HEAD": ["CRATE", "CDMG", "EM", "ATK%", "HP%", "DEF%"],
    #"SANDS": ["ER", "EM", "ATK%", "HP%", "DEF%"],
    #"GOBLET": ["ELE_DMG", "PHYS_DMG", "ATK%", "HP%", "DEF%", "EM"],
    "HEAD": ["CRATE", "CDMG", "ATK%"],
    "SANDS": ["ER", "ATK%"],
    "GOBLET": ["ELE_DMG", "PHYS_DMG", "ATK%"],
    "FLOWER": ["HP"],
    "PLUME": ["ATK"],
}

weapons = {
    "SKY": {"BATK": 674, "ER%": 36.8, "DMG":8},
    "WGS": {"BATK": 608, "ATK%": 69.6},
    "WGS!": {"BATK": 608, "ATK%": 109.6},
    "UNF(0)": {"BATK": 608, "ATK%": 49.6},
    "UNF(1)": {"BATK": 608, "ATK%": 53.6},
    "UNF(2)": {"BATK": 608, "ATK%": 57.6},
    "UNF(3)": {"BATK": 608, "ATK%": 61.6},
    "UNF(4)": {"BATK": 608, "ATK%": 65.6},
    "UNF(5)": {"BATK": 608, "ATK%": 69.6},
    "UNF(1)!": {"BATK": 608, "ATK%": 57.6},
    "UNF(2)!": {"BATK": 608, "ATK%": 65.6},
    "UNF(3)!": {"BATK": 608, "ATK%": 73.6},
    "UNF(4)!": {"BATK": 608, "ATK%": 81.6},
    "UNF(5)!": {"BATK": 608, "ATK%": 89.6},
    "SBP":{"BATK": 741, "PHYS_DMG": 20.7, "ATK%": 16},
    "SBP!":{"BATK": 741, "PHYS_DMG": 20.7, "ATK%": 36, "ASPD%": 12},
    "ARC":{"BATK": 565, "ATK%": 27.6},
    "BLK(0)":{"BATK": 510, "CMDG": 55.1},
    "BLK(1)":{"BATK": 510, "CMDG": 55.1, "ATK%": 12},
    "BLK(2)":{"BATK": 510, "CMDG": 55.1, "ATK%": 24},
    "BLK(3)":{"BATK": 510, "CMDG": 55.1, "ATK%": 36},
    "BLK R5(0)":{"BATK": 510, "CMDG": 55.1},
    "BLK R5(1)":{"BATK": 510, "CMDG": 55.1, "ATK%": 24},
    "BLK R5(2)":{"BATK": 510, "CMDG": 55.1, "ATK%": 48},
    "BLK R5(3)":{"BATK": 510, "CMDG": 55.1, "ATK%": 72},
    "RYL(0)":{"BATK": 565, "CRATE": 0, "ATK%": 27.6},
    "RYL(1)":{"BATK": 565, "CRATE": 8, "ATK%": 27.6},
    "RYL(2)":{"BATK": 565, "CRATE": 16, "ATK%": 27.6},
    "RYL(3)":{"BATK": 565, "CRATE": 24, "ATK%": 27.6},
    "RYL(4)":{"BATK": 565, "CRATE": 32, "ATK%": 27.6},
    "RYL(5)":{"BATK": 565, "CRATE": 40, "ATK%": 27.6},
}

weapons = {name:{"Name":name, "Lv":90, **weapon} for (name,weapon) in weapons.items()}
    
characters = {"Diluc": {
    "Name": "Diluc",
    "Lv": 80,
    "BHP": 12068,
    "BATK": 311,
    "BDEF": 729,
    "CRATE": 24.2,
    "CDMG": 50,
    "EM": 0,
    "PYRO_DMG": 0,
    "CRYO_DMG": 0,
    "HYDRO_DMG": 0,
    "GEO_DMG": 0,
    "ELEC_DMG": 0,
    "ANEMO_DMG": 0,
    "ELE_DMG": 0,
    "PHYS_DMG": 0, 
    "REACT_DMG": 0,
    "ER": 100,
    "ATK_PER_10s": 14,
    #"DT": "Pyro",
    #"WT": "Claymore",
    #"Talents": {
    #    "Normal":[
    #        {"ATK":153.32, "HP": 0, "DEF": 0},
    #        {"ATK":149.79, "HP": 0, "DEF": 0},
    #        {"ATK":168.9, "}HP": 0, "DEF": 0},
    #        {"ATK":229.03, "HP": 0, "DEF": 0}
    #    ], 
    #    "Charge":[], 
    #    "Elemental":[
    #        {"ATK":151.04, "HP": 0, "DEF": 0},
    #        {"ATK":156.16, "HP": 0, "DEF": 0},
    #        {"ATK":206.08, "HP": 0, "DEF": 0}
    #    ], 
    #    "Burst":[
    #        {"ATK":326.4, "HP": 0, "DEF": 0},
    #        {"ATK":96, "HP": 0, "DEF": 0},
    #        {"ATK":326.4, "HP": 0, "DEF": 0}
    #    ]
    #},
    #"Rotation": "NNNENNNENNNENNNQNNNENNNENNNE"
}}

constraints = {
    "EM": {"minimum":None, "maximum": None},
    "ER": {"minimum":100, "maximum": None}
}

allStats = {k:0.0 for k in allStats}
Base_Multiplier = {
    "Burning":0.25,
    "Superconduct":0.5,
    "Swirl":0.6,
    "Electro-Charged":1.2,
    "Shattered":1.5,
    "Overloaded":2
}

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
    char_data = {**allStats, **char_data} 
    for (weapon_name,weapon_data) in weapons.items():
        weapon_data = {**allStats, **weapon_data}
        for (set_name,set_data) in sets_4pc.items():
            set_data = {**allStats, **set_data}
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
best_set_art_weapon.to_csv("results.csv")