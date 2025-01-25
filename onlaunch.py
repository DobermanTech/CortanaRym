import game_config
import sys
from game_config import pygame, screen

game_config.check_and_install_packages()
pygame.display.set_caption('CortanaRym V 0.5')

# Function to check for save file
def check_for_save_file():
    try:
        with open('savegame.pkl', 'rb') as file:
            game_state = game_config.pickle.load(file)
            player_level = game_state['player'].level
            current_weapon = game_state['player'].current_weapon.name
            return True, player_level, current_weapon
    except FileNotFoundError:
        return False, None, None

save_file_found, player_level, current_weapon = check_for_save_file()

# Define button parameters (you may need to define Y/N_buttons elsewhere in your code)
load_button = {"text": "Load", "rect": pygame.Rect(game_config.screen_width/3, 200, game_config.screen_width/3, 90)}
new_button = {"text": "New", "rect": pygame.Rect(game_config.screen_width/3, 400, game_config.screen_width/3, 90)}
Y_N_buttons = [load_button, new_button]

splash_image_filename = "images/splashscreen.png"
splash_image = pygame.image.load(splash_image_filename)
splash_image = pygame.transform.scale(splash_image, (game_config.screen_width, game_config.screen_height))
load_decide = True
while load_decide:
    screen.fill(game_config.BLACK)
    game_config.screen.blit(splash_image, (0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in Y_N_buttons:
                if button["rect"].collidepoint(event.pos):                
                    action = button["text"].lower()
                    if action == "load":
                        # Load the game here
                        load = True
                        player_instance, my_adventure, player_weapon_bag = game_config.load_game('savegame.pkl')
                        load_decide = False  # Exit the initialize screen
                    elif action == "new":
                        # Start a new game here
                        load = False
                        load_decide = False  # Exit the initialize screen

    # Display messages based on save file presence
    if save_file_found:
        # Draw the text "Found Save File Level X wielding a Y"
        font = pygame.font.Font(None, 36)
        shadowtext = font.render(f"Found Save File: Level {player_level} wielding a {current_weapon}", True, game_config.BLACK)
        text = font.render(f"Found Save File: Level {player_level} wielding a {current_weapon}", True, game_config.WHITE)
        screen.blit(shadowtext, ((game_config.screen_width/3) +2, 102))
        screen.blit(shadowtext, (game_config.screen_width/3, 99))       
        screen.blit(text, (game_config.screen_width/3, 100))
        for button in Y_N_buttons:
            pygame.draw.rect(screen, game_config.WHITE, button["rect"])
            text_surface = font.render(button["text"], True, game_config.BLACK)
            text_rect = text_surface.get_rect(center=button["rect"].center)
            screen.blit(text_surface, text_rect)
    else:
        # Draw the text "No Save File Found"
        font = pygame.font.Font(None, 36)
        text = font.render("No Save File Found", True, game_config.WHITE)
        screen.blit(text, (100, 100))

        # Draw the new game button
        pygame.draw.rect(screen, game_config.WHITE, new_button["rect"])
        newgame_surface = font.render(new_button["text"], True, game_config.BLACK)
        newgame_rect = newgame_surface.get_rect(center=new_button["rect"].center)
        screen.blit(newgame_surface, newgame_rect)

    pygame.display.flip()  # Update the display
