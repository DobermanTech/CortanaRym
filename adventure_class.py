import pygame
import random
import game_config
import os


def determine_encounter(terrain, location_events, skills):
    event_dict = {}
    for location, events in location_events.items():
        event_dict[location] = events  # Direct assignment since events are already in tuple form
    
    # print(f'Location_Events: {event_dict}')
    
    events = event_dict.get(terrain, [])
    if not events:
        return "no events found"
    
    valid_events = [event for event in events if isinstance(event, tuple) and len(event) == 2]
    print(valid_events)
    if skills["Lumbering"] >0 and terrain == "forest": 
        valid_events.append(('find_trees', 5))
    print(valid_events)
    if not valid_events:
        return "no valid events found"
    
    event_names, event_weights = zip(*valid_events) if valid_events else ([], [])
    chosen_event = random.choices(event_names, weights=event_weights, k=1)
    
    return chosen_event[0] if chosen_event else None

def custom_print(*args, **kwargs):
    original_print(*args, **kwargs)
    message = ' '.join(map(str, args))
    game_config.log_message(message)
original_print = print
print = custom_print





def determine_enemy(player_pos, terrain, encounter_chance, level):
    # print(terrain["type"])
    
    encounterable = []
    
    for beast_name, beast_info in game_config.beasts_dict.items():
        # print(f'{beast_name},:::::: {beast_info}')
        if terrain["type"] in beast_info["env"]:
            if level >= beast_info["min_level"]:
                encounterable.append(beast_info)
    
    if encounterable:
        chosen_beast = random.choice(encounterable)
        print(f"Encountered a {chosen_beast["beastname"]} in the {terrain["type"]}")
        return chosen_beast["beastname"]
    else:
        print("No encounters available for this terrain.")
        return None

# Function to calculate neighbors for a given position
def calc_neighbors(pos):
    x, y = pos
    return [
        (x - 1, y), (x + 1, y),
        (x, y - 1), (x, y + 1),
        (x - 1, y-1), (x + 1, y+1),
        (x+1, y - 1), (x-1, y + 1)
    ]
def load_map_images(TERRAINS, UNIQUE_TERRAINS):
    for terrain in TERRAINS:
        if "image" in TERRAINS[terrain]:
            # print(f"Loading image for terrain: {terrain}, path: {TERRAINS[terrain]['image']}")
            TERRAINS[terrain]["image_surface"] = pygame.image.load(TERRAINS[terrain]["image"])

    for unique_terrain in UNIQUE_TERRAINS:
        if "image" in UNIQUE_TERRAINS[unique_terrain]:
            UNIQUE_TERRAINS[unique_terrain]["image_surface"] = pygame.image.load(UNIQUE_TERRAINS[unique_terrain]["image"])
        

# Function to update location based on player's position and visited grids
def update_location(player_pos, visited_grids, unique_locations):
    # print(unique_locations[tuple(player_pos)])
    if tuple(player_pos) in unique_locations and tuple(player_pos) not in visited_grids:
        visited_grids[tuple(player_pos)] = unique_locations[tuple(player_pos)]
        print(f'You found a unique Location: {unique_locations[tuple(player_pos)]}')
    elif tuple(player_pos) not in visited_grids and tuple(player_pos) not in unique_locations:
        neighbors = calc_neighbors(player_pos)
        neighbor_terrains = [visited_grids.get(neighbor, {}).get("type") for neighbor in neighbors]
        # print(f'not recognized location at {player_pos}')
        # Handle the case where no neighbors are found
        if not neighbor_terrains:
            # print(f"No neighbors found for {player_pos}")
            return
        
        weights = game_config.TERRAIN_WEIGHTS.copy()
        for terrain in neighbor_terrains:
            if terrain in weights:
                if terrain == 'meadow' or terrain == 'forest':
                    weights[terrain] *= 1.5  
                elif terrain == 'castle' or terrain == 'crypt':
                    weights[terrain] *= 0  

        terrain_type = random.choices(
            population=list(game_config.TERRAINS.keys()), 
            weights=list(weights.values())
        )[0]
        
        # Store the new location
        terrain_color = game_config.TERRAINS[terrain_type].get("color", (128, 128, 128)) # Use default gray color if not specified    
        visited_grids[tuple(player_pos)] = {"type": terrain_type}
        print(f'You discover a {terrain_type}')
        image_folder = os.path.join("images/landscape/", (terrain_type))
        # print(image_folder)
        image_background_dump = os.listdir(image_folder)
        # print(image_background_dump)
        backgroud_file = random.choice(image_background_dump)
        visited_grids[tuple(player_pos)]["background"] = backgroud_file

    else:
        terrain_type = visited_grids[tuple(player_pos)]["type"]
        print(f"This {terrain_type} looks familiar. You've been to {player_pos} before.")

    if tuple(player_pos) in unique_locations:
        location_details = unique_locations[tuple(player_pos)]
        print(f"Unique Location: {location_details}")
    # print(f'Update location funciton reporting player pos {player_pos}')
    return player_pos

def map_dimensions(screen_width, screen_height, region_x, region_y):
    #create the bounds of the map and region
    #calc map data
    mapXsize = 0.7 * screen_width
    mapYsize = 0.9 * screen_height  
    gridXsize = mapXsize / region_x
    gridYsize = mapYsize / region_y
    print(gridXsize, gridYsize)
    GRID_SIZE = (gridXsize, gridYsize)


# Update function to handle player movement
def update_player_position(player_pos, new_x, new_y, visited_grids, unique_locations, region_x, region_y):
    # Update player position if move is within bounds
    old_pos = tuple(player_pos)
    if 0 < new_x <= region_x and 0 < new_y <= region_y:
        player_pos = [new_x, new_y]
        # Ensure the neighbor exists in visited_grids before accessing its type
        neighbors = calc_neighbors(player_pos)
        for neighbor in neighbors:
            if neighbor not in visited_grids:
                # print(f"Neighbor {neighbor} not found in visited_grids.")
                continue
        # print(f"Moved from {old_pos} to {player_pos}")
        update_location(player_pos, visited_grids, unique_locations)

    else:
        print("Movement out of bounds")
        player_pos = old_pos
        print(f'Remaining at {player_pos}')
    return player_pos
class Adventure:
    def __init__(self, screen_width, screen_height):
        self.player_pos = [10, 10]
        # Initialize visited_grids as an empty dictionary
        self.visited_grids = {
        }
        self.portal_found = False

    def movement(self, player_pos, new_x, new_y):
        # new_x, new_y = (player_position)
        region_x = game_config.region_x
        region_y = game_config.region_y
        # print(f'You are at {player_position}')   #####THESE TWO ARE PASSING
        # print(f'Move Function to move to {new_x}, {new_y}. Send to Update Player position')
        attempted_location = update_player_position(self.player_pos, new_x, new_y, self.visited_grids, game_config.UNIQUE_LOCATIONS, region_x, region_y)
        # print(f'recieve from updatePlayerPosition function reporting player pos {attempted_location}')
        if attempted_location is not None:
            self.player_pos = attempted_location
        else:
            pass
            # print(f'Error caught with invalid player position. could not go to {attempted_location}. staying at {player_pos}')
        # print(f'movment function returning {self.player_pos}')
        return self.player_pos
    
    def calculate_exp_to_next_level(self):
        return self.level ** 2 * 10

    def gain_exp(self, amount):
        self.exp += amount
        print(f"{self.name} gained {amount} XP!")
        self.check_level_up()

    def check_level_up(self):
        while self.exp >= self.exp_to_next_level:
            self.exp -= self.exp_to_next_level
            self.level += 1
            self.exp_to_next_level = self.calculate_exp_to_next_level()
            print(f"Level up! {self.name} is now level {self.level}!")
        else:()
           # print(f'You have {self.exp_to_next_level} exp to next level')
    
    def display_status(self):
        print(f"{self.name} - Level: {self.level}, XP: {self.exp}/{self.exp_to_next_level}")
    # def attack(self, current_weapon):
    #     game_config.custom_print("You chose to attack!")  # Debug print
    #     calc_hit = random.randint(1, 100)
    #     hit_chance = current_weapon["hitChance"]
    #     min_damage = current_weapon["min_damage"]
    #     max_damage = current_weapon["max_damage"]
    #     if calc_hit <= hit_chance:
    #         calc_damage = random.randint(min_damage, max_damage)
    #         print(f"Adventure_class attack:You dealt {calc_damage} damage!")  # Debug print
    #         return calc_damage
    #     else:
    #         print("You missed the target!")
    #         return 0
        

    def draw_adventure(self, screen, adventure_buttons, visited_grids, player_pos):
        # Draw the adventure screen
# Draw the new background
        local_terrain = self.visited_grids[tuple(self.player_pos)]["type"]
        try:
            env_image = visited_grids[tuple(player_pos)]["background"]
            # print(f'ENV_IMAGE: {env_image}')
            
            # Ensure the correct path is used
            image_path = os.path.join("images", "landscape", local_terrain, env_image)
            # print(f'IMAGE_PATH: {image_path}')
            
            background_image = pygame.image.load(image_path).convert_alpha()
            game_config.screen.blit(background_image, (0, 0))
            
        except FileNotFoundError as e:
            print(f'FileNotFoundError: {e}')
        except pygame.error as e:
            print(f'PygameError: {e}')
        except KeyError as e:
            print(f'KeyError: {e}')
        except Exception as e:
            print(f'Unexpected Error: {e}')

#Draw Adventure buttons

        loaded_buttons = adventure_buttons
        wood_available = visited_grids[tuple(player_pos)].get("trees",0) 
        if wood_available>0:
            # print("I HAS TREES")
            loaded_buttons.append(game_config.chop_wood_button)
        for button in loaded_buttons:
            pygame.draw.rect(screen, button["color"], button["rect"])
            text_surface = game_config.font.render(button["text"], True, game_config.WHITE)  # Create text surface
            text_rect = text_surface.get_rect(center=button["rect"].center)  # Center text on button
            screen.blit(text_surface, text_rect)
            #print(button["text"])
        terrain_box = pygame.draw.rect(screen, game_config.lighttan, (int(game_config.screen_width/4), 20, int(game_config.screen_width/2), 60))

        my_region = game_config.get_region(self.player_pos)
        terrain_text = game_config.font.render(f'{local_terrain} in the {my_region}', True, game_config.WHITE)
        terrain_text_rect = terrain_text.get_rect(center=terrain_box.center)
        screen.blit(terrain_text, terrain_text_rect)

        #Lumberjack's button





#draw the new background

    def draw_menu_nav_buttons(self, screen, menu_buttons, mode_flags, mode):
        # print(f'Adventuring: {}')
        for button in menu_buttons:
            # print(button["text"])
            if mode_flags[mode.ON_ADVENTURE] and button["text"].lower() =="close":
                continue
            pygame.draw.rect(screen, button["color"], button["rect"])
            text_surface = game_config.font.render(button["text"], True, game_config.WHITE)  # Create text surface
            text_rect = text_surface.get_rect(center=button["rect"].center)  # Center text on button
            screen.blit(text_surface, text_rect)
            #print(button["text"])




def draw_map(player_pos, visited_grids, screen, screen_width, screen_height, GRID_SIZE, TERRAINS, UNIQUE_TERRAINS):
    backgroundimage = pygame.image.load('images/map icons/map background.png').convert_alpha()
    backgroundimage = pygame.transform.scale(backgroundimage, (screen_width * 1.2, screen_height * 1.2))
    # Define the grid region

    GRID_REGION_TOP_LEFT = (int(game_config.screen_width/5), 100)
    GRID_REGION_SIZE = (int(screen_width * .75), screen_height - 200)

# Load images for castles and crypts
# Fill the window with white
    screen.fill('gray')
    screen.blit(backgroundimage, ((-0.1*screen_width), (-.1*screen_height)))
    # Draw the grid
    for x in range(GRID_REGION_TOP_LEFT[0], GRID_REGION_TOP_LEFT[0] + GRID_REGION_SIZE[0], GRID_SIZE):
        for y in range(GRID_REGION_TOP_LEFT[1], GRID_REGION_TOP_LEFT[1] + GRID_REGION_SIZE[1], GRID_SIZE):
            rect = pygame.Rect(x, y, GRID_SIZE, GRID_SIZE)
            grid_pos = ((x - GRID_REGION_TOP_LEFT[0]) // GRID_SIZE, (y - GRID_REGION_TOP_LEFT[1]) // GRID_SIZE)
            if grid_pos in visited_grids:
                terrain_info = visited_grids[grid_pos]
                terrain_type = terrain_info["type"]
                # Only draw the portal if found
                # if terrain_info["type"] == "magic portal" and not portal_found:
                #     continue
                # Draw the image for castles and crypts
                if terrain_info["type"] in ["castle", "swamp"]:
                    screen.blit(pygame.transform.scale(TERRAINS[terrain_info["type"]]["image_surface"], (GRID_SIZE, GRID_SIZE)), rect)
                else:
                    # print(f'filling {terrain_info}')
                    # print(terrain_info['type'])
                    tile_color = TERRAINS.get(terrain_type, {}).get("color", (128, 128, 128)) # Default color if not found                    # print(tile_color)
                    pygame.draw.rect(screen, tile_color, rect)
            #pygame.draw.rect(window, (0, 0, 0), rect, 1)

    # Draw the player
    player_rect = pygame.Rect(player_pos[0] * GRID_SIZE + GRID_REGION_TOP_LEFT[0], player_pos[1] * GRID_SIZE + GRID_REGION_TOP_LEFT[1], GRID_SIZE, GRID_SIZE)
    pygame.draw.rect(screen, (0, 0, 0), player_rect)

    # #draw the bag close button
    # for button in game_config.map_buttons:
    #     pygame.draw.rect(screen, button["color"], button["rect"])
    #     text_surface = game_config.font.render(button["text"], True, game_config.WHITE)  # Create text surface
    #     text_rect = text_surface.get_rect(center=button["rect"].center)  # Center text on button
    #     screen.blit(text_surface, text_rect)
    #     #print(button["text"])
    # Update the display
    # pygame.display.flip()


#wierd