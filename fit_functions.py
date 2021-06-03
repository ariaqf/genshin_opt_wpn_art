def calc_total_hp(sheet):
    b_hp = sheet["BHP"]
    p_hp = sheet["HP%"]
    hp = sheet["HP"]
    return b_hp * p_hp/100.0 + hp

def calc_total_def(sheet):
    b_def = sheet["BDEF"]
    p_def = sheet["DEF%"]
    def_ = sheet["DEF"]
    return b_def * p_def/100.0 + def_

def calc_total_atk(sheet):
    b_atk = sheet["BATK"]
    p_atk = sheet["ATK%"]
    atk = sheet["ATK"]
    return b_atk * p_atk/100.0 + atk

def calc_mult_react(sheet):
    em = sheet["EM"]
    react_dmg = sheet["REACT_DMG"]
    reaction_type_multiplier = 2.78
    react_multiplier = 1.5
    return (1+(em/(1400+em))*reaction_type_multiplier + react_dmg/100.0)

def calc_trans_react(sheet):
    em = sheet["EM"]
    react_dmg = sheet["REACT_DMG"]
    reaction_type_multiplier = 2.78
    react_multiplier = 1.5
    return (1+(em/(1400+em))*reaction_type_multiplier + react_dmg/100.0)

def generic_dmg_function(sheet, dmg_type=None):
    edmg = sheet["DMG"] + sheet["ELE_DMG"]
    if(dmg_type is not None):
        edmg += sheet[dmg_type]
    pdmg = sheet["DMG"] + sheet["PHYS_DMG"]
    normal_dmg = sheet["NORM_DMG"]
    skill_dmg = sheet["ELE_SKILL_DMG"]
    burst_dmg = sheet["BURST_DMG"]
    c_rate = min(sheet["CRATE"],100)
    c_dmg = sheet["CDMG"]
    total_hp = calc_total_hp(sheet)
    total_atk = calc_total_atk(sheet)
    # If using reaction, remember to multiply
    # 1.5 for reverse vap, reverse melt; 2 for vap/melt
    # For everything else: Base Multiplier × Character Level Multiplier
    # Base Multiplier up there. Level Multiplier: 80 -> 946.4, 90 -> 1202.8, 100 -> 1674.8
    return total_atk *  (edmg/100.0 + 1.0) * (min(c_rate/100.0,1) * c_dmg/100.0 + 1.0)

def zhongli_fit_function(sheet):
    edmg = sheet["DMG"] + sheet["ELE_DMG"] + sheet["GEO_DMG"]
    pdmg = sheet["DMG"] + sheet["PHYS_DMG"]
    normal_dmg = sheet["NORM_DMG"]
    skill_dmg = sheet["ELE_SKILL_DMG"]
    burst_dmg = sheet["BURST_DMG"]
    c_rate = min(sheet["CRATE"],100)
    c_dmg = sheet["CDMG"]
    total_hp = calc_total_hp(sheet)
    total_atk = calc_total_atk(sheet)
    q_dmg = (7.70*total_atk + 0.33 * total_hp) * (edmg/100.0 + 1.0) * (min(c_rate/100.0,1) * c_dmg/100.0 + 1.0) *(1+burst_dmg/100.0)  
    shield_v = 1.5*(2311 + total_hp*0.205)
    return q_dmg + 4*shield_v