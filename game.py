import pygame
import random

pygame.init()

#Screen Dimensions
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

clock = pygame.time.Clock()
running = True

player_pos = pygame.Vector2(SCREEN_WIDTH / 5, SCREEN_HEIGHT / 2)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.draw.circle(screen, "white", player_pos, 20)

    pygame.display.flip()


pygame.quit()