from random import randint, choice
import copy
from look_up_tables import stats, languages, xp_for_second_level, \
    saving_throws, class_hit_dice, equipment_costs


number_of_characters_to_create = 3
reroll_low_hp = True
low_dice_result = 2
human_weighting = 50


def dice_roller(dice_count: int, dice_size: int, reroll_low_result: bool) -> int:
    
    result = 0
    for _ in range(0, dice_count):

        if reroll_low_result == True:

            while result <= low_dice_result:
                result = 0
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


def determine_charisma_mods(charisma_stat: int) -> dict:
    reaction_adjustment = 0
    max_retainers = 0
    retainer_morale = 0
    
    if charisma_stat == 3:
        reaction_adjustment = -2
        max_retainers = 1
        retainer_morale = 4
    elif charisma_stat >= 4 and charisma_stat <= 5:   
        reaction_adjustment = -1
        max_retainers = 2
        retainer_morale = 5
    elif charisma_stat >= 6 and charisma_stat <= 8:
        reaction_adjustment = -1
        max_retainers = 3
        retainer_morale = 6
    elif charisma_stat >= 9 and charisma_stat <= 12:
        reaction_adjustment = 0
        max_retainers = 4
        retainer_morale = 7
    elif charisma_stat >= 13 and charisma_stat <= 15:
        reaction_adjustment = +1
        max_retainers = 5
        retainer_morale = 8
    elif charisma_stat >= 16 and charisma_stat <= 17:
        reaction_adjustment = +1
        max_retainers = 6
        retainer_morale = 9
    else: 
        reaction_adjustment = +2
        max_retainers = 7
        retainer_morale = 10
    
    return {'reaction_adjustment': reaction_adjustment,
        'max_retainers': max_retainers,
        'retainer_morale': retainer_morale,
        }


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
    class_specific_saves = saves[character['character_class'].lower()]
    char_saves = copy.deepcopy(class_specific_saves)
    
    if wis_bonus != 0:
        char_saves['death_ray_or_poison'] = \
            f"{str(int(char_saves['death_ray_or_poison']) + wis_bonus)} / {char_saves['death_ray_or_poison']} (magic)"    
        char_saves['magic_wands'] = char_saves['magic_wands'] - wis_bonus
        char_saves['paralysis_or_turn_to_stone'] = char_saves['paralysis_or_turn_to_stone'] - wis_bonus
        char_saves['rods_staves_or_spells'] = char_saves['rods_staves_or_spells'] - wis_bonus
    return char_saves


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

    hit_dice_max = class_hit_dice[character['character_class'].lower()]
    hp = dice_roller(1, hit_dice_max, reroll_low_hp)
    hp += con_bonus
    character['HP'] = hp

    return character


def determine_languages(character: dict) -> list:

    languages_known = ['Common', 'Alignment Tongue',]
    
    if character['character_class'] == 'Dwarf':
        languages_known += ['Dwarf', 'Gnome', 'Kobold', 'Goblin',]
    
    if character['character_class'] == 'Elf':
        languages_known += ['Elvish', 'Orc', 'Hobgoblin', 'Gnoll',]

    if character['Int'] >= 13 and character['Int'] <= 15:
        additional_languages = 1
    elif character['Int'] >= 16 and character['Int'] <= 17:
        additional_languages = 2
    elif character['Int'] == 18:
        additional_languages = 3
    else: additional_languages = 0

    if additional_languages > 0:
        candidate_languages = []
        for language in languages:
            if language not in languages_known:
                candidate_languages.append(language)
        
        for _ in range(additional_languages):
            new_language = choice(candidate_languages)
            languages_known.append(new_language)
            candidate_languages.remove(new_language)

    return languages_known


def determine_starting_gold():
    return dice_roller(3, 6, False) * 10


def equip_character(character: dict, gold: int):
    equipment = "none"
    if character['character_class'] in ['Elf', 'Fighter',]:
        equipment = "Sword"
        gold = gold - 10
    # To Do - Added equipment shopping logic

    return equipment, gold


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
        equipment, gold = equip_character(character_attributes, gold)

        
        print(f'{character_attributes}\nStat Bonuses: {stat_bonuses}\n{determine_charisma_mods(char_attributes["Cha"])}')
        print(f'{saves}\nStarting Gold : {gold} Equipment : {equipment}')
        print(f'Prime Requisite XP Mod : {int(determine_prime_requisite_xp_mod(char_attributes) * 100)}%  ', end='')
        print(f'XP for Next Level : {xp_for_second_level[char_attributes["character_class"].lower()]}')
        print(f'Languages: {determine_languages(character_attributes)}')
        print("\n")
        

if __name__ == '__main__':
    main()
