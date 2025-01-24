import json
import random

class Weapon:
    def __init__(self, name, adjective, weapon_type, hitChance, min_damage, max_damage, value, min_level, carry_weight, extra_attribute):
        self.name = name
        base_name = name
        self.adjective = adjective
        self.weapon_type = weapon_type
        self.hitChance = hitChance
        self.min_damage = min_damage
        self.max_damage = max_damage
        self.value = value
        self.min_level = min_level
        self.carry_weight = carry_weight
        self.extra_attribute = extra_attribute


    def __repr__(self):
            return f"Weapon(name={self.name}, adjective={self.adjective}, weapon_type={self.weapon_type}, min_damage={self.min_damage}, max_damage={self.max_damage}, value={self.value}, min_level={self.min_level}, carry_weight={self.carry_weight}, extra_attribute={self.extra_attribute})"
    @classmethod
    def load_from_file(cls, filename):
        with open(filename, 'r') as file:
            return json.load(file)
        
    @classmethod
    def create_random_weapon(cls, weapon_dict, player_level):
        weapons_list = []
        for name, attributes in weapon_dict.items():
            if attributes['min_level'] <= player_level:
                probability_int = round(attributes['probability'] * 10)
                for _ in range(probability_int):
                    weapons_list.append(cls(
                        name, 
                        None,
                        attributes.get('weapon_type', 'unknown'),
                        attributes['hitChance'], 
                        attributes['min_damage'], 
                        attributes['max_damage'],
                        attributes['value'],
                        attributes['min_level'],
                        attributes['weapon_type'],
                        attributes.get('carry_weight', 0),
                        # None
                    ))
        return random.choice(weapons_list)
    
    
    @classmethod
    def create_weapon(cls, weapon_data):
        return cls(
            weapon_data.get('name', 'unknown'),
            weapon_data.get('adjective', None),
            weapon_data.get('weapon_type', 'unknown'),
            weapon_data['hitChance'],
            weapon_data['min_damage'],
            weapon_data['max_damage'],
            weapon_data['value'],
            weapon_data['min_level'],
            weapon_data.get('carry_weight', 0),
            weapon_data['weapon_type']
        )
