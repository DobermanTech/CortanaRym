import pygame
import random
import game_config
import time
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
#player
    player_health_ratio = max(player_instance.health / player_instance.maxhealth, 0)  # Ratio of current health to max health
    player_health_bar_width = int(player_health_ratio * game_config.screen_width/3)  # Width of the health bar based on health ratio
    pygame.draw.rect(screen, (0,0,0), (10, 55, (game_config.screen_width/3), 50), 5)  # Draw border around health bar
    pygame.draw.rect(screen, (255, 0, 0), (10, 60, player_health_bar_width, 40))  # Draw player's health bar

#Opponent
    opponent_health_ratio = max(opponent.health / opponent.maxhealth, 0)  # Ratio of current health to max health for opponent
    opponent_health_bar_width = int(opponent_health_ratio * screen_width /3)  # Width of the opponent health bar
    pygame.draw.rect(screen, (0,0,0), (screen_width *2/3 - 15, 55, screen_width/3 + 10, 50), 5)  # Draw border around opponent's health bar
    pygame.draw.rect(screen, (255, 0, 0), (screen_width * 2/3 -10, 60, opponent_health_bar_width, 40))  # Draw opponent's health bar

# Optional: Display health text
    font = pygame.font.Font(None, 36)
    player_health_text = font.render(f'{player_instance.health}/{player_instance.maxhealth}', True, (0,0,0))
    screen.blit(player_health_text, (screen_width/9, 75))
    opponent_health_text = font.render(f'{opponent.health}/{opponent.maxhealth}', True, (0,0,0))
    screen.blit(opponent_health_text, (screen_width *2/3, 75))





def turn_based_combat(player_instance, my_adventure, opponent, current_weapon):
    if opponent.health > 0 and player_instance.health > 0:
        # print(current_weapon)
        outcome = player_turn(player_instance, my_adventure, opponent, current_weapon)
        if outcome == "victory":
              return "victory" # End combat if player wins
        effects(player_instance, my_adventure, opponent)
        if opponent.health <= 0:
            return "victory"  # Exit if opponent is defeated
        hostile_turn(player_instance, my_adventure, opponent)
        if player_instance.health <= 0:
            print("You were defeated!")
            return "Defeat"  # Exit if player is defeated

def player_turn(player_instance, my_adventure, opponent, current_weapon):
    damage = player_instance.attack(current_weapon)
    if damage != 0:
        print(f'You deal {damage} damage.')

    else:
        print("You missed")
    opponent.health -= damage
    game_config.screen.fill((255,255,255))
    draw_combat_hud(game_config.screen, player_instance, my_adventure, opponent)
    game_config.draw_message_log(game_config.screen)
    pygame.display.flip()
    time.sleep(.7)
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
    pygame.display.flip()
    time.sleep(.7)


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

