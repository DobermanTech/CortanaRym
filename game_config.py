import pygame
import os
import sys
import random

pygame.font.init()
global screen_height
global screen_width
screen_width, screen_height = 1680, 1050
clock = pygame.time.Clock()
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
darktan = (90, 40, 40)
lighttan = (220, 190, 90)
dropshadow_color = (50, 0, 0)
roso= (150, 15, 15)
yellow = (255,222,89)
woodtan = (196, 155, 99)
button_color = (90, 90, 40)
font = pygame.font.Font(None, 32)
BIG_font = pygame.font.Font(None, 84)
small_font = pygame.font.Font(None, 24)
menu_font = pygame.font.Font(None, 14)
game_data = "game_data.txt" #WEAPONS ARE FROM JSONS
forest_photos = 'images/landscape/forest/'
castle_photos = 'images/landscape/castle/'
swamp_photos = 'images/landscape/swamp/'
meadow_photos = 'images/landscape/forest/'
town_gate_photos = "iamges/landscape/town/"
damage_hitsplat = "images/damage_hitsplat.png"
hitsplat_image = pygame.image.load(damage_hitsplat)
hitsplat_image = pygame.transform.scale(hitsplat_image, (screen_width/11, screen_height/11))
small_splat_rect = hitsplat_image.get_rect()
player_image_file = "images/player.png"
player_image = pygame.image.load(player_image_file)


GRID_SIZE = 64
region_x, region_y = (15,15)




def initalize_screen():
    global screen
    screen = pygame.display.set_mode((screen_width, screen_height))
import subprocess
import sys

def install_package(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def check_and_install_packages(requirements_file='requirements.txt'):
    with open(requirements_file, 'r') as file:
        packages = file.readlines()

    for package in packages:
        package = package.strip()
        if not package:  # Skip empty lines
            continue
        try:
            __import__(package.split('==')[0])  # Try to import the package
            # print(f'package {package} loaded')
        except ImportError:
            install_package(package)   # Install the package if not installed
            print(f'installing{package}')



#I DON"T KNOW how I ended up with two of them... but this one didn't seem nessessary
# def load_game_data(filename):
#     # Determine if the application is a frozen .exe
#     if getattr(sys, 'frozen', False):
#         datadir = os.path.dirname(sys.executable)
#     else:
#         datadir = os.path.dirname(__file__)
#     game_data_path = os.path.join(datadir, 'game_data.txt')
#     weapons_json_path = os.path.join(datadir, 'weapons.json')
#     requirements_txt_path = os.path.join(datadir, 'requirements.txt')
#     # Make sure to check if the files exist
#     if not os.path.exists(game_data_path):
#         raise FileNotFoundError(f"File not found: {game_data_path}")
#     if not os.path.exists(weapons_json_path):
#         raise FileNotFoundError(f"File not found: {weapons_json_path}")
#     if not os.path.exists(requirements_txt_path):
#         raise FileNotFoundError(f"File not found: {requirements_txt_path}")



import re

def load_game_data(filename):
    data = {}
    current_section = None

    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith("#"):
                current_section = line.strip("# ").lower().replace(" ", "_")
                if current_section in ["beasts", "weapon_list", "items"]: 
                    data[current_section] = []
                elif current_section == "location_events":
                    data[current_section] = {}
                else:
                    data[current_section] = {}
            elif line and current_section:
                if current_section == "location_events":
                    if ":" in line:
                        terrain, events = line.split(": ")
                        event_list = [tuple(event.split(',')) for event in events.split(';')]
                        if terrain not in data[current_section]:
                            data[current_section][terrain] = []
                        data[current_section][terrain].extend([(e.strip(), int(w.strip())) for e, w in event_list])
                elif ":" in line and current_section not in ["beasts"]:
                    key, value = line.split(":", 1)
                    data[current_section][key.strip()] = eval(value.strip())
                else:
                    data[current_section].append(line.strip())

    return data

# Testing the function with your input data
game_data = load_game_data('game_data.txt')
# print(game_data)


game_data = load_game_data('game_data.txt')
locations = game_data['locations']
events = game_data['events']
location_events = game_data['location_events']
characters = game_data['characters']
beasts_list = game_data['beasts']
# weapon_list = game_data['weapon_list']
items = game_data['items']
location = "tavern"
beasts_dict = {
    beast.split(", ")[0]: {
        "beastname": beast.split(", ")[0],
        "health": int(beast.split(", ")[1].split(": ")[1]),
        "min_damage": int(beast.split(", ")[2].split(": ")[1].split("-")[0]),
        "max_damage": int(beast.split(", ")[2].split(": ")[1].split("-")[1]),
        "xp": int(beast.split(", ")[3].split(": ")[1]),
        "min_level": int(beast.split(", ")[4].split(": ")[1]),
        "env": beast.split(", ")[5].split(": ")[1].split("-")
    } for beast in beasts_list
}
# print(beasts_dict["dragon"])

TERRAINS = {
    "forest": {"color": (200,255,200)},  # Use color for forests
    "swamp": {"color": (0, 0, 255), "image": "images/map icons/crypt.png"},  # Relative path
    "castle": {"color": (255, 0, 0), "image": "images/map icons/castle.png"},  # Relative path
    "meadow": {"color": (20,200,20)}  # Use color for meadows
    }

towngate_image_list = os.listdir('images/landscape/town/')
# print(towngate_image_list)
town_gate_file = random.choice(towngate_image_list)
town_gate_filename = os.path.basename(town_gate_file)

UNIQUE_LOCATIONS = {
    (10,10): {"location" : "Town", "color": 'BLACK', "Reputation": 10, "type" : "Town", "background": f'{town_gate_filename}'},
    (3,5): {"location" : "Fort Timble", "type": "Outpost", "color": "BLACK", "Reputation": 10},
    (12,12): {"location": "magic portal", "type": "Secret Mission Objective", "color": (255, 0, 255), "image": "images/map icons/portal.png"}  # Relative path
    }

# Define weights for each terrain type
TERRAIN_WEIGHTS = {
    "forest": 2,
    "swamp": 0.75,
    "castle": 1,
    "meadow": 2
    }
# Define the movement actions
player_move = {
    "Go North": (0, -1),
    "Go South": (0, 1),
    "Go East": (1, 0),
    "Go West": (-1, 0)
}
adventure_buttons = [
    {"rect": pygame.Rect(60, 700, 100, 50), "color": BLACK, "text": "Go West"},
    {"rect": pygame.Rect(280, 700, 100, 50), "color": BLACK, "text": "Go East"},
    {"rect": pygame.Rect(170, 760, 100, 50), "color": BLACK, "text": "Go South"},
    {"rect": pygame.Rect(170, 640, 100, 50), "color": BLACK, "text": "Go North"},
    {"rect": pygame.Rect(170, 700, 100, 50), "color": RED, "text": "Loiter"}
]

chop_wood_button = {"rect": pygame.Rect(20, screen_height *.9, 100, 50), "color": BLACK, "text": "Chop Wood"}
mine_stone_button = {"rect": pygame.Rect(20, screen_height *.9, 100, 50), "color": BLACK, "text": "Mine Stone"}

# map_buttons = [
#     {"rect": pygame.Rect(screen_width -275, screen_height/5, 200, 3*screen_height/5), "color": lighttan, "text": ""},
#     {"rect": pygame.Rect(screen_width -250, screen_height/4, 150, 100), "color": darktan, "text": "Close Map"}
#]

menu_buttons = [
    {"rect": pygame.Rect(10, 570, 200, 50), "color": darktan, "text": "Close"},
    {"rect": pygame.Rect(10, 510, 200, 50), "color": darktan, "text": "Player Stats"},
    {"rect": pygame.Rect(10, 450, 200, 50), "color": darktan, "text": "Map"},
    {"rect": pygame.Rect(10, 390, 200, 50), "color": darktan, "text": "Weapon Bag"},
    {"rect": pygame.Rect(10, 330, 200, 50), "color": darktan, "text": "Back to Town"},
]
combat_buttons = [
    {"rect": pygame.Rect(10, 700, 140, 50), "color": GREEN, "text": "Use an Item"},
    {"rect": pygame.Rect(10, 625, 140, 50), "color": BLACK, "text": "Run Away"},
    {"rect": pygame.Rect(10, 550, 140, 50), "color": RED, "text": "Attack"},
]

spells = {
    "Heat": {"lifestyle": "Pain", "danage": "3-8", "description": "Pour energy directly into heating (or melting) anything within spell range. Causes Immeadite damage at a high mana cost."}
    }



def get_region(player_pos):
    third_of_x = region_x/3
    third_of_y = region_y/3
    x, y = tuple(player_pos)
    if x < third_of_x and y < third_of_y:
        return 'northwest'

    elif third_of_x <= x < 2*third_of_x and y < third_of_y:
        return 'north'
    elif x >= 2*third_of_x and y < third_of_y:
        return 'northeast'
    elif x < third_of_x and third_of_y <= y < 2*third_of_y:
        return 'west'
    elif third_of_x <= x < 2*third_of_x and third_of_y <= y < 2*third_of_y:
        return 'central'
    elif x >= 2*third_of_x and third_of_y <= y < 2*third_of_y:
        return 'east'
    elif x < third_of_x and y >= third_of_y:
        return 'southwest'
    elif third_of_x <= x < 2*third_of_x and y >= 2*third_of_y:
        return 'south'
    else:
        return 'southeast'
global message_log
message_log = []
def log_message(message):
    if len(message_log) >= 5:
        message_log.pop(0)
    message_log.append(message)

def custom_print(*args, **kwargs):
    original_print(*args, **kwargs)
    message = ' '.join(map(str, args))
    log_message(message)

original_print = print
print = custom_print
def draw_message_log(screen):
    log_background = pygame.Surface((int(screen_width * 0.5), screen_height /5), pygame.SRCALPHA)
    log_background.fill((242, 225, 150, 128))
    screen.blit(log_background, (screen_width*.58, screen_height*.8,))
    y_offset = screen_height * .96
    for message in message_log:
        message_surface = small_font.render(message, True, BLACK)
        screen.blit(message_surface, (screen_width* 3/5, y_offset))
        y_offset -= int(screen_height/35)

def setscreenres(screen_width, screen_height):
    global screen_res 
    screen_res = (screen_width, screen_height)
setscreenres(screen_width, screen_height)

def pause(duration):
    start_time = pygame.time.get_ticks()
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # You can add a key to unpause if needed
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                paused = False

        current_time = pygame.time.get_ticks()
        if current_time - start_time >= duration:
            paused = False

        # # Display "Paused" message
        # font = pygame.font.Font(None, 74)
        # text = font.render("Paused", True, (255, 0, 0))
        # screen.fill((0, 0, 0))  # Clear the screen
        # screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2,
        #                    screen.get_height() // 2 - text.get_height() // 2))
        # pygame.display.flip()
