from random import randint

stats = ['Str', 'Int', 'Wis', 'Dex', 'Con', 'Cha',]
number_of_characters_to_create = 2
low_dice_result = 2
human_weighting = 50

saving_throws = {
'normal_man' : 
{'death_ray_or_poison' : 14,
'magic_wands' : 15,
'paralysis_or_turn_to_stone' : 16,
'dragon_breath' : 17,
'rods_staves_or_spells' : 17},

'cleric' : 
{'death_ray_or_poison' : 11,
'magic_wands' : 12,
'paralysis_or_turn_to_stone' : 14,
'dragon_breath' : 16,
'rods_staves_or_spells' : 15},

'dwarf' : 
{'death_ray_or_poison' : 10,
'magic_wands' : 11,
'paralysis_or_turn_to_stone' : 12,
'dragon_breath' : 13,
'rods_staves_or_spells' : 14},

'halfling' : 
{'death_ray_or_poison' : 10,
'magic_wands' : 11,
'paralysis_or_turn_to_stone' : 12,
'dragon_breath' : 13,
'rods_staves_or_spells' : 14},

'elf' : 
{'death_ray_or_poison' : 12,
'magic_wands' : 13,
'paralysis_or_turn_to_stone' : 13,
'dragon_breath' : 15,
'rods_staves_or_spells' : 15},

'fighter' : 
{'death_ray_or_poison' : 12,
'magic_wands' : 13,
'paralysis_or_turn_to_stone' : 14,
'dragon_breath' : 15,
'rods_staves_or_spells' : 16},

'magic user' : 
{'death_ray_or_poison' : 13,
'magic_wands' : 14,
'paralysis_or_turn_to_stone' : 13,
'dragon_breath' : 16,
'rods_staves_or_spells' : 15},

'thief' : 
{'death_ray_or_poison' : 13,
'magic_wands' : 14,
'paralysis_or_turn_to_stone' : 13,
'dragon_breath' : 16,
'rods_staves_or_spells' : 15},
}


def dice_roller(dice_count: int, dice_size: int, reroll_low_result: bool) -> int:
    
    result = 0
    for _ in range(0, dice_count):

        if reroll_low_result == True:

            while result <= low_dice_result:
                result = result + randint(1, dice_size)

        else:
            result = result + randint(1, dice_size)

    return result


def stats_roller() -> dict:

    stat_block = {}
    stat_block['character_class'] = 0

    for characteristic in stats:
        stat_block[characteristic] = dice_roller(3, 6, False)

    return stat_block


def determine_bonuses_and_penalties(character_statistics: dict) -> dict:

    bonuses_and_penalties = {}

    for characteristic in stats:

        bonus = ''
        stat = character_statistics[characteristic] 

        if stat == 3: bonus = -3
        elif stat >= 4 and stat <= 5:   bonus = -2
        elif stat >= 6 and stat <= 8:   bonus = -1
        elif stat >= 9 and stat <= 12:  bonus = 0
        elif stat >= 13 and stat <= 15: bonus = 1
        elif stat >= 16 and stat <= 17: bonus = 2
        elif stat == 18: bonus = 3
        else: bonus = 0
        
        bonuses_and_penalties[characteristic] = bonus

    return bonuses_and_penalties

def calculate_prime_requisite_mod(attribute_value: int) -> float:
    xp_mod = None
    if attribute_value <= 5: xp_mod = -0.2
    elif attribute_value >= 6 and attribute_value <= 8:   xp_mod = -0.1
    elif attribute_value >= 9 and attribute_value <= 12:  xp_mod = 0
    elif attribute_value >= 13 and attribute_value <= 15: xp_mod = 0.05
    else: xp_mod = 0.1

    return xp_mod

def determine_prime_requisite_xp_mod(char_attributes: dict) -> float:
    
    if char_attributes['character_class'] == 'Fighter':
        prime_requisite = calculate_prime_requisite_mod(char_attributes['Str'])
    elif char_attributes['character_class'] == 'Cleric':
        prime_requisite = calculate_prime_requisite_mod(char_attributes['Wis'])
    elif char_attributes['character_class'] == 'Magic User':
        prime_requisite = calculate_prime_requisite_mod(char_attributes['Int'])
    elif char_attributes['character_class'] == 'Thief':
        prime_requisite = calculate_prime_requisite_mod(char_attributes['Dex'])
    elif char_attributes['character_class'] == 'Dwarf':
        prime_requisite = calculate_prime_requisite_mod(char_attributes['Str'])

    elif char_attributes['character_class'] == 'Elf':
        if char_attributes['Str'] == 13 and char_attributes['Int'] == 16:
            prime_requisite = 0.1
        elif char_attributes['Str'] == 13 or char_attributes['Int'] == 13:
            prime_requisite = 0.05
        else:
            prime_requisite = 0

    elif char_attributes['character_class'] == 'Halfling':
        if char_attributes['Str'] == 13 and char_attributes['Dex'] == 13:
            prime_requisite = 0.1
        elif char_attributes['Str'] == 13 or char_attributes['Dex'] == 13:
            prime_requisite = 0.05
        else:
            prime_requisite = 0

    return prime_requisite


def determine_saving_throws(character: dict, saves: dict, wis_bonus) -> dict:
    base_saves = saves[character['character_class'].lower()]
    saves = base_saves
    if wis_bonus != 0:
        saves['death_ray_or_poison'] = \
            f"{str(saves['death_ray_or_poison'] + wis_bonus)} / {saves['death_ray_or_poison']} (magic)"    
        saves['magic_wands'] = saves['magic_wands'] - wis_bonus
        saves['paralysis_or_turn_to_stone'] = saves['paralysis_or_turn_to_stone'] - wis_bonus
        saves['rods_staves_or_spells'] = saves['rods_staves_or_spells'] - wis_bonus
    return saves


def class_chooser(statistics_block: dict) -> dict:
    
    ordered_stats = sorted(statistics_block.items(), key=lambda x:x[1], reverse=True)
    del ordered_stats[-1]
    ordered_stats = [stat[0] for stat in ordered_stats]

    if (ordered_stats[0] == 'Str' and statistics_block['Con'] >= 9) and \
        randint(1, 100) <= human_weighting:
        statistics_block['character_class'] = 'Dwarf'

    elif statistics_block['Int'] >= 9 and \
        ((ordered_stats[0] == 'Int' and ordered_stats[1] == 'Str') or \
        (ordered_stats[1] == 'Int' and ordered_stats[0] == 'Str')) and \
        randint(1, 100) <= human_weighting:
        statistics_block['character_class'] = 'Elf'

    elif ((statistics_block['Dex'] >= 9 and statistics_block['Con'] >= 9) and \
    ((ordered_stats[0] == 'Str' or ordered_stats[1] == 'Dex') or \
    (ordered_stats[1] == 'Str' or ordered_stats[0] == 'Dex'))) and \
        randint(1, 100) <= human_weighting:
        statistics_block['character_class'] = 'Halfling'

    elif ordered_stats[0] == 'Str':
        statistics_block['character_class'] = 'Fighter'
    
    elif ordered_stats[0] == 'Int':
        statistics_block['character_class'] = 'Magic User'
    
    elif ordered_stats[0] == 'Wis':
        statistics_block['character_class'] = 'Cleric'
    
    elif ordered_stats[0] == 'Dex':
        statistics_block['character_class'] = 'Thief'

    else:
        if ordered_stats[1] == 'Str':
            statistics_block['character_class'] = 'Fighter'
        
        elif ordered_stats[1] == 'Int':
            statistics_block['character_class'] = 'Magic User'
        
        elif ordered_stats[1] == 'Wis':
            statistics_block['character_class'] = 'Cleric'
        
        elif ordered_stats[1] == 'Dex':
            statistics_block['character_class'] = 'Thief'
            
        else:
            statistics_block['character_class'] = 'Fighter'

    return statistics_block


def roll_hp(character: dict, con_bonus: int) -> dict:
    if character['character_class'] == 'Cleric':
        character['HP'] = dice_roller(1, 6, True) + con_bonus
    elif character['character_class'] == 'Fighter':
        character['HP'] = dice_roller(1, 8, True) + con_bonus
    elif character['character_class'] == 'Magic User':
        character['HP'] = dice_roller(1, 4, True) + con_bonus
    elif character['character_class'] == 'Thief':
        character['HP'] = dice_roller(1, 4, True) + con_bonus
    elif character['character_class'] == 'Dwarf':
        character['HP'] = dice_roller(1, 8, True) + con_bonus
    elif character['character_class'] == 'Elf':
        character['HP'] = dice_roller(1, 6, True) + con_bonus
    elif character['character_class'] == 'Halfling':
        character['HP'] = dice_roller(1, 6, True) + con_bonus

    return character


def determine_starting_gold():
    return dice_roller(3, 6, False) * 10


def main() -> None:
    for _ in range(number_of_characters_to_create):
        char_attributes = stats_roller()
        character_attributes = class_chooser(char_attributes)
        stat_bonuses = determine_bonuses_and_penalties(char_attributes)
        character_attributes = roll_hp(character_attributes, \
            stat_bonuses['Con'])
        saves = determine_saving_throws(character_attributes, saving_throws, \
            stat_bonuses['Wis'])
        gold = determine_starting_gold()
        
        print(f'{character_attributes}\n{stat_bonuses}\n{saves}\nStarting Gold : {gold}')
        print(f'Prime Requisite XP Mod : {int(determine_prime_requisite_xp_mod(char_attributes) * 100)}%')
        print("\n")
        

if __name__ == '__main__':
    main()
