
import os
import pygame
import game_config
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
global weapon_positions, images
bagimage_size = (100, 100)
font = pygame.font.Font(None, 32)
small_font = pygame.font.Font(None, 24)

def draw_weapon_bag(player_weapon_bag, screen, bagimage_size, weapon_dict, player_instance):
    images = []
    weapon_positions = []  # Store positions and names of weapons
    weapon_image_folder = "images"
    
    for idx, weapon_instance in enumerate(player_weapon_bag):
        # print(weapon_instance)
        try:
            weapon_name = weapon_instance.name  # Access the name attribute directly
            image_name = f"{weapon_name}.png"  # Construct the image filename
            image_path = os.path.join(weapon_image_folder, image_name)  # Construct the full path
            # print(f"Loading image from path: {image_path}")
            if not os.path.isfile(image_path):
                raise FileNotFoundError(f"File not found: {image_path}")

            image = pygame.image.load(image_path)
            scaled_image = pygame.transform.scale(image, bagimage_size)  # Rescale the image
            images.append(scaled_image)

            row = idx // 4
            col = idx % 4
            x = col * (bagimage_size[0] + 50) + (game_config.screen_width/5)  # Adjust spacing between images
            y = row * (bagimage_size[1] + 75) + 50  # Adjust spacing between images
            weapon_positions.append({"rect": pygame.Rect(x, y, bagimage_size[0], bagimage_size[1]), "instance": weapon_instance, "name": weapon_name})
            # print(f"weapon image loaded:{weapon_name}")       
        
        except KeyError:
            print(f"Weapon '{weapon_name}' not found in weapon dictionary.")
        except FileNotFoundError as fnf_error:
            print(fnf_error)
        except pygame.error as e:
            print(f"Unable to load image for weapon '{weapon_name}': {e}")

    for idx, weapon_info in enumerate(weapon_positions):
        x = weapon_info["rect"].x
        y = weapon_info["rect"].y

        # Highlight the currently equipped weapon
        if weapon_info["instance"] == player_instance.current_weapon:
            pygame.draw.rect(screen, GREEN, (x - 5, y - 5, bagimage_size[0] + 10, bagimage_size[1] + 10), 2)

        # Draw weapon image
        if idx < len(images):
            screen.blit(images[idx], (x, y))

        # Draw weapon stats
        weapon_name = weapon_info["name"]
        weapon = weapon_dict[weapon_name]
        text = small_font.render(f"{weapon_name}", True, BLACK)
        screen.blit(text, (x, y + bagimage_size[1] + 10))
        text = small_font.render(f"Damage: {weapon['min_damage']}-{weapon['max_damage']}", True, BLACK)
        screen.blit(text, (x, y + bagimage_size[1] + 30))
        text = small_font.render(f"Hit Chance: {weapon['hitChance']}", True, BLACK)
        screen.blit(text, (x, y + bagimage_size[1] + 50))


    return weapon_positions, images
