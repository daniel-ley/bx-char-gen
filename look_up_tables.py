stats = ['Str', 'Int', 'Wis', 'Dex', 'Con', 'Cha',]

languages = [
    'Bugbear', 'Dopplganger', 'Dragon', 'Dwarvish', 'Elvish', 
    'Gargoyle', 'Gnoll', 'Gnome', 'Goblin', 'Halfling', 
    'Harpy', 'Hobgolin', 'Kobold', 'Lizard Man', 'Medusa',
    'Minotaur', 'Ogre', 'Orc', 'Pixie', 'Human Dialect',]

xp_for_second_level = {
'cleric' :  1500,
'dwarf' : 2200,
'halfling' : 2000,
'elf' : 4000,
'fighter' : 2000,
'magic user' : 2500,
'thief' : 1200,
}

class_hit_dice = {
'cleric' :  6,
'dwarf' : 8,
'halfling' : 6,
'elf' : 6,
'fighter' : 8,
'magic user' : 4,
'thief' : 4,
}

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

equipment_costs = {
'Battle Ax': 7,
'Hand Ax': 4, 
'Crossbow': 30,
'Case with 30 quarrels': 10,
'Long Bow': 40,
'Short Bow': 25,
'Quiver with 20 arrows': 5,
'silver-tipped arrow': 5,
'Dagger': 3,
'Silver dagger': 30,
'Short Sword': 7,
'Sword': 10,
'Two-handed Sword': 15,
'Mace*': 5,
'Club*': 3,
'Pole Arm (two-handed)': 7,
'Sling with 30 Sling Stones': 2,
'Spear': 3,
'War Hammer': 5,
'Chain Mail Armor': 40,
'Leather Armor': 20,
'Plate Mail Armor': 60,
'Shield': 10,
}
