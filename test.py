import pygame
import game_config
import adventure_class
running = True
on_adventure = True
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1000, 1000))
pygame.init()
while running:
    screen.fill(game_config.GREEN)
    clock.tick(6)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if on_adventure:
        adventure_class.draw_adventure(screen)
    pygame.display.update()