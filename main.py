
#Modules
import os
import pygame
pygame.init()
pygame.font.init()
import random
from random import randint
import time
from enum import Enum, auto

##  MY Scripts
import game_config
game_config.initalize_screen()
from game_config import screen
import blacksmith
import json
import weapon_class
from weapon_bag import draw_weapon_bag
import adventure_class
import player_class
import combat
import inn
import hunter
 
game_config.check_and_install_packages()
clock = pygame.time.Clock()
pygame.display.set_caption('CortanaRym V 0.4')
weapon_counter = 0
running = True
weapons_found = 0
# Load weapon and adjective data (This calls a class function to load the .jsons required for the class)
weapon_dict = weapon_class.Weapon.load_from_file('weapons.json')
weapon_attributes = weapon_class.Weapon.load_from_file('weapon_adjectives.json')
inventory = []
current_location = "village"
current_weapon_name = "fists"
current_weapon = weapon_dict[current_weapon_name]

####////LOCATION FLAGS////####
in_combat = False
in_weapon_menu = False
in_town = True
####////STATUS FLAGS////####
player_turn_flag = True
YNchoice = False
hostile = {}
####////PLAYER Starting Values////####
encounter_chance = 100
weapon_positions = []
images = []
unique_weapons = {}
player_weapon_bag = []
bagimage_size = (100, 100)  # Define the size to which images will be rescaled



def draw_message_log(screen):
    log_background = pygame.Surface((int(game_config.screen_width * 0.5), game_config.screen_height /5), pygame.SRCALPHA)
    log_background.fill((242, 225, 150, 128))
    game_config.screen.blit(log_background, (game_config.screen_width*.58, game_config.screen_height*.8,))
    y_offset = game_config.screen_height * .96
    for message in game_config.message_log:
        message_surface = game_config.small_font.render(message, True, game_config.BLACK)
        screen.blit(message_surface, (game_config.screen_width* 3/5, y_offset))
        y_offset -= int(game_config.screen_height/35)

def custom_print(*args, **kwargs):
    original_print(*args, **kwargs)
    message = ' '.join(map(str, args))
    game_config.log_message(message)
original_print = print
print = custom_print


class Mode(Enum):
    IN_COMBAT = auto()
    IN_WEAPON_BAG = auto()
    IN_MAP = auto()
    ON_ADVENTURE = auto()
    SHOW_SKILLS = auto()
    IN_BLACKSMITH = auto()
    IN_INN = auto()
    IN_TOWN = auto()
    PRESENT_WEAPON = auto()
    IN_HUNTER = auto()
def set_mode(current_mode, new_mode):
    # Reset all flags
    mode_flags = {
        Mode.IN_COMBAT: False,
        Mode.IN_WEAPON_BAG: False,
        Mode.IN_MAP: False,
        Mode.ON_ADVENTURE: False,
        Mode.SHOW_SKILLS: False,
        Mode.IN_BLACKSMITH: False,
        Mode.IN_INN: False,
        Mode.IN_TOWN: False,
        Mode.PRESENT_WEAPON: False,
        Mode.IN_HUNTER: False
    }
    
    # Set the new mode to True
    mode_flags[new_mode] = True
    return mode_flags
# Initialize the mode flags with a default mode
current_mode = Mode.IN_MAP
mode_flags = set_mode(current_mode, Mode.ON_ADVENTURE)  # Set your initial mode as needed

# Function to change the current mode
def change_mode(new_mode):
    global mode_flags
    mode_flags = set_mode(current_mode, new_mode)

# Define the new function to add weapon to unique_weapons
def acquire_weapon(Weapon):
    global weapons_found
    weapons_found += 1
    unique_key = f"{new_weapon.name} {weapons_found}"
    unique_weapons[unique_key] = new_weapon
    player_weapon_bag.append(new_weapon)
    #print(f'{new_weapon.name} was aquired')

#def make it magical

player_instance = player_class.Player("Hero", weapon_dict )  # Create a Player instance
my_adventure = adventure_class.Adventure(game_config.screen_width, game_config.screen_height)
adventure_class.load_map_images(game_config.TERRAINS, game_config.UNIQUE_LOCATIONS)
adventure_class.update_location(my_adventure.player_pos, my_adventure.visited_grids, game_config.UNIQUE_LOCATIONS)


player_weapon_bag.append(player_instance.current_weapon)

town_background_image = inn.choose_town_background()

print("Welcome to CortanaRym v0.5")
running = True
while running:
    screen.fill(game_config.WHITE)
    clock.tick(60)
################   MODE DRAWS   ##############
################   MODE DRAWS   ##############
################   MODE DRAWS   ##############
    if mode_flags[Mode.IN_MAP]:
        adventure_class.draw_map(my_adventure.player_pos, my_adventure.visited_grids, screen, game_config.screen_width, game_config.screen_height, game_config.GRID_SIZE, game_config.TERRAINS, game_config.UNIQUE_LOCATIONS)
        my_adventure.draw_menu_nav_buttons(screen, game_config.menu_buttons, mode_flags, Mode)
        # print("looking at your map")
    if mode_flags[Mode.IN_BLACKSMITH]:
        blacksmith.draw_blacksmith(screen)
        # print("shopping")
    if mode_flags[Mode.ON_ADVENTURE]:
        my_adventure.draw_adventure(screen, game_config.adventure_buttons, my_adventure.visited_grids, my_adventure.player_pos)
        my_adventure.draw_menu_nav_buttons(screen, game_config.menu_buttons, mode_flags, Mode)
    if mode_flags[Mode.SHOW_SKILLS]:
        player_instance.draw_player_stats(screen, game_config.screen_width, game_config.screen_height)
        my_adventure.draw_menu_nav_buttons(screen, game_config.menu_buttons, mode_flags, Mode)
        # print("reflecting on your skills")
    if mode_flags[Mode.IN_WEAPON_BAG]:
        weapon_positions, images, = draw_weapon_bag(player_weapon_bag, screen, bagimage_size, weapon_dict, player_instance)
        my_adventure.draw_menu_nav_buttons(screen, game_config.menu_buttons, mode_flags, Mode)

    if mode_flags[Mode.IN_COMBAT]:
        #draw the combat buttons and screen
        combat.draw_combat_hud(screen, player_instance, my_adventure, opponent)
        combat.draw_combat_buttons(screen, game_config.combat_buttons)
    if mode_flags[Mode.IN_INN]:
        inn.draw_inn(screen, inn_background_image, player_instance.coinpurse, player_instance.health, player_instance.maxhealth)
    if mode_flags[Mode.IN_HUNTER]:
        hunter.draw_hunter(screen, hunter_background_image, player_instance.coinpurse, player_instance.health, player_instance.maxhealth)
    
    if mode_flags[Mode.IN_TOWN]:
        inn.draw_town(screen, town_background_image)
    if mode_flags[Mode.PRESENT_WEAPON]:
        weapon_positions, images, = draw_weapon_bag(player_weapon_bag, screen, bagimage_size, weapon_dict, player_instance)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    ##########BUTTON ACTIONS###############
    ##########BUTTON ACTIONS################
    ##########BUTTON ACTIONS###############
        if event.type == pygame.MOUSEBUTTONDOWN:
            if mode_flags[Mode.SHOW_SKILLS] or mode_flags[Mode.IN_MAP] or mode_flags[Mode.ON_ADVENTURE] or mode_flags[Mode.IN_WEAPON_BAG]:
            # if in_map or show_skills or on_adventure:
                for button in game_config.menu_buttons:
                    if button["rect"].collidepoint(event.pos):                
                        action = button["text"].lower()
                        if action == "map":
                            mode_flags = set_mode(current_mode, Mode.IN_MAP)
                        if action == "player stats":
                            mode_flags = set_mode(current_mode, Mode.SHOW_SKILLS)
                        if action == "close":
                            mode_flags = set_mode(current_mode, Mode.ON_ADVENTURE)
                        if action == "weapon bag":
                            mode_flags = set_mode(current_mode, Mode.IN_WEAPON_BAG)
                            # mode_flags = set_mode(current_mode, Mode.ON_ADVENTURE)
                        if action == "back to town":                               
                            location = "Town"
                            mode_flags = set_mode(current_mode, Mode.IN_TOWN)
                            my_adventure.player_pos = (10,10)
                        # print(action)

            if mode_flags[Mode.IN_COMBAT]:
                for button in game_config.combat_buttons:
                    if button["rect"].collidepoint(event.pos):
                        action = button["text"].lower()
                        if action == "attack":
                            fight = combat.turn_based_combat(player_instance, my_adventure, opponent, player_instance.current_weapon, my_adventure.visited_grids, my_adventure.player_pos)
                            if fight == "victory":
                                change_mode(Mode.ON_ADVENTURE)
                                time.sleep(0.5)
                        elif action == "run away":
                            opponent.attack()
                            time.sleep(0.2)
                            change_mode(Mode.ON_ADVENTURE)
                            print("You flee.")  # Debug print
                            break

            if mode_flags[Mode.ON_ADVENTURE]:
                for button in game_config.adventure_buttons:
                    if button["rect"].collidepoint(event.pos):
                        if button["text"] == "Loiter":
                            # print(f'Debug1 visited grids: {my_adventure.visited_grids}')
                            # print(f'debug2 {my_adventure.player_pos}')
                            # print(f'Debug3 {my_adventure.visited_grids[tuple(my_adventure.player_pos)]}')
                            # print(f'Debug4 {my_adventure.visited_grids[tuple(my_adventure.player_pos)]["type"]}')
                            loiter_result = adventure_class.determine_encounter(my_adventure.visited_grids[tuple(my_adventure.player_pos)]["type"], game_config.location_events, player_instance.skills)
                            print(loiter_result)
                            if loiter_result == "find_trees":
                                my_adventure.visited_grids[tuple(my_adventure.player_pos)]["trees"] = 5
                                print(my_adventure.visited_grids[tuple(my_adventure.player_pos)])
                                
                            if loiter_result == "beast_encounter":
                                encounter = adventure_class.determine_enemy(my_adventure.player_pos, my_adventure.visited_grids[tuple(my_adventure.player_pos)], encounter_chance, player_instance.level)                           
                                if encounter is not None:
                                    mode_flags = set_mode(current_mode, Mode.IN_COMBAT)
                                    enemy_data = game_config.beasts_dict[encounter]
                                    opponent = combat.Enemy(enemy_data["beastname"], enemy_data)
                                    # print(f'Encounter rolled: you have a {player_instance.current_weapon} equipped.')
                            if loiter_result == "find_weapon":
                                new_weapon = weapon_class.Weapon.create_random_weapon(weapon_dict, player_instance.level)
                                acquire_weapon(new_weapon)
                        elif button["text"] == "Back to Town":                                
                            location = "Town"
                            on_adventure = False
                            in_blacksmith = True
                            my_adventure.player_pos = (10,10)
                            town_background = inn.choose_town_background()
                        elif button["text"] == "Map":
                            in_map = True
                            on_adventure = False
                        elif button["text"] == "Player Stats":
                            show_skills = True
                        #PLAYER MOVMENT BUTTONS
                        elif button["text"] in game_config.player_move:
                            dx, dy = game_config.player_move[button["text"]]
                            new_x = my_adventure.player_pos[0] 
                            new_x+= dx
                            new_y = my_adventure.player_pos[1] 
                            new_y+= dy                           
                            my_adventure.player_pos = my_adventure.movement(my_adventure.player_pos, new_x, new_y)
                            # print(my_adventure.player_pos)
  
            if mode_flags[Mode.IN_BLACKSMITH]:
                for button in blacksmith.blacksmith_buttons:
                    if button["rect"].collidepoint(event.pos):
                        action = button["text"].lower()
                        print(action)
                        if action == "leave":
                            town_background = inn.choose_town_background()
                            mode_flags = set_mode(current_mode, Mode.IN_TOWN)
                        if action =="present":
                            change_mode(Mode.PRESENT_WEAPON)
            if mode_flags[Mode.PRESENT_WEAPON]:
                if event.type == pygame.MOUSEBUTTONDOWN:
                        for weapon_info in weapon_positions:
                            if weapon_info['rect'].collidepoint(event.pos):
                                present = blacksmith.sell_weapon(weapon_class, weapon_info['instance'])                
                                if present == "sell":
                                    # print(weapon_info)
                                    player_instance.coinpurse += weapon_info['instance'].value
                                    player_weapon_bag.remove(weapon_info['instance']) 
                                    # print("Change MODE")
                                change_mode(Mode.IN_BLACKSMITH)   
            if mode_flags[Mode.IN_WEAPON_BAG]: 
                if event.type == pygame.MOUSEBUTTONDOWN:
                        for weapon_info in weapon_positions:
                            if weapon_info['rect'].collidepoint(event.pos):
                                player_instance.current_weapon = weapon_info['instance']
                                print(f"Equipped weapon: {weapon_info['name']}")
            if mode_flags[Mode.IN_INN]:
                for button in inn.inn_buttons:
                    if button["rect"].collidepoint(event.pos):
                        action = button["text"].lower()
                        print(action)
                        if action == "leave":
                            town_background = inn.choose_town_background()
                            mode_flags = set_mode(current_mode, Mode.IN_TOWN)
                        if action == "hot meal - $5":
                            print(player_instance.coinpurse)
                            player_instance.coinpurse -= 5
                            player_instance.health += int((player_instance.maxhealth -player_instance.health)/5) + 5
                            if player_instance.health>player_instance.maxhealth:
                                player_instance.health = player_instance.maxhealth
                        if action == "bed & meal - $10":
                            player_instance.coinpurse -= 10
                            player_instance.health += int((player_instance.maxhealth -player_instance.health)/2) + 5
                            if player_instance.health>player_instance.maxhealth:
                                player_instance.health = player_instance.maxhealth
            if mode_flags[Mode.IN_TOWN]:
                for button in inn.town_buttons:
                    if button["rect"].collidepoint(event.pos):
                        action = button["text"].lower()
                        print(action)
                        if action == "leave":
                            mode_flags = set_mode(current_mode, Mode.ON_ADVENTURE)    
                        if action == "blacksmith":
                            mode_flags = set_mode(current_mode, Mode.IN_BLACKSMITH)
                        if action == "inn":
                            inn_background_image = inn.choose_inn_background()
                            mode_flags = set_mode(current_mode, Mode.IN_INN)  
                        if action == "hunter's guild":
                            hunter_background_image = hunter.choose_hunter_background()
                            change_mode(Mode.IN_HUNTER)
            if mode_flags[Mode.IN_HUNTER]:
                for button in inn.inn_buttons:
                    if button["rect"].collidepoint(event.pos):
                        action = button["text"].lower()
                        print(action)
                        if action == "leave":
                            town_background = inn.choose_town_background()
                            mode_flags = set_mode(current_mode, Mode.IN_TOWN)       

                            
                                                               
    ###   OTHER ACTIONS   ###
    ###   OTHER ACTIONS   ###
    ###   OTHER ACTIONS   ###
    recent_keys = pygame.key.get_pressed()   
    if recent_keys[pygame.K_SPACE]:
        new_weapon = weapon_class.Weapon.create_random_weapon(weapon_dict, player_instance.level)
        acquire_weapon(new_weapon)
        print(f'you found a {new_weapon.name}.')
    if recent_keys[pygame.K_p]:
        for weapon_name, weapon_obj in unique_weapons.items():
            print(f'{weapon_obj.name} : {weapon_obj.min_damage} - {weapon_obj.max_damage} raw Damage per hit')
    if recent_keys[pygame.K_l]:
        print(player_instance.current_weapon)
 
    if recent_keys[pygame.K_j]:
        print(my_adventure.visited_grids)


    
    draw_message_log(screen)
    # print("current mode:", mode_flags)
    pygame.display.flip()
print("End of Main Loop")    
pygame.quit()