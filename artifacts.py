from constants import all_stats, sub_buffs, artifact_slots, mean_subroll
from itertools import permutations, combinations, chain, combinations_with_replacement


artifact_set_2pc = {
    "BC": {"PHYS_DMG":25},
    "GF": {"ATK%":18},
    "WT": {"EM":80},
    "PF": {"PHYS_DMG":25},
    "TF": {"ELEC_DMG":15},#, "DT": "Electro" },
    "VV": {"ANEMO_DMG":15},#, "DT": "Anemo"  },
    "AP": {"GEO_DMG":15},#, "DT": "Geo"},
    "CW": {"PYRO_DMG":15},#, "DT": "Pyro"},
    "BS": {"CRYO_DMG":15},#, "DT": "Cryo"},
    "HD": {"HYDRO_DMG":15},#, "DT": "Hydro", },
    "NO": {"BURST_DMG":20},#, "T": "Burst"},
    "TM": {"HP%": 20}
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
    "TF": {"ELEC_DMG":15, "REACT_DMG":40},#, "DT": "Electro" },
    "VV": {"ANEMO_DMG":15, "REACT_DMG":60},#, "DT": "Anemo"  },
    "AP": {"GEO_DMG":15},#, "DT": "Geo"},
    "AP!": {"GEO_DMG":15, "ELE_DMG":35},#, "DT": "Geo"}
    "CW": {"PYRO_DMG":15, "REACT_DMG":40},#, "DT": "Pyro"},
    "CW!": {"PYRO_DMG":37.5, "REACT_DMG":40},#, "DT": "Pyro"},
    "BS": {"CRYO_DMG":15, "CRATE": 20},#, "DT": "Cryo"},
    "BS!": {"CRYO_DMG":15, "CRATE": 40},#, "DT": "Cryo"},
    "HD": {"HYDRO_DMG":15},#, "DT": "Hydro", },
    "NO": {"BURST_DMG":20},#, "T": "Burst"},
    "NO!": {"BURST_DMG":20, "ATK%": 20},#, "T": "Burst"},
    "TM": {"HP%": 20},
    "TM!": {"HP%": 20, "ATK%": 20}    
}

sets_4pc = {k:v for (k,v) in artifact_set_4pc.items()}

for (i,v1) in artifact_set_2pc.items():
    for (j,v2) in artifact_set_2pc.items():
        set_s = {k:0.0 for k in all_stats}
        if (i!=j):
            for sub in v1:
                set_s[sub] += v1[sub]
            for sub2 in v2:
                set_s[sub2] += v2[sub2]
            sets_4pc[i+j] = set_s


for (k,v) in sets_4pc.items():
    sec_stats = {k:0.0 for k in all_stats}
    sets_4pc[k] = {**sec_stats,**v}
    
all_sets = {name:{"Name":name, **_set} for (name,_set) in sets_4pc.items()}