from collections import namedtuple

Stats = namedtuple('Stats', "plume flower sands goblet circlet")

class Build:
    sub_buffs = ["HP", "ATK", "DEF", "HP%", "ATK%", "DEF%", "EM", "ER", "CRATE", "CDMG"]
    min_subroll = {
                    'HP': 209,
                    'ATK': 14,
                    'DEF': 16,
                    'HP%': 4.1,
                    'ATK%': 4.1,
                    'DEF%': 5.1,
                    'EM': 16,
                    'ER': 4.5,
                    'CRATE': 2.7,
                    'CDMG': 5.4
                  }
    mean_subroll = {
                    'HP': 254.0,
                    'ATK': 16.75,
                    'DEF': 19.75,
                    'HP%': 4.975,
                    'ATK%': 4.975,
                    'DEF%': 6.2,
                    'EM': 19.75,
                    'ER': 5.5,
                    'CRATE': 3.3,
                    'CDMG': 6.6
                  }
    max_subroll = {
                    'HP': 299,
                    'ATK': 19,
                    'DEF': 23,
                    'HP%': 5.8,
                    'ATK%': 5.8,
                    'DEF%': 7.3,
                    'EM': 23,
                    'ER': 6.5,
                    'CRATE': 3.9,
                    'CDMG': 7.8
                  }
    def __init__(self, Weapon, Character, Set, Sands_main, Goblet_main, Circlet_main, constraints,
                 subroll_to_use=None, fit_function=None, max_total_rolls = 9, max_optimizable_subs = 4, locked_subs = {"plume":[], "flower":[], "sands":[], "goblet":[], "circlet":[]}):
        self.max_total_rolls = max_total_rolls
        self.max_optimizable_subs = min(max_optimizable_subs, 4)
        self.locked_subs = locked_subs
        self.fit_function = self.dmg_calc
        if(fit_function is not None):
            self.fit_function = fit_function
        self.subroll = self.mean_subroll
        if(subroll_to_use is not None and subroll_to_use == "MAX"):
            self.subroll = self.max_subroll
        if(subroll_to_use is not None and subroll_to_use == "MIN"):
            self.subroll = self.min_subroll
        self.weapon = Weapon
        self.character = Character
        self.set = Set
        self.mains = Stats("ATK", "HP", Sands_main, Goblet_main, Circlet_main)
        self.subs = Stats([], [], [], [], [])
        self.final_dmg = 0.0
        self.constraints = constraints
        
        self.calculate_stats()
        
    def calculate_stats(self):
        substats = {"HP":0.0, "ATK":0.0, "DEF":0.0, "HP%":0.0, "ATK%":0.0, "DEF%":0.0, "EM":0.0, "ER":0.0, "CRATE":0.0, "CDMG":0.0}
        for (slot,_subs) in self.subs._asdict().items():
            for sub in _subs:
                substats[sub] += self.subroll[sub]
        self.b_atk = self.weapon["BATK"] + self.character["BATK"]
        self.b_def = self.character["BDEF"]
        self.b_hp = self.character["BHP"]
        self.pyro_dmg = self.character["PYRO_DMG"] + self.weapon["PYRO_DMG"] + self.set["PYRO_DMG"]
        self.cryo_dmg = self.character["CRYO_DMG"] + self.weapon["CRYO_DMG"] + self.set["CRYO_DMG"]
        self.hydro_dmg = self.character["HYDRO_DMG"] + self.weapon["HYDRO_DMG"] + self.set["HYDRO_DMG"]
        self.geo_dmg = self.character["GEO_DMG"] + self.weapon["GEO_DMG"] + self.set["GEO_DMG"]
        self.elec_dmg = self.character["ELEC_DMG"] + self.weapon["ELEC_DMG"] + self.set["ELEC_DMG"]
        self.anemo_dmg = self.character["ANEMO_DMG"] + self.weapon["ANEMO_DMG"] + self.set["ANEMO_DMG"]
        self.norm_dmg = self.character["NORM_DMG"] + self.weapon["NORM_DMG"] + self.set["NORM_DMG"]
        self.charge_dmg = self.character["CHARGE_DMG"] + self.weapon["CHARGE_DMG"] + self.set["CHARGE_DMG"]
        self.ele_skill_dmg = self.character["ELE_SKILL_DMG"] + self.weapon["ELE_SKILL_DMG"] + self.set["ELE_SKILL_DMG"]
        self.burst_dmg = self.character["BURST_DMG"] + self.weapon["BURST_DMG"] + self.set["BURST_DMG"]
        self.e_dmg = self.character["ELE_DMG"] + self.weapon["ELE_DMG"] + (46.6 if self.mains.goblet == "ELE_DMG" else 0.0) + self.set["ELE_DMG"]
        self.p_dmg = self.character["PHYS_DMG"] + self.weapon["PHYS_DMG"] + (58.3 if self.mains.goblet == "PHYS_DMG" else 0.0) + self.set["PHYS_DMG"]
        self.r_dmg = self.character["REACT_DMG"] + self.weapon["REACT_DMG"] + self.set["REACT_DMG"]
        self.dmg = self.character["DMG"] + self.weapon["DMG"] + self.set["DMG"]
        self.hp = self.character["HP"] + self.weapon["HP"] + self.set["HP"] + 4780 + substats["HP"]
        self.atk = self.character["ATK"] + self.weapon["ATK"] + self.set["ATK"] + 311 + substats["ATK"]
        self._def = self.character["DEF"] + self.weapon["DEF"] + self.set["DEF"] + substats["DEF"]
        self.p_hp = self.character["HP%"] + self.weapon["HP%"] + self.set["HP%"] + substats["HP%"] + (46.6 if self.mains.sands == "HP%" else 0.0) + (46.6 if self.mains.goblet == "HP%" else 0.0) + (46.6 if self.mains.circlet == "HP%" else 0.0)
        self.p_atk = self.character["ATK%"] + self.weapon["ATK%"] + self.set["ATK%"] + substats["ATK%"] + (46.6 if self.mains.sands == "ATK%" else 0.0) + (46.6 if self.mains.goblet == "ATK%" else 0.0) + (46.6 if self.mains.circlet == "ATK%" else 0.0)
        self.p_def = self.character["DEF%"] + self.weapon["DEF%"] + self.set["DEF%"] + substats["DEF%"] + (46.6 if self.mains.sands == "DEF%" else 0.0) + (46.6 if self.mains.goblet == "DEF%" else 0.0) + (46.6 if self.mains.circlet == "DEF%" else 0.0)
        self.em = self.character["EM"] + self.weapon["EM"] + self.set["EM"] + substats["EM"] + (187 if self.mains.sands == "EM" else 0.0) + (187 if self.mains.goblet == "EM" else 0.0) + (187 if self.mains.circlet == "EM" else 0.0)
        self.er = self.character["ER"] + self.weapon["ER"] + self.set["ER"] + substats["ER"] + (51.8 if self.mains.sands == "ER" else 0.0)
        self.c_rate = self.character["CRATE"] + self.weapon["CRATE"] + self.set["CRATE"] + substats["CRATE"] + (31.1 if self.mains.circlet == "CRATE" else 0.0)
        self.c_dmg = self.character["CDMG"] + self.weapon["CDMG"] + self.set["CDMG"] + substats["CDMG"] + (62.2 if self.mains.circlet == "CDMG" else 0.0)
        self.atk_per_10s = self.character.get("ATK_PER_10s", 10) / (1-self.weapon.get("ASPD%", 0)/100)
        self.f_atk = self.b_atk*(1+self.p_atk/100.0)+self.atk
        self.f_def = self.b_def*(1+self.p_def/100.0)+self._def
        self.f_hp = self.b_hp*(1+self.p_hp/100.0)+self.hp
        self.update_damage()        
    
    def generate_sheet(self):
        return {
            "BATK": self.b_atk,
            "BDEF": self.b_def,
            "BHP": self.b_hp,
            "ELE_DMG": self.e_dmg,
            "PHYS_DMG": self.p_dmg,
            "REACT_DMG": self.r_dmg,
            "DMG": self.dmg,
            "HP": self.hp,
            "ATK": self.atk,
            "DEF": self._def,
            "EM": self.em,
            "ER": self.er,
            "HP%": self.p_hp,
            "ATK%": self.p_atk,
            "DEF%": self.p_def,
            "CRATE": self.c_rate,
            "CDMG": self.c_dmg,
            "ASPD": self.atk_per_10s/10,
            "PYRO_DMG": self.pyro_dmg,
            "CRYO_DMG": self.cryo_dmg,
            "HYDRO_DMG": self.hydro_dmg,
            "GEO_DMG": self.geo_dmg,
            "ELEC_DMG": self.elec_dmg,
            "ANEMO_DMG": self.anemo_dmg,
            "NORM_DMG": self.norm_dmg,
            "CHARGE_DMG": self.charge_dmg,
            "ELE_SKILL_DMG": self.ele_skill_dmg,
            "BURST_DMG": self.burst_dmg,
        }
        
    def is_valid_exchange(self,slot,new=None,old=None):
        max_one_sub_rolls = self.max_total_rolls - 3
        slot_subs = None
        if slot in self.subs._fields:
            slot_subs = getattr(self.subs, slot)
        else:
            return False
        is_on_roll_limit = slot_subs.count(new) == max_one_sub_rolls
        is_main_stat = getattr(self.mains, slot) == new
        is_on_artifact_limit = len(slot_subs) > self.max_total_rolls
        are_we_trying_to_use_unusable_slots = (slot_subs.count(new) > 0 and slot_subs.count(old) == 1)
        is_not_a_locked_sub = old not in self.locked_subs[slot]
        old_is_empty = old == None
        old_exists_in_subs = slot_subs.count(old) == 1
        return not(is_on_roll_limit
                or is_main_stat
                or is_on_artifact_limit
                or are_we_trying_to_use_unusable_slots) and (old_is_empty or old_exists_in_subs) and is_not_a_locked_sub

    def change_substat(self,slot,new=None,old=None):
        max_one_sub_rolls = self.max_total_rolls - 3
        slot_subs = None
        if slot in self.subs._fields:
            slot_subs = getattr(self.subs, slot)
        else:
            return False
        
        if(new is None):
            return False
        
        if(not(self.is_valid_exchange(slot,new,old))):
            return False
            
        if(new is not None and slot_subs.count(new) < max_one_sub_rolls and getattr(self.mains, slot) != new):
            slot_subs.append(new)
            
        if(old is not None and old in slot_subs):
            slot_subs.remove(old)
            
        if(len(slot_subs) > self.max_total_rolls):
            slot_subs.remove(new)
            return False
            
        if(len(slot_subs) >= self.max_optimizable_subs and len(list(set(slot_subs))) < self.max_optimizable_subs):
            slot_subs.append(old)
            slot_subs.remove(new)
            return False
            
        self.calculate_stats()
        return True
    
    def update_damage(self):
        sheet = self.generate_sheet()
        self.final_dmg =  self.fit_function(sheet)
        
    def dmg_calc(self, character_sheet):
        b_atk = character_sheet["BATK"]
        p_atk = character_sheet["ATK%"]
        atk = character_sheet["ATK"]
        dmg = character_sheet["DMG"]
        c_rate = min(character_sheet["CRATE"],100)
        c_dmg = character_sheet["CDMG"]
        return (b_atk*(1.0+p_atk/100.0) + atk) *  (dmg/100.0 + 1.0) * (min(c_rate/100.0,1) * c_dmg/100.0 + 1.0)
    
    def get_possible_subs(self):
        max_one_sub_rolls = self.max_total_rolls - 3
        add_subs = {k:[] for k in self.subs._fields}
        exchange_subs = {k:[] for k in self.subs._fields}
        total_subs = {k:0 for k in self.subs._fields}
        for slot in add_subs:
            main_stat = getattr(self.mains,slot)
            slot_subs = getattr(self.subs, slot)
            locked_subs = self.locked_subs[slot]
            for s in locked_subs:
                if(s not in slot_subs):
                    slot_subs.append(s)
            total_subs[slot] = len(slot_subs)
            if len(slot_subs) >= self.max_optimizable_subs:
                add_subs[slot] = list(set(slot_subs))
                for s in add_subs[slot]:
                    if(slot_subs.count(s) == max_one_sub_rolls):
                        add_subs[slot].remove(s)
            else:
                add_subs[slot] = self.sub_buffs[:]
                if(main_stat in add_subs[slot]):
                    add_subs[slot].remove(main_stat)
                for s in slot_subs:
                    add_subs[slot].remove(s)
                    
            exchange_subs[slot] = self.sub_buffs[:]
            if(main_stat in exchange_subs[slot]):
                    exchange_subs[slot].remove(main_stat)
            for s in list(set(slot_subs)):
                if(exchange_subs[slot].count(s) == max_one_sub_rolls):
                    exchange_subs[slot].remove(s)
                if(s in self.locked_subs[slot]):
                    exchange_subs[slot].remove(s)
        return {"add":add_subs, "exchange": exchange_subs, "total": total_subs}
            
        
    def get_sub_value_rate(self, investment=1):
        sub_add_upgrade = {k:0.0 for k in self.sub_buffs}
        sub_exchange_upgrade = {k:{k_:0.0 for k_ in self.sub_buffs} for k in self.sub_buffs}
        
        sheet = self.generate_sheet()
        
        baseline = self.fit_function(sheet.copy())
        
        added_value = {k:0.0 for k in self.sub_buffs}
        
        for sub in self.sub_buffs:
            s_sheet = sheet.copy()
            s_sheet[sub] += investment*self.subroll[sub]
            added_value[sub] = self.fit_function(s_sheet)
               
        for sub in sub_add_upgrade:
            sub_added_value = 0
            sub_add_upgrade[sub] = added_value[sub] - baseline
        
        for (sub,others) in sub_exchange_upgrade.items():
            for _sub in others:
                ex = sheet.copy()
                ex[sub] += investment*self.subroll[sub]
                ex[_sub] -= investment*self.subroll[_sub]
                sub_exchange_upgrade[sub][_sub] = self.fit_function(ex) - baseline
        
        for (sub,value) in self.constraints.items():
            if value["minimum"] is not None and sheet[sub] < value["minimum"]:
                sub_add_upgrade[sub] = 2*baseline
                for _sub in sub_exchange_upgrade:
                    if(_sub != sub):
                        sub_exchange_upgrade[_sub][sub] = -2*baseline
                        sub_exchange_upgrade[sub][_sub] = 2*baseline
            if(value["minimum"] is not None and  sheet[sub] - self.subroll[sub] < value["minimum"]):
                for _sub in sub_exchange_upgrade:
                    if(_sub != sub):
                        sub_exchange_upgrade[_sub][sub] = -2*baseline
                        sub_exchange_upgrade[sub][_sub] = 0.0
            if value["maximum"] is not None and  sheet[sub] > value["maximum"]:
                sub_add_upgrade[sub] = 2*baseline
                for _sub in sub_exchange_upgrade:
                    if(_sub != sub):
                        sub_exchange_upgrade[_sub][sub] = 2*baseline
                        sub_exchange_upgrade[sub][_sub] = -2*baseline
            if(value["maximum"] is not None and sheet[sub] - self.subroll[sub] > value["maximum"]):
                for _sub in sub_exchange_upgrade:
                    if(_sub != sub):
                        sub_exchange_upgrade[_sub][sub] = 0.0
                        sub_exchange_upgrade[sub][_sub] = -2*baseline
                        
        return {"add": sub_add_upgrade,
                "exchange": sub_exchange_upgrade}
    
    def to_dict(self):
        return {
                 "Character": self.character["Name"]+" "+str(self.character["Lv"]),
                 "Weapon": self.weapon["Name"]+" "+str(self.weapon["Lv"]),
                 "Artifact Set": self.set["Name"],
                 "Sands": self.mains.sands,
                 "Goblet": self.mains.goblet,
                 "Circlet": self.mains.circlet,
                 "Plume_Subs": "_".join([str(self.subs.plume.count(u))+u for u in set(self.subs.plume)]),
                 "Flower_Subs": "_".join([str(self.subs.flower.count(u))+u for u in set(self.subs.flower)]),
                 "Sands_Subs": "_".join([str(self.subs.sands.count(u))+u for u in set(self.subs.sands)]),
                 "Goblet_Subs": "_".join([str(self.subs.goblet.count(u))+u for u in set(self.subs.goblet)]),
                 "Circlet_Subs": "_".join([str(self.subs.circlet.count(u))+u for u in set(self.subs.circlet)]),
                 "Final ATK": self.f_atk,
                 "Final DEF": self.f_def,
                 "Final HP": self.f_hp,
                 "Final EM": self.em,
                 "Final ER": self.er,
                 "Final ELE_DMG Bonus": self.e_dmg + self.pyro_dmg+self.cryo_dmg+self.hydro_dmg+self.geo_dmg+self.elec_dmg+self.anemo_dmg,
                 "Final PHYS_DMG Bonus": self.p_dmg,
                 "Final NORM_DMG": self.norm_dmg,
                 "Final CHARGE_DMG":self.charge_dmg,
                 "Final ELE_SKILL_DMG":self.ele_skill_dmg,
                 "Final BURST_DMG":self.burst_dmg,
                 "Final REACT_DMG": self.r_dmg,
                 "Final ASPD": self.atk_per_10s/10,
                 "Final CRATE": self.c_rate,
                 "Final CDMG": self.c_dmg,
                 "Final DMG": self.final_dmg,
                }

    def optimize_build(self):
        trial = True
        runs = 0
        max_runs = 100
        while(trial and runs < max_runs):
            possible = self.get_possible_subs()
            rates = self.get_sub_value_rate()
            total_operations = 0
            for slot in possible["add"]:
                best_sub = None
                best_removal = None
                p_list = []
                op_type = ""
                valid_exchange = False
                if(possible["total"][slot] < self.max_total_rolls):
                    op_type = "Add"
                    p_list = possible["add"][slot]
                    for sub in p_list:
                        if best_sub is None or rates['add'][best_sub] < rates['add'][sub]:
                            best_sub = sub
                        else:
                            pass
                if(possible["total"][slot] == self.max_total_rolls):
                    op_type = "Exchange"
                    p_list = possible["exchange"][slot]
                    for sub in p_list:
                        for (_sub, value) in rates['exchange'][sub].items():
                            valid_exchange = self.is_valid_exchange(slot,sub,_sub)
                            if (_sub in p_list and valid_exchange and 
                                ((best_sub is None and best_removal == None) or (rates['exchange'][best_sub][best_removal] < rates['exchange'][sub][_sub])) 
                                and rates['exchange'][sub][_sub] > 0):
                                best_sub = sub
                                best_removal = _sub
                            else: 
                                pass
                slot_subs = getattr(self.subs,slot)
                if(best_sub is not None and self.change_substat(slot, best_sub, best_removal)):
                    total_operations += 1
                    rates = self.get_sub_value_rate()
                if(False): 
                    #Log for debug
                    print(slot)
                    print(valid_exchange)
                    print(possible["total"][slot])
                    print(op_type)
                    print(best_sub)
                    print(best_removal)
                    print(p_list)
                    print(getattr(self.subs,slot))
                    print("*******************")
            if total_operations == 0:
                trial = False
            runs+=1