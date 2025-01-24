
import pygame
import game_config
import random


terrains = game_config.TERRAINS
plants = ["Tonicroot", "Mindcap", "Rotcarpet", "Toxicroot" "Green Gums"]
monster_parts = ["hide", "head", "teeth"]

# Create multiple quests
quests = []
objective_types = [
    "plants"
    "monster parts"
    "treasure chest"
]
# Define a function to create quests
def create_quest(guild, quest_name, description, objective_type, objective, terrain):
    selected_plant = random.choice(plants)
    chosen_terrain = random.choice(list(terrains.keys()))
    objective_location =     objective_location = (random.randint(1, game_config.region_x), random.randint(1, game_config.region_y))
    # terrain = game_config.TERRAINS[]
    print(f"quest in {chosen_terrain}")
    
    quest = {
        "guild": guild,
        "quest_name": quest_name,
        "description": description,
        "objective_type": objective_type,
        "objective": objective,
        "terrain_type": chosen_terrain,
        "location": objective_location

    }
    return quest
gather_plants = ("Mages Guild", "gather plants", "We need a few more materials for our work here", "plants", random.choice(plants), terrains)
gather_tissues = ("Hunters Guild", "Cull the beasts", "We've got a beast problem", random.choice(monster_parts), random.choice(list(game_config.beasts_dict.keys())), terrains)

# Mages Guild quests
quests.append(create_quest(*gather_plants))
quests.append(create_quest(*gather_tissues))

# # Other Guild quests
# quests.append(create_quest("Warriors Guild", "defend the village", "Protect the village from bandits", ["Sword", "Shield"], terrains))
# quests.append(create_quest("Thieves Guild", "steal the artifact", "Retrieve the ancient artifact from the castle", ["Lockpick", "Dagger"], terrains))

# Print all quests
for quest in quests:
    print(f"Guild: {quest['guild']}")
    print(f"Quest: {quest['quest_name']}")
    print(f"Description: {quest['description']}. We need you to aquire {quest["objective"]} {quest['objective_type']} for us")
    print(f"Terrain Type: {quest['terrain_type']}")
    print(f"Located at {quest['location']}")

# Example Output:
# Guild: Mages Guild
# Quest: gather plants
# Description: We need a few more materials for our work here
# Plant: Tonicroot
# Terrain Type: forest
# Specific Terrain: Enchanted Grove
# --------------------
# (and so on for each quest...)


for beast_key in game_config.beasts_dict:
    beast = game_config.beasts_dict[beast_key]
    print(beast["beastname"])

