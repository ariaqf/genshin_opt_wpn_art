from Build import Build
from constants import artifact_slots, sub_buffs

from random import Random
from itertools import combinations, combinations_with_replacement

all_subs = list(combinations(sub_buffs,4))
for i in range(len(all_subs)):
    all_subs[i] = tuple(sorted(all_subs[i]))
all_subs = set(all_subs)
sub_slot = {}
for (slot,atts) in artifact_slots.items():
    sub_slot[slot] = {}
    for att in atts:
        sub_slot[slot][att] = []
        for m_subs in all_subs:
            not_in = att not in m_subs
            if(not_in):
                sorts = combinations_with_replacement(m_subs,5)
                for comb in sorts:
                    sub_slot[slot][att].append(comb+m_subs)

def random_build(weapon_data, char_data, set_data, sands, goblet, circlet, constraints, my_fit_function):
        r = Random()
        r.seed(time.time())
        build = Build(Weapon=weapon_data, 
                            Character=char_data, 
                            Set=set_data, 
                            Sands_main=sands, 
                            Goblet_main=goblet, 
                            Circlet_main=circlet, 
                            constraints=constraints,
                            fit_function=my_fit_function,
                            starting_subs= {
                                "plume": list(r.choice(sub_slot["PLUME"]["ATK"])), 
                                "flower": list(r.choice(sub_slot["FLOWER"]["HP"])), 
                                "sands": list(r.choice(sub_slot["SANDS"][sands])), 
                                "goblet": list(r.choice(sub_slot["GOBLET"][goblet])), 
                                "circlet": list(r.choice(sub_slot["HEAD"][circlet]))
                            })
        build.optimize_build()
        return build