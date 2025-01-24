import os
import pygame
import os
import weapon_class
import random
import time
import game_config

player_level = 4
default_timer = 6
# screen_width, screen_height = 1280, 1024
from game_config import screen_width, screen_height
game_data = "game_data(recursive dic).txt"
blacksmith_photos = 'images/blacksmith/backgrounds/'
pygame.font.init()
fancyfont = pygame.font.SysFont("serif", 30)
scrawlfont = pygame.font.SysFont('segoescript', 32)
darktan = (90, 40, 40)
lighttan = (220, 190, 90)
dropshadow_color = (50, 0, 0)
roso= (150, 15, 15)
woodtan = (196, 155, 99)


#in_blacksmith = True
#Define the hud elements


#randomly choose a background
background_dump = os.listdir(blacksmith_photos)
png_files = [f for f in background_dump if os.path.isfile(os.path.join(blacksmith_photos, f)) and f.lower().endswith(('.png'))]
if png_files:
     backgroud_file = random.choice(png_files)
background_image = pygame.image.load(os.path.join("images/blacksmith/backgrounds", backgroud_file)).convert_alpha()
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
menu_box = pygame.Surface((screen_width - 250, screen_height), pygame.SRCALPHA)
roomtitle_rect = pygame.Rect((screen_width - (0.22 * screen_width)), 95, 240, 200)
#load and locate the sign
roomsignimage = pygame.image.load(os.path.join("images/blacksmith/wood sign.png")).convert_alpha()
roomsignimage = pygame.transform.scale(roomsignimage, (screen_width/4, screen_height/4))

menu_box_surface = pygame.Surface((250, screen_height), pygame.SRCALPHA)
menu_box.fill((242, 225, 150, 128))  # RGBA, with alpha set to 128 (semi-transparent)

#Drop Shadow
roomtitle_text = ["Durom's", "Blacksmith", "Shop"]
def draw_roomtitle(screen):
    screen.blit(roomsignimage, (screen_width - (screen_width /4), 10))
    y = 0
    for text in roomtitle_text:##THE drop shadow
        renderedtext = scrawlfont.render(text, True, (woodtan)) # White color
        text_width = renderedtext.get_width()
        room_width = roomtitle_rect.width
        x_offset = (room_width - text_width) // 2
        screen.blit(renderedtext, (roomtitle_rect.x + x_offset, roomtitle_rect.y + y))
        y += 50
        #print("I did it?")
    y = -2
    for text in roomtitle_text:###The Main Text
        renderedtext = scrawlfont.render(text, True, ('black')) # White color
        text_width = renderedtext.get_width()
        room_width = roomtitle_rect.width
        x_offset = (room_width - text_width) // 2
        screen.blit(renderedtext, (roomtitle_rect.x + x_offset, roomtitle_rect.y + y))
        y += 50
# #tan
# roomtitle_owner = scrawlfont.render("Durom's", True, (90, 90, 40)) # White color

browse_rect = pygame.Rect((screen_width -200), 300, 180, 50)
present_rect = pygame.Rect((screen_width -200), 375, 180, 50)
inquire_rect = pygame.Rect(screen_width -200, 450, 180, 50)
leave_rect = pygame.Rect((screen_width -200), 625, 180, 50)
blacksmith_buttons = [
    {"rect": browse_rect, "text": "Browse"},
    {"rect": present_rect, "text": "Present"},
    {"rect": inquire_rect, "text": "Inquire"},
    {"rect": leave_rect, "text": "Leave"}
]


button_color = (90, 90, 40)


#if the weapon bag is empty and


# Define the timers using the default value
blacksmith_examine_timer = default_timer
blacksmith_inquire_timer = default_timer
blacksmith_restock_timer = default_timer
# Create a list of timers
timers = {
    "blacksmith_restock_timer" : 6,
    'blacksmith_examine_timer' :20,
    'blacksmith_inquire_timer' :10
}
weaponshop = []
shopslots = 8
#if the weapon bag is empty and the timer is at 0
def weapon_restock():
    weaponshop.clear()
    for i in range(shopslots):
        weaponshop.append(weapon_class.Weapon.create_random_weapon())
        print('working?')
        print(weaponshop)

sell_rect = pygame.Rect((screen_width/3), screen_height *.4, 180, 50)
sell_text = game_config.font.render("Sell", True, (game_config.BLACK))
sell_button = (sell_rect, sell_text)

nevermind_rect = pygame.Rect(int(screen_width*.55), screen_height *.4, 180, 50)
nevermind_text = game_config.font.render("Nevermind", True, (game_config.BLACK))
nevermind_button = (nevermind_rect, nevermind_text)

def sell_weapon(self, weapon):
    print(weapon)
    popup_box = pygame.Surface((screen_width/2, screen_height/2), pygame.SRCALPHA)
    popup_box.fill((242, 225, 150, 192))  # RGBA, with alpha set to 128 (semi-transparent)
    game_config.screen.blit(popup_box, (screen_width*.25, screen_height*.25,))
    if weapon.value < 1000:
        # offer value only
        options_text = game_config.font.render(f"Your {weapon.name} isn't worth much. I'll give you {weapon.value} for it.", True, (game_config.BLACK))
        selecting = True
        while selecting:
            game_config.screen.blit(options_text, (screen_width*.35, screen_height *2/5-60, screen_width/5, screen_height/5))
            pygame.draw.rect(game_config.screen, button_color, sell_rect)
            pygame.draw.rect(game_config.screen, button_color, nevermind_rect)

            # Blit text onto the buttons
            game_config.screen.blit(sell_text, (sell_rect.x + (sell_rect.width - sell_text.get_width()) // 2, sell_rect.y + (sell_rect.height - sell_text.get_height()) // 2))
            game_config.screen.blit(nevermind_text, (nevermind_rect.x + (nevermind_rect.width - nevermind_text.get_width()) // 2, nevermind_rect.y + (nevermind_rect.height - nevermind_text.get_height()) // 2))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if sell_rect.collidepoint(event.pos):
                        print(f'weapon sold')
                        selecting = False
                        return "sell"
                    if nevermind_rect.collidepoint(event.pos):
                        print(f'OK, keep your {weapon.name}')
                        selecting = False
                        return
            pygame.display.flip()


def draw_blacksmith(screen):
        # Draw the background image
    screen.blit(background_image, (0, 0))
        # Draw other HUD elements (buttons, titles)
    screen.blit(menu_box, (screen_width-(250), ((screen_height/4)+10)))
    for button in blacksmith_buttons:
        pygame.draw.rect(screen, button_color, button["rect"])   # Red color for demo
        text = fancyfont.render(button['text'], True, 'white')
        text_rect = text.get_rect(center = button['rect'].center)
        screen.blit(text, text_rect)
    draw_roomtitle(screen)


    # pygame.display.flip()
