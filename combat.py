import pygame
import random
import game_config
from game_config import screen_width, screen_height
import time
import os

# Beasts
def custom_print(*args, **kwargs):
    original_print(*args, **kwargs)
    message = ' '.join(map(str, args))
    game_config.log_message(message)
original_print = print
print = custom_print

# Beasts
def draw_combat_buttons(screen, combat_buttons):
    for button in combat_buttons:
        pygame.draw.rect(screen, button["color"], button["rect"])
        text_surface = game_config.font.render(button["text"], True, game_config.WHITE)  # Create text surface
        text_rect = text_surface.get_rect(center=button["rect"].center)  # Center text on button
        screen.blit(text_surface, text_rect)


def draw_combat_hud(screen, player_instance, my_adventure, opponent):
    screen_width = screen.get_width()
    local_terrain = my_adventure.visited_grids[tuple(my_adventure.player_pos)]["type"]
    env_image = my_adventure.visited_grids[tuple(my_adventure.player_pos)]["background"]
    image_path = os.path.join("images", "landscape", local_terrain, env_image)
    background_image = pygame.image.load(image_path).convert_alpha()
    game_config.screen.blit(background_image, (0, 0))
#player
    player_health_ratio = max(player_instance.health / player_instance.maxhealth, 0)  # Ratio of current health to max health
    player_health_bar_width = int(player_health_ratio * game_config.screen_width/3)  # Width of the health bar based on health ratio
    pygame.draw.rect(screen, (0,0,0), (10, 55, (game_config.screen_width/3), 50), 5)  # Draw border around health bar
    pygame.draw.rect(screen, (255, 0, 0), (10, 60, player_health_bar_width, 40))  # Draw player's health bar
#player "sprite"
    adv_player_image = pygame.transform.scale(game_config.player_image, (game_config.screen_width/7, game_config.screen_height/3))
    player_xy = game_config.screen_width/5, game_config.screen_height/3
    player_rect = game_config.player_image.get_rect(topleft = player_xy)
    game_config.screen.blit(adv_player_image, player_rect.topleft)

#Opponent
    opponent_health_ratio = max(opponent.health / opponent.maxhealth, 0)  # Ratio of current health to max health for opponent
    opponent_health_bar_width = int(opponent_health_ratio * screen_width /3)  # Width of the opponent health bar
    pygame.draw.rect(screen, (0,0,0), (screen_width *2/3 - 15, 55, screen_width/3 + 10, 50), 5)  # Draw border around opponent's health bar
    pygame.draw.rect(screen, (255, 0, 0), (screen_width * 2/3 -10, 60, opponent_health_bar_width, 40))  # Draw opponent's health bar
#opponent "sprite"


# Optional: Display health text
    font = pygame.font.Font(None, 36)
    player_health_text = font.render(f'{player_instance.health}/{player_instance.maxhealth}', True, (0,0,0))
    screen.blit(player_health_text, (screen_width/9, 75))
    opponent_health_text = font.render(f'{opponent.health}/{opponent.maxhealth}', True, (0,0,0))
    screen.blit(opponent_health_text, (screen_width *2/3, 75))
    enemy_name = font.render(f'{opponent.name}', True, (255, 255, 250))
    enemy_name_dshadow = font.render(f'{opponent.name}', True, (0,0,0))
    screen.blit(enemy_name_dshadow, (screen_width *2/3-2, 32))
    screen.blit(enemy_name, (screen_width *2/3, 30))





def turn_based_combat(player_instance, my_adventure, opponent, current_weapon, visited_grids, player_pos):
    game_config.screen.fill((255,255,255))
    draw_combat_hud(game_config.screen, player_instance, my_adventure, opponent)
    game_config.draw_message_log(game_config.screen)
    # my_adventure.draw_adventure(game_config.screen, game_config.adventure_buttons, my_adventure.visited_grids, my_adventure.player_pos)

    if opponent.health > 0 and player_instance.health > 0:
        # print(current_weapon)
        outcome = player_turn(player_instance, my_adventure, opponent, current_weapon)
        game_config.screen.fill((255,255,255))
        draw_combat_hud(game_config.screen, player_instance, my_adventure, opponent)
        game_config.draw_message_log(game_config.screen)
        pygame.display.flip()
        if outcome == "victory":
              return "victory" # End combat if player wins
        effects(player_instance, my_adventure, opponent)
        if opponent.health <= 0:
            return "victory"  # Exit if opponent is defeated
        game_config.pause(300)
        hostile_turn(player_instance, my_adventure, opponent)
        if player_instance.health <= 0:
            print("You were defeated!")
            return "Defeat"  # Exit if player is defeated




def player_turn(player_instance, my_adventure, opponent, current_weapon):
    damage = player_instance.attack(current_weapon)
    icon_xy = (screen_width * 0.85, screen_height * 1.75 / 5)
    if damage > opponent.health:
        damage = opponent.health
    if damage != 0:
        print(f'You deal {damage} damage.')
        damage_display = game_config.BIG_font.render(f'{damage}', True, (game_config.BLACK)) # Red color
        text_rect = damage_display.get_rect()
        splat_rect = game_config.hitsplat_image.get_rect(center=icon_xy)
        game_config.screen.blit(game_config.hitsplat_image, splat_rect.topleft)
        text_rect.center = splat_rect.center
        game_config.screen.blit(damage_display, text_rect.topleft)

    else:
        print("You missed")
        damage_display = game_config.BIG_font.render('Miss', True, (game_config.BLACK)) # Red color
        text_rect = damage_display.get_rect(center = icon_xy)
        game_config.screen.blit(damage_display, text_rect.topleft)
    opponent.health -= damage
    pygame.display.flip()
    # time.sleep(.7)
    game_config.pause(500)
    # print(f'{opponent.name} has {opponent.health} health left.')
    if opponent.health < 1:
        print(f'You defeated {opponent.name}!')
        player_instance.gain_exp(opponent.xp)
        random_money_gained = random.randint(0,2)
        leveled_money_gained = random.randint(0, opponent.min_level)
        money_gained = random_money_gained + leveled_money_gained
        player_instance.coinpurse += money_gained
        print(f'You found {money_gained} bringing your total to {player_instance.coinpurse}')
        player_instance.display_status()
        return "victory"
def effects(player_instance, my_adventure, opponent):
    # opponent.health += 1
    pass
def hostile_turn(player_instance, my_adventure, opponent):
    retort_damage = opponent.attack()
    player_instance.health -= retort_damage
    # print(retort_damage)

    game_config.screen.fill(game_config.WHITE)
    draw_combat_hud(game_config.screen, player_instance, my_adventure, opponent)
    game_config.draw_message_log(game_config.screen)
    damage_display = game_config.BIG_font.render(f'{retort_damage}', True, (game_config.BLACK)) # Red color
    text_rect = damage_display.get_rect()
    icon_xy = (screen_width * 0.28, screen_height * 2.1 / 5)
    splat_rect = game_config.hitsplat_image.get_rect(center=icon_xy)
    game_config.screen.blit(game_config.hitsplat_image, splat_rect.topleft)
    text_rect.center = splat_rect.center
    game_config.screen.blit(damage_display, text_rect.topleft)
    pygame.display.flip()

    # time.sleep(.7)
    game_config.pause(500)


class Enemy:
    def __init__(self, name, beasts_dict):
        self.name = name
        self.health = beasts_dict['health']
        self.maxhealth = beasts_dict['health']
        self.min_retort = beasts_dict['min_damage']
        self.max_retort = beasts_dict['max_damage']
        self.xp = beasts_dict['xp']
        self.min_level = beasts_dict['min_level']

    def attack(self):
        retort = random.randint(self.min_retort, self.max_retort)
        print(f'{self.name} attacks back for {retort} damage.')  # Debug print
        return retort

# def combat(player_instance, hostile, current_weapon):
#     print(f'You vs {hostile.name}. {hostile.name} has {hostile.health} health. You are armed with a {player_instance.current_weapon}.')
#     while in_combat:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 exit()
#             elif event.type == pygame.MOUSEBUTTONDOWN:
#                 for button in game_config.combat_buttons:
#                     if button["rect"].collidepoint(event.pos):
#                         action = button["text"].lower()
#                         print(action)
#                         if action == "attack":
#                             damage = player_instance.attack(current_weapon)
#                             print(f'You deal {damage} damage.')
#                             hostile.health -= damage
#                             print(f'{hostile.name} has {hostile.health} health left.')
#                             if hostile.health < 1:
#                                 print(f'You defeated {hostile.name}!')
#                                 in_combat = False
#                                 player_instance.gain_exp(hostile.xp)
#                                 player_instance.display_status()
#                                 break
#                         elif action == "run away":
#                             print("You flee.")
#                             in_combat = False
#                             break
#                         # time.sleep(0.5)
#                         if in_combat:
#                             hostile.attack()

#         for button in combat_buttons:
#             pygame.draw.rect(screen, button["color"], button["rect"])
#             screen.blit(button["text_surface"], button["text_rect"])

