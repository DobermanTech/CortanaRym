import random
import game_config
import pygame
import weapon_class

class Player:
    def __init__(self, name, weapon_dict):
        self.name = name
        self.health = 100
        self.level = 1
        self.exp = 0
        self.exp_to_next_level = self.calculate_exp_to_next_level()
        self.maxhealth = 100 + (5 * self.level)
        self.coinpurse = 50
        self.wood = 0
        self.stone = 0

        # Define the default weapon name
        default_weapon_name = 'fists'
        
        # Check if the default weapon is in the weapon_dict
        if default_weapon_name in weapon_dict:
            # Set default weapon data when creating a weapon
            self.current_weapon = weapon_class.Weapon.create_weapon({
                'name': default_weapon_name,
                **weapon_dict[default_weapon_name]  # Merge default weapon data
            })
        else:
            raise ValueError(f"Weapon '{default_weapon_name}' not found in weapon dictionary")

        self.skills = {
            "Long Blade":1,
            "Short Blade":1,
            "Choppers":1,
            "Polearms":1,
            "Ranged":1,
            "Blunt":1,
            "Tracker":0,
            "Scout":0,
            "Lumbering":2,
            "Mining":0,
            "Builder":0,
            "Gathering":0,
            "Treasure Hunter":0,
            "Leadership":0
        }
        self.skill_xp = {
            "Long Blade": 6,
            "Short Blade": 0,
            "Choppers": 1,
            "Polearms": 4,
            "Ranged": 9,
            "Blunt": 14
        }

    def add_skill_xp(self, skill, xp_amount):

        skill_capitalized = " ".join(word.capitalize() for word in skill.split())
        skill = skill_capitalized
        self.skill_xp[skill] += xp_amount  # Add XP to the skill
        current_level = self.skills[skill]  # Get current level of the skill
        next_level = current_level + 1  # Calculate the next level
        xp_threshold = current_level **(1+(current_level*.02)) *35
        # Check if XP is enough for the next level
        if self.skill_xp[skill] >= xp_threshold:
            self.skills[skill] = next_level  # Level up the skill
            self.skill_xp[skill] -= xp_threshold  # Deduct XP used for leveling up
            
            print(f"{skill} leveled up to {next_level}!")
        else:
            print(f"{xp_amount} XP added to {skill}. Current level: {current_level}.")




        
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
            self.maxhealth +=5
            self.exp_to_next_level = self.calculate_exp_to_next_level()
            print(f"Level up! {self.name} is now level {self.level}!")
        else:
           print(f'You have {self.exp_to_next_level} exp to next level')
    
    def display_status(self):
        print(f"{self.name} - Level: {self.level}, XP: {self.exp}/{self.exp_to_next_level}")

    def attack(self, current_weapon):
        # print(f"You attack with a {current_weapon}!")  # Debug print
        calc_hit = random.randint(1, 100)
        hit_chance = current_weapon.hitChance
        min_damage = current_weapon.min_damage
        max_damage = current_weapon.max_damage
        # print(min_damage, max_damage)
        if calc_hit <= hit_chance:
            print(current_weapon)
            print(current_weapon.weapon_type)
            calc_damage = random.randint(min_damage, max_damage) + self.skills[current_weapon.weapon_type.title()]
            # print(f"PLAYER_CLASS: You dealt {calc_damage} damage!")  # Debug print
            self.add_skill_xp(current_weapon.weapon_type, calc_damage)
            return calc_damage
        else:
            # print("You missed the target!")
            return 0
    def draw_player_stats(self, screen, screen_width, screen_height):
        
        screen.fill((0, 0, 40))  # Dark blue background
        backgroundimage = pygame.image.load('images/map icons/map background.png').convert_alpha()
        backgroundimage = pygame.transform.scale(backgroundimage, (game_config.screen_width * 1.2, game_config.screen_height * 1.2))
        screen.blit(backgroundimage, ((-0.1*game_config.screen_width), (-.1*game_config.screen_height)))

        y_offset = screen_height / 5
        x_offset = screen_width / 4
        x_pos = 1
        
        box_width = screen_width * 0.1875 - 20  # Fixed width for each box
        box_height = 80  # Fixed height for each box
        progress_bar_height = 10  # Height of the progress bar
        
        for skill, level in self.skills.items():
            text = game_config.font.render(f"{skill}: {level}", True, game_config.BLACK)
            text_rect = text.get_rect(center=(x_offset + box_width // 2, y_offset + box_height // 2))
            box_rect = pygame.Rect(x_offset, y_offset, box_width, box_height)
            
            pygame.draw.rect(screen, game_config.lighttan, box_rect)  # Draw the fixed size box
            screen.blit(text, text_rect)  # Blit the text in the center of the box
            current_xp = self.skill_xp.get(skill, 0) # Calculate progress
            xp_to_next_level = (self.skills[skill] ** 1.5) * 20
            progress = current_xp / xp_to_next_level if xp_to_next_level > 0 else 0
            progress_bar_rect = pygame.Rect(        # Draw progress bar
                x_offset,
                y_offset + box_height,
                int(box_width * progress),
                progress_bar_height
            )
            pygame.draw.rect(screen, game_config.lighttan, (x_offset, y_offset + box_height, box_width, progress_bar_height))  # Background bar
            pygame.draw.rect(screen, game_config.GREEN, progress_bar_rect)  # Progress bar
            x_offset += box_width + 20  # Move to the next box position
            x_pos += 1
            if x_pos >= 4:
                y_offset += box_height + 30  # Move to the next row, adjust spacing for progress bar
                x_offset = screen_width / 4
                x_pos = 1


# You can also use setattr
#setattr(player, 'experience', 0)

###test
player = Player('Adventurer', {'fists': {'hitChance': 70, 'min_damage': 1, 'max_damage': 3, 'weapon_type': 'blunt', 'value':0, 'min_level':0}})

skill =player.skills['Blunt']
# print(f'Weapon Skill:{skill}, Xp Required: {skill **1.5 *20}')
total_xp=0
total_hits = 0
prev_hits = 0
for x in range(50):
    xp = int(skill **(1+(skill*.02)) *50)
    xp_per_hit = 6 + skill
    hits_to_level = int(xp/xp_per_hit)
    more_hits = hits_to_level-prev_hits
    prev_hits = hits_to_level
    if skill in (1,2,5, 10,20,30,40,50):
        print(f'Skill Level:{skill}:   {total_xp} xp. {xp} to next. {hits_to_level} hits to Level, {more_hits} more. {total_hits} total hits')
    total_hits +=hits_to_level
    total_xp +=xp

    skill +=1

print(player.current_weapon.min_damage)