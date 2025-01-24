import os
import pygame
import os
import weapon_class
import random
import time
import game_config
from game_config import screen_height, screen_width
player_level = 4
default_timer = 6
# screen_width, screen_height = 1280, 1024
from game_config import screen_width, screen_height
game_data = "game_data(recursive dic).txt"
inn_photos = 'images/inn/backgrounds/'
pygame.font.init()
fancyfont = pygame.font.SysFont("serif", 30)
scrawlfont = pygame.font.SysFont('segoescript', 32)
darktan = (90, 40, 40)
lighttan = (220, 190, 90)
dropshadow_color = (50, 0, 0)
roso= (150, 15, 15)
woodtan = (196, 155, 99)
#randomly choose a background
def choose_inn_background():
    inn_background_dump = os.listdir(inn_photos)
    inn_png_files = [f for f in inn_background_dump if os.path.isfile(os.path.join(inn_photos, f)) and f.lower().endswith(('.png'))]
    if inn_png_files:
        backgroud_file = random.choice(inn_png_files)
    inn_background_image = pygame.image.load(os.path.join("images/inn/backgrounds", backgroud_file)).convert_alpha()
    inn_background_image = pygame.transform.scale(inn_background_image, (screen_width, screen_height))
    return inn_background_image
inn_background_image = choose_inn_background()   
menu_box = pygame.Surface((screen_width/4, screen_height), pygame.SRCALPHA)
roomtitle_rect = pygame.Rect((screen_width - (0.22 * screen_width)), 95, 240, 200)
#load and locate the sign
roomsignimage = pygame.image.load(os.path.join("images/blacksmith/wood sign.png")).convert_alpha()
roomsignimage = pygame.transform.scale(roomsignimage, (screen_width/4, screen_height/4))

menu_box_surface = pygame.Surface((screen_width/5, screen_height), pygame.SRCALPHA)
menu_box.fill((242, 225, 150, 128))  # RGBA, with alpha set to 128 (semi-transparent)


roomtitle_text = ["Emily's", "Inn &", "Tavern"]
def draw_roomtitle(screen, coinpurse, health, maxhealth):
    screen.blit(roomsignimage, (screen_width - (screen_width /4), 10))
    y = -screen_width/80
    for text in roomtitle_text:##THE drop shadow
        renderedtext = scrawlfont.render(text, True, (woodtan)) # White color
        text_width = renderedtext.get_width()
        room_width = roomtitle_rect.width
        x_offset = (room_width - text_width) // 2
        screen.blit(renderedtext, (roomtitle_rect.x + x_offset, roomtitle_rect.y + y))
        y += (screen_width/40)
        #print("I did it?")
    y = -screen_width/80-2
    for text in roomtitle_text:###The Main Text
        renderedtext = scrawlfont.render(text, True, ('black')) # White color
        text_width = renderedtext.get_width()
        room_width = roomtitle_rect.width
        x_offset = (room_width - text_width) // 2
        screen.blit(renderedtext, (roomtitle_rect.x + x_offset, roomtitle_rect.y + y))
        y += (screen_width/40)
        player_money = str(coinpurse)
        # print(player_money)
        moneytext = game_config.font.render(f'Your gold:{player_money}', True, (game_config.BLACK)) # White color
        screen.blit(moneytext, (screen_width*.85,screen_height *1.5/5,screen_width/5, screen_height/5))
        player_health = str(f'{health} / {maxhealth}')
        healthtext = game_config.font.render(f'Health:{player_health}', True, (game_config.BLACK)) # White color
        screen.blit(healthtext, (screen_width*.85, screen_height *1.75/5 , screen_width/5, screen_height/5))

# #tan
# roomtitle_owner = scrawlfont.render("Durom's", True, (90, 90, 40)) # White color
eat_rect = pygame.Rect((screen_width*.85), screen_height*.4, 180, 50)
sleep_rect = pygame.Rect((screen_width*.85), screen_height*.5, 180, 50)
inquire_rect = pygame.Rect((screen_width*.85),screen_height*.6, 180, 50)
leave_rect = pygame.Rect((screen_width*.85), screen_height*.75, 180, 50)
inn_buttons = [
    {"rect": eat_rect, "text": "Hot Meal - $5"},
    {"rect": sleep_rect, "text": "Bed & Meal - $10"},
    {"rect": inquire_rect, "text": "Inquire"},
    {"rect": leave_rect, "text": "Leave"}
]


button_color = (90, 90, 40)
def draw_inn(screen, inn_background_image, coinpurse, health, maxhealth):
        # Draw the background image
    screen.blit(inn_background_image, (0, 0))
        # Draw other HUD elements (buttons, titles)
    screen.blit(menu_box, (screen_width*4/5, ((screen_height/4)+10)))
    for button in inn_buttons:
        pygame.draw.rect(screen, button_color, button["rect"])   # Red color for demo
        text = fancyfont.render(button['text'], True, 'white')
        text_rect = text.get_rect(center = button['rect'].center)
        screen.blit(text, text_rect)
    draw_roomtitle(screen, coinpurse, health, maxhealth)
    # pygame.display.flip()      

####TOWN SQUARE
town_photos = 'images/town/backgrounds/'
town_background_dump = os.listdir(town_photos)

inn_rect = pygame.Rect((screen_width/4), 300, screen_width/5, 50)
blacksmith_rect = pygame.Rect((screen_width/5 *3 ), 300, screen_width/5, 50)
hunters_rect = pygame.Rect((screen_width/4), 450, screen_width/5, 50)
mages_rect = pygame.Rect((screen_width/5 *3), 450, screen_width/5, 50)
leave_rect = pygame.Rect((screen_width/4), 600, screen_width/5, 50)

town_buttons = [
    {"rect": inn_rect, "text": "Inn"},
    {"rect": blacksmith_rect, "text": "Blacksmith"},
    {"rect": hunters_rect, "text": "Hunter's Guild"},
    {"rect": mages_rect, "text": "Mage's Guild"},
    {"rect": leave_rect, "text": "Leave"}
]

def choose_town_background():
    town_png_files = [f for f in town_background_dump if os.path.isfile(os.path.join(town_photos, f)) and f.lower().endswith(('.png'))]
    if town_png_files:
        backgroud_file = random.choice(town_png_files)
    town_background_image = pygame.image.load(os.path.join("images/town/backgrounds", backgroud_file)).convert_alpha()
    town_background_image = pygame.transform.scale(town_background_image, (screen_width, screen_height))
    return town_background_image
def draw_town(screen, town_background_image):
        # Draw the background image
    screen.blit(town_background_image, (0, 0))
        # Draw other HUD elements (buttons, titles)
    screen.blit(menu_box, (screen_width-(250), ((screen_height/4)+10)))
    for button in town_buttons:
        pygame.draw.rect(screen, button_color, button["rect"])   # Red color for demo
        text = fancyfont.render(button['text'], True, 'white')
        text_rect = text.get_rect(center = button['rect'].center)
        screen.blit(text, text_rect)